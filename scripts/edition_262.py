"""Build/validate the independent 26.2 edition without touching the existing 26.3 or 1.21.11 editions.

python3 scripts/edition_262.py --build --packwiz .tools/bin/packwiz
Requires Python 3.11+ and a JDK (java, javac, javap). No gameplay is simulated.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tomllib
import zipfile

from verify import (FabricVersions, check_index, fetch, inspect_jar, require,
                    validate_modrinth_dependencies)

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'packs/26.2'
DOCS = ROOT / 'docs/editions/26.2'
WORK = ROOT / '.build/edition-26.2'
ARTIFACT = ROOT / 'dist/Lumina-Optimized-26.2-beta.1.mrpack'
PROFILE = '26.2-beta.1'
LOADER_URL = 'https://maven.fabricmc.net/net/fabricmc/fabric-loader/0.19.5/fabric-loader-0.19.5.jar'


def checked_download(row):
    official = json.loads(fetch('https://api.modrinth.com/v2/version/' + row['version']['id']))
    require(official['id'] == row['version']['id'] and
            official['project_id'] == row['project_id'] and
            official['version_number'] == row['version']['version_number'], 'Publication identity changed')
    legacy_mandala = (row['project_id'], official['id'], row['kind']) == ('h6zxsNVF', 'Z2ajDlEE', 'resourcepacks')
    require(('26.2' in official['game_versions'] or
             legacy_mandala and bool(row.get('compatibility_exception'))) and row['loader'] in official['loaders'],
            'Not published for target: ' + row['slug'])
    file = next(f for f in official['files'] if f['filename'] == row['file']['filename'])
    # The project-version listing can expose a file UUID omitted by the
    # version endpoint. Publication identity is pinned by project/version;
    # compare every download field, including both official hashes.
    require({k: v for k, v in file.items() if k != 'id'} ==
            {k: v for k, v in row['file'].items() if k != 'id'},
            'Official file metadata changed: ' + row['slug'])
    data = fetch(file['url'])
    require(len(data) == file['size'], 'Incorrect size: ' + row['slug'])
    for algorithm, expected in file['hashes'].items():
        require(hashlib.new(algorithm, data).hexdigest() == expected, 'Official hash mismatch: ' + row['slug'])
    pin = tomllib.loads((PACK / row['kind'] / row['descriptor']).read_text())
    require(pin['pin'] and pin['filename'] == file['filename'] and
            pin['download'] == {'url': file['url'], 'hash-format': 'sha512', 'hash': file['hashes']['sha512']} and
            pin['update']['modrinth'] == {'mod-id': row['project_id'], 'version': official['id']},
            'Pin differs from official publication: ' + row['slug'])
    with zipfile.ZipFile(io.BytesIO(data)) as container:
        require(container.testzip() is None, 'Corrupt archive: ' + row['slug'])
        if row['kind'] == 'resourcepacks':
            require(json.loads(container.read('pack.mcmeta')) == row['pack_mcmeta'], 'Resource metadata differs')
            metadata = row['pack_mcmeta']['pack']
            def format_number(value):
                return tuple(value) if isinstance(value, list) else (value, 0)
            if legacy_mandala:
                require(metadata.get('pack_format') == 64,
                        'Unreviewed Mandala metadata; only original format64 accepted')
            else:
                require('min_format' in metadata and 'max_format' in metadata and
                        format_number(metadata['min_format']) <= (88, 0) <= format_number(metadata['max_format']),
                        'Resource metadata excludes actual Minecraft 26.2 format 88')
    records = []
    if row['kind'] == 'mods':
        inspect_jar(data, file['filename'], records)
        require(records == row['jar_metadata'], 'JAR metadata differs: ' + row['slug'])
    return row, data, records


def resolve(inventory, engine):
    """Check predicates including nested candidates and Loader-provided aliases.

    This is a static selection model, not a replacement for Fabric's SAT solver.
    Java 25 includes native-math candidates when their predicates allow it.
    Actual Minecraft startup is checked separately.
    """
    chosen, alternatives = {}, {}
    for record in inventory:
        key = record['id']
        alternatives.setdefault(key, []).append(record)
        if key not in chosen or engine.compare(record['version'], chosen[key]['version']) > 0:
            chosen[key] = record
    inactive = {}
    # MixinExtras 0.5.5 supplied by Loader replaces older nested candidates,
    # including the older artifact whose ID is now an alias.
    for record in list(chosen.values()):
        for alias in record['provides']:
            if alias in chosen:
                other = chosen[alias]
                require('!' in other['origin'], 'External dependency duplicates a provider: ' + alias)
                inactive[alias] = {'record': other, 'reason': 'Provided by ' + record['id']}
                del chosen[alias]
    available = {'minecraft': '26.2', 'java': '25', 'fabricloader': '0.19.5'}
    for record in chosen.values():
        available[record['id']] = record['version']
        for alias in record['provides']:
            require(alias not in available, 'Duplicate alias: ' + alias)
            available[alias] = record['version']
    for record in chosen.values():
        for dependency, predicate in record['depends'].items():
            require(dependency in available and engine.matches(available[dependency], predicate),
                    f"Unresolved dependency: {record['id']} -> {dependency} {predicate}")
        for category in ('breaks', 'conflicts'):
            for conflict, predicate in record[category].items():
                require(conflict not in available or not engine.matches(available[conflict], predicate),
                        f"Declared {category}: {record['id']} -> {conflict}")
    return available, chosen, alternatives, inactive


def javap(path, cls, verbose=False):
    return subprocess.run(['javap', '-p', '-c', *(['-v'] if verbose else []),
                           '-classpath', str(path), cls], check=True, capture_output=True, text=True).stdout


def check_configs(blobs):
    jars = {}
    target = WORK / 'validator'
    target.mkdir(parents=True, exist_ok=True)
    for row, data, _ in blobs:
        if row['kind'] == 'mods':
            path = target / (row['slug'] + '.jar')
            path.write_bytes(data)
            jars[row['slug']] = path
    configs = PACK / 'config'
    parsed = {}
    for path in configs.rglob('*'):
        if path.suffix == '.json': parsed[path.name] = json.loads(path.read_text())
        if path.suffix == '.toml': parsed[path.name] = tomllib.loads(path.read_text())
    bbe = {x['option']: x['value'] for x in parsed['BBEConfig.json']['bbe.config.storage.main']}
    require(bbe['optimize.master'] and not bbe['optimize.banner'] and not bbe['optimize.sign'], 'BBE reference changed')
    require(all(bbe[k] for k in ('animation.chest', 'animation.shulker', 'animation.bell', 'animation.decoratedpot')), 'Animation disabled')
    require(bbe['misc.shademode'] == 0 and bbe['misc.update_scheduler'] == 1,
            'Requested BBE Sodium shading/Smart scheduler changed')
    ec = parsed['entityculling.json']; mc = parsed['moreculling.toml']
    require(ec['safeMode'] and ec['tickCulling'] and not ec['solidLeaves'], 'Beta requires tick culling with safe mode')
    # The explicitly requested differences from the 26.3 configuration baseline.
    baseline = ROOT / 'pack/config'
    require({str(p.relative_to(configs)) for p in configs.rglob('*') if p.is_file()} ==
            {str(p.relative_to(baseline)) for p in baseline.rglob('*') if p.is_file()},
            'Configuration file set changed')
    for path in configs.rglob('*'):
        if not path.is_file():
            continue
        reference = baseline / path.relative_to(configs)
        if path.name == 'entityculling.json':
            expected = json.loads(reference.read_text())
            expected['tickCulling'] = True
            require(json.loads(path.read_text()) == expected, 'Unreviewed Entity Culling setting change')
        elif path.name == 'BBEConfig.json':
            expected = json.loads(reference.read_text())
            for option in expected['bbe.config.storage.main']:
                if option['option'] == 'misc.shademode': option['value'] = 0
                if option['option'] == 'misc.update_scheduler': option['value'] = 1
            require(json.loads(path.read_text()) == expected, 'Unreviewed BBE setting change')
        else:
            require(path.read_bytes() == reference.read_bytes(), 'Unreviewed config change: ' + path.name)
    require(mc['leavesCullingMode'] == 'DEFAULT' and not mc['useBlockStateCulling'] and
            not mc['includeMangroveRoots'] and not mc['useItemFrameLOD'] and not mc['useItemFrame3FaceCulling'], 'Overlapping leaf culling or visual change')
    require(parsed['cullleaves.json'] == {'enabled': True, 'cullRoots': False}, 'Leaf reference changed')
    require(parsed['lambdynlights.toml']['mode'] == 'off', 'Dynamic lights must start off')
    require((configs / 'iris.properties').read_text().strip() == 'enableShaders=false', 'Shaders must start off')
    require(parsed['sodium-extra-options.json'] == {'extra_settings': {'reduce_resolution_on_mac': False}}, 'Requested macOS resolution default changed')
    require(parsed['gnetum.json']['enabled']['value'] == 'ON' and parsed['gnetum.json']['downscale']['value'] == 'OFF', 'Gnetum base settings changed')
    require(parsed['c2me.toml']['version'] == 3 and not parsed['c2me.toml']['clientSideConfig']['modifyMaxVDConfig']['enableExtRenderDistanceProtocol'], 'C2ME schema/protocol changed')
    for slug, cls, keys in [
        ('better-block-entities', 'betterblockentities.client.gui.config.builder.ConfigBuilder', bbe),
        ('entityculling', 'dev.tr7zw.entityculling.versionless.Config', ec),
        ('moreculling', 'ca.fxco.moreculling.config.MoreCullingConfig', mc),
        ('cull-leaves', 'eu.midnightdust.cullleaves.config.CullLeavesConfig', parsed['cullleaves.json']),
        ('sodium-extra', 'me.flashyreese.mods.sodiumextra.client.config.SodiumExtraGameOptions$ExtraSettings', ['reduceResolutionOnMac']),
        ('iris', 'net.irisshaders.iris.config.IrisConfig', ['enableShaders', 'Properties.getProperty']),
        ('fastquit', 'me.contaria.fastquit.FastQuitConfig', ['ixeris', 'allowMultipleServers', 'MODS_THAT_CONFLICT_WITH_MULTIPLE_SERVERS']),
    ]:
        code = javap(jars[slug], cls)
        require(all(key in code for key in keys), 'Configuration keys not in actual JAR: ' + slug)
    require('Toml4jConfigSerializer' in javap(jars['moreculling'], 'ca.fxco.moreculling.MoreCulling$1'), 'More Culling serializer changed')
    require('LOWER_CASE_WITH_UNDERSCORES' in javap(jars['sodium-extra'], 'me.flashyreese.mods.sodiumextra.client.config.SodiumExtraGameOptions'), 'Sodium Extra serializer changed')
    code = javap(jars['lambdynamiclights'], 'dev.lambdaurora.lambdynlights.DynamicLightsConfig')
    require('String mode' in code and 'lambdynlights.toml' in code, 'Dynamic lights schema changed')
    with zipfile.ZipFile(jars['lambdynamiclights']) as container:
        defaults = tomllib.loads(container.read('lambdynlights.toml').decode())
        # Includes per-entity settings (e.g. glow_item_frame), handled by the
        # light source registry rather than DynamicLightsConfig directly.
        def known_keys(actual, reference):
            require(set(actual) <= set(reference), 'Unknown dynamic-light setting')
            for key, value in actual.items():
                if isinstance(value, dict): known_keys(value, reference[key])
        known_keys(parsed['lambdynlights.toml'], defaults)
    gnetum_code = javap(jars['gnetum'], 'me.decce.gnetum.GnetumConfig')
    require(all(key in gnetum_code for key in parsed['gnetum.json']), 'Gnetum config keys changed')
    require('mixin.perf.remove_biome_temperature_cache=false' in (configs / 'modernfix-mixins.properties').read_text(), 'Temperature cache collision uncorrected')
    for slug, cls in [
        ('modernfix-mvus', 'org.embeddedt.modernfix.common.mixin.perf.remove_biome_temperature_cache.BiomeMixin'),
        ('lithium', 'net.caffeinemc.mods.lithium.mixin.world.temperature_cache.BiomeMixin')]:
        require('public float getTemperature(net.minecraft.core.BlockPos, int)' in javap(jars[slug], cls), 'Temperature method changed; reassess correction')
    with zipfile.ZipFile(jars['c2me-fabric']) as container:
        for part, cls, keys in [
            ('base', 'com.ishland.c2me.base.common.config.ConfigSystem', ['c2me.toml']),
            ('client-uncapvd', 'com.ishland.c2me.client.uncapvd.common.Config', ['clientSideConfig.modifyMaxVDConfig.maxViewDistance', 'clientSideConfig.modifyMaxVDConfig.enableExtRenderDistanceProtocol'])]:
            name = next(n for n in container.namelist() if n.startswith('META-INF/jars/c2me-fabric-' + part + '-'))
            path = target / ('c2me-' + part + '.jar'); path.write_bytes(container.read(name))
            require(all(key in javap(path, cls) for key in keys), 'C2ME config changed: ' + part)
    schema = {
        'MainConfig': ['features', 'dynamic', 'breeding-cap', 'activation-range', 'mob-spawning'],
        'OptimizationConfig': ['reduce-sync-loads', 'cache-ticking-chunks', 'optimize-command-blocks', 'fast-biome-lookups', 'cancel-duplicate-fluid-ticks'],
        'data.FeatureConfig': ['prevent-enderpearl-chunkloading', 'chunk-tick-distance-affects-random-ticks', 'prevent-moving-into-unloaded-chunks', 'autosave-interval-seconds', 'xp-merge-fraction', 'xp-merge-radius', 'item-merge-radius', 'lobotomize-villagers.enabled', 'lobotomize-villagers.tick-interval'],
        'data.dynamic.DynamicConfig': ['enabled', 'default-values', 'dynamic-settings'],
        'data.activation_range.ActivationRangeConfig': ['enabled', 'use-vertical-range', 'skip-non-immune'],
        'data.breeding_cap.BreedingCapConfig': ['enabled'],
        'data.mob_spawning.MobSpawnConfig': ['zombie-reinforcements', 'nether-portal-randomticks', 'monster-spawners', 'infested', 'categories'],
        'data.mob_spawning.EnforcedMobcap': ['enforce-mobcap'],
    }
    for cls, keys in schema.items():
        code = javap(jars['servercore'], 'me.wesley1808.servercore.common.config.' + cls, verbose=True)
        require(all('value="' + key + '"' in code for key in keys), 'ServerCore schema changed: ' + cls)
    with zipfile.ZipFile(jars['servercore']) as container:
        yaml = target / 'snakeyaml.jar'
        yaml.write_bytes(container.read(next(n for n in container.namelist() if n.startswith('META-INF/jars/snakeyaml-') and n.endswith('.jar'))))
    subprocess.run(['javac', '-cp', str(yaml), '-d', str(target), str(ROOT / 'scripts/ServerCoreConfigCheck.java')], check=True)
    subprocess.run(['java', '-cp', str(target) + os.pathsep + str(yaml), 'ServerCoreConfigCheck', str(configs / 'servercore/config.yml'), str(configs / 'servercore/optimizations.yml')], check=True)
    options = dict(line.split(':', 1) for line in (PACK / 'options.txt').read_text().splitlines())
    requested = {'renderDistance': '16', 'simulationDistance': '5',
                 'preferredGraphicsBackend': '"vulkan"', 'renderClouds': '"false"',
                 'cloudRange': '26', 'particles': '1', 'graphicsPreset': '"custom"'}
    require(set(options) == {'version', 'resourcePacks', 'incompatibleResourcePacks', *requested}
            and options['version'] == '4903' and all(options[k] == v for k, v in requested.items()),
            'Unexpected graphics overrides or requested default mismatch')
    resources = ['file/' + r['file']['filename'] for r, _, _ in blobs if r['kind'] == 'resourcepacks']
    require(set(json.loads(options['resourcePacks'])) == {'vanilla', *resources}, 'Resources not enabled')
    require(json.loads(options['incompatibleResourcePacks']) == ['file/MandalasGUI+Dakmode_1.21.6_v2.1.zip'], 'Unreviewed resource format acceptance')


def build(blobs, packwiz):
    """Seed an isolated packwiz cache from already officially verified bytes."""
    cache = WORK / 'packwiz-cache'; cache.mkdir(parents=True, exist_ok=True)
    hashes = {key: [] for key in ('length-bytes', 'sha1', 'sha256', 'sha512')}
    for _, data, _ in blobs:
        sha = hashlib.sha256(data).hexdigest()
        path = cache / sha[:2] / sha[2:]; path.parent.mkdir(exist_ok=True); path.write_bytes(data)
        hashes['length-bytes'].append(str(len(data)))
        for algorithm in ('sha1', 'sha256', 'sha512'):
            hashes[algorithm].append(hashlib.new(algorithm, data).hexdigest())
    (cache / 'index.json').write_text(json.dumps({'Version': 2, 'Hashes': hashes}) + '\n')
    executable = shutil.which(packwiz)
    require(executable is not None, 'packwiz not found')
    command = [str(Path(executable).resolve()), '--cache', str(cache)]
    ARTIFACT.parent.mkdir(exist_ok=True)
    subprocess.run([*command, 'refresh'], cwd=PACK, check=True)
    subprocess.run([*command, 'modrinth', 'export', '-o', str(ARTIFACT)], cwd=PACK, check=True)


def check_export(blobs):
    expected = {r['kind'] + '/' + r['file']['filename']: r for r, _, _ in blobs}
    require(ARTIFACT.is_file(), 'Export missing; use --build')
    with zipfile.ZipFile(ARTIFACT) as archive:
        require(archive.testzip() is None, 'Corrupt mrpack')
        names = archive.namelist()
        require(len(names) == len(set(names)), 'Duplicate ZIP paths')
        require(all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts for n in names), 'Unsafe ZIP path')
        index = json.loads(archive.read('modrinth.index.json'))
        require(index['formatVersion'] == 1 and index['game'] == 'minecraft' and index['name'] == 'Lumina Optimized' and index['versionId'] == PROFILE, 'Export identity changed')
        require(index['dependencies'] == {'minecraft': '26.2', 'fabric-loader': '0.19.5'}, 'Export target changed')
        require(len(index['files']) == len(expected) and {f['path'] for f in index['files']} == set(expected), 'Incomplete export (packwiz can skip timed-out downloads)')
        for file in index['files']:
            official = expected[file['path']]['file']
            require(file['hashes'] == official['hashes'] and file['downloads'] == [official['url']] and file['fileSize'] == official['size'], 'Export URL/hash/size mismatch: ' + file['path'])
            require(file.get('env', {}).get('client') == 'required', 'Client content made optional')
        overrides = {str(p.relative_to(PACK)): p.read_bytes() for p in (PACK / 'config').rglob('*') if p.is_file()}
        overrides['options.txt'] = (PACK / 'options.txt').read_bytes()
        require({n for n in names if not n.endswith('/')} == {'modrinth.index.json', *('overrides/' + p for p in overrides)}, 'Unexpected overrides or embedded binaries')
        for path, data in overrides.items():
            require(archive.read('overrides/' + path) == data, 'Exported config mismatch: ' + path)
    sha = hashlib.sha256(ARTIFACT.read_bytes()).hexdigest()
    (ARTIFACT.parent / ('SHA256SUMS-' + PROFILE)).write_text(sha + '  ' + ARTIFACT.name + '\n')
    return {'path': str(ARTIFACT.relative_to(ROOT)), 'size': ARTIFACT.stat().st_size, 'sha256': sha, 'downloads': len(expected), 'overrides': len(overrides)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build', action='store_true')
    parser.add_argument('--packwiz', default='packwiz')
    args = parser.parse_args()
    WORK.mkdir(parents=True, exist_ok=True)
    require(all(shutil.which(x) for x in ('java', 'javac', 'javap')), 'A JDK is required for validation')
    selection = json.loads((DOCS / 'selection.json').read_text())
    rows = selection['selection']
    require(not selection['omissions'] and any(r['project_id'] == 'h6zxsNVF' and r['version']['id'] == 'Z2ajDlEE' for r in rows), 'Modrinth Mandala selection changed')
    require(any(r['slug'] == 'gnetum' for r in rows), '26.3 base Gnetum must be preserved')
    require({str(p.relative_to(PACK)) for p in PACK.rglob('*.pw.toml')} == {r['kind'] + '/' + r['descriptor'] for r in rows}, 'Unlisted/missing component')
    require(selection['edition'] == PROFILE and selection['minecraft'] == '26.2' and selection['java'] == 25 and selection['fabric_loader'] == '0.19.5', 'Selection identity/platform changed')
    with ThreadPoolExecutor(max_workers=5) as executor:
        blobs = list(executor.map(checked_download, rows))
    loader = fetch(LOADER_URL)
    require(hashlib.sha1(loader).hexdigest() == fetch(LOADER_URL + '.sha1').decode().strip(), 'Loader official hash mismatch')
    inventory = []
    with zipfile.ZipFile(io.BytesIO(loader)) as container:
        require(container.testzip() is None, 'Loader corrupt')
        for path in container.namelist():
            if path.startswith('META-INF/jars/') and path.endswith('.jar'):
                inspect_jar(container.read(path), 'fabric-loader!' + path, inventory)
    for _, _, records in blobs: inventory.extend(records)
    engine = FabricVersions(loader)
    try: available, chosen, alternatives, inactive = resolve(inventory, engine)
    finally: engine.close()
    embedded = selection['embedded_publications']
    for row in embedded:
        require(any(r['jar_sha512'] == row['file']['hashes']['sha512'] and r['origin'] == row['provider']['origin'] for r in inventory), 'Embedded publication bytes not found')
        require('26.2' in row['version']['game_versions'] and 'fabric' in row['version']['loaders'], 'Embedded dependency not published for target')
    projects = {r['project_id']: r['version'] for r in rows}
    projects.update({r['project_id']: r['version'] for r in embedded})
    validate_modrinth_dependencies(projects)
    check_configs(blobs)
    if args.build: build(blobs, args.packwiz)
    check_index(PACK)
    export = check_export(blobs)
    preserved = WORK / 'preserved.json'
    preservation = 'not checked: initial local snapshot unavailable'
    if preserved.exists():
        for path, sha in json.loads(preserved.read_text()).items():
            require(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == sha, 'Pre-existing file changed: ' + path)
        preservation = 'PASS: all pre-existing definitions, artifacts and local changes unchanged'
    result = {
        'edition': PROFILE, 'evidence_date': selection['evidence_date'],
        'checks': {key: 'PASS' for key in ('official_publications_and_hashes', 'recursive_jar_integrity', 'fabric_and_modrinth_dependencies', 'declared_conflicts', 'configuration_keys_and_invariants', 'packwiz_index', 'mrpack_completeness_and_overrides')},
        'counts': {**dict(Counter(r['role'] for r in rows)), 'external_mod_jars': sum(r['kind'] == 'mods' for r in rows), 'resolved_nested_ids': sum('!' in r['origin'] for r in chosen.values()), 'nested_candidate_instances': sum('!' in r['origin'] for r in inventory), 'resolved_mod_ids_excluding_platform': len(chosen)},
        'export': export, 'preservation_existing_editions_and_local_changes': preservation,
        'available': available, 'resolved_inventory': list(chosen.values()),
        'inactive_optional_candidates': inactive,
        'multiple_nested_candidates': {k: v for k, v in alternatives.items() if len(v) > 1},
        'manual_user_test': 'User-reported beta gameplay/FPS screenshot; saving/reopening and extended testing not confirmed',
        'user_observations_alpha1': selection.get('user_observations_alpha1', {}),
        'user_observations_beta1': selection.get('user_observations_beta1', {}),
        'config_changes_from_alpha1': selection['config_changes_from_alpha1'],
        'default_settings_revision': selection['default_settings_revision'],
        'pending': ['Extended gameplay, save and reopen; CurseForge App workflow', 'Feature-by-feature lighting/HUD/model checks', 'Both Lumina shaders enabled separately', 'Long sessions and controlled performance comparison', 'Windows/Linux startup and play'],
    }
    (DOCS / 'validation.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'checks': result['checks'], 'counts': result['counts'], 'export': export, 'existing_editions': preservation}, indent=2))


if __name__ == '__main__':
    main()
