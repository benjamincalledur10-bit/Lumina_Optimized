"""Export/validate the CurseForge variant from the 26.2 Modrinth base.

Uses the audited official IDs in docs/editions/26.2. No JAR is committed
or embedded in overrides. Mandala is omitted only from CurseForge because
the user requested Mandala only in Modrinth; no Mandala replacement is used.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tomllib
import zipfile

from verify import fetch, require

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs/editions/26.2'
PACK = ROOT / 'packs/26.2'
VERSION = '26.2-beta.1'
SOURCE = ROOT / ('dist/Lumina-Optimized-' + VERSION + '.mrpack')
OUTPUT = ROOT / ('dist/Lumina-Optimized-' + VERSION + '-curseforge.zip')


def expected_overrides(archive, mapping):
    result = {n: archive.read(n) for n in archive.namelist()
              if n.startswith('overrides/') and not n.endswith('/')}
    omitted = 'file/' + Path(mapping['omissions'][0]['source_path']).name
    lines = result['overrides/options.txt'].decode().splitlines(keepends=True)
    seen = set()
    for i, line in enumerate(lines):
        key, sep, value = line.rstrip('\n').partition(':')
        if key in ('resourcePacks', 'incompatibleResourcePacks'):
            packs = json.loads(value)
            require(packs.count(omitted) == 1, 'Unexpected Mandala selection')
            packs.remove(omitted)
            lines[i] = key + sep + json.dumps(packs, ensure_ascii=False, separators=(',', ':')) + ('\n' if line.endswith('\n') else '')
            seen.add(key)
    require(len(seen) == 2, 'Missing resource selection lists')
    result['overrides/options.txt'] = ''.join(lines).encode()
    return result


def verify_mapping(mapping):
    require(hashlib.sha256(SOURCE.read_bytes()).hexdigest() == mapping['source_mrpack_sha256'], 'Source changed')
    require(mapping['version'] == VERSION and len(mapping['files']) == 48, 'Incomplete mapping')
    require({k: sum(r['kind'] == k for r in mapping['files']) for k in ('mods', 'resourcepacks', 'shaderpacks')} == {'mods': 43, 'resourcepacks': 3, 'shaderpacks': 2}, 'Wrong composition')
    publications = json.loads((DOCS / 'curseforge-publications.json').read_text())['data']
    files = {f['id']: f for f in publications['files']['data']}
    projects = {p['id']: p for p in publications['projects']['data']}
    present = {r['project_id'] for r in mapping['files']} | {p['project_id'] for p in mapping['embedded_providers']}
    require(len({r['project_id'] for r in mapping['files']}) == 48, 'Duplicate project')
    replacements = [r for r in mapping['files'] if r['replacement']]
    require(not replacements and not mapping['approved_replacements'], 'Unauthorized replacement')
    omissions = mapping.get('omissions', [])
    require(len(omissions) == 1 and omissions[0]['project_id'] == 664719 and omissions[0]['source_path'] == 'resourcepacks/MandalasGUI+Dakmode_1.21.6_v2.1.zip' and 664719 not in present, 'Unauthorized omission')
    source_files = {}
    with zipfile.ZipFile(SOURCE) as archive:
        source_files = {f['path']: f for f in json.loads(archive.read('modrinth.index.json'))['files']}
    require(set(source_files) == {r['source_path'] for r in mapping['files']} | {omissions[0]['source_path']}, 'Source content omitted')
    downloaded = {}
    for row in mapping['files']:
        file, project = files[row['file_id']], projects[row['project_id']]
        require(file['modId'] == project['id'] and file['fileName'] == Path(row['path']).name, 'IDs/name differ')
        require(file['isAvailable'] and file['fileStatus'] == 4 and project['isAvailable'] and project['status'] == 4, 'Unapproved content')
        require('26.2' in file['gameVersions'], 'Not published for 26.2')
        require(project['classId'] == {'mods': 6, 'resourcepacks': 12, 'shaderpacks': 6552}[row['kind']], 'Wrong content class')
        if row['kind'] == 'mods': require('Fabric' in file['gameVersions'], 'Not Fabric')
        if row['kind'] == 'shaderpacks': require('Iris' in file['gameVersions'], 'Not Iris')
        require(source_files[row['source_path']]['hashes'] == {'sha1': row['source_sha1'], 'sha512': row['source_sha512']}, 'Source hashes changed')
        data = fetch(row['validation_url']); downloaded[row['source_path']] = data
        require(len(data) == row['size'] == file['fileLength'], 'Size differs')
        require(hashlib.sha512(data).hexdigest() == row['sha512'] and hashlib.sha1(data).hexdigest() == row['sha1'], 'Byte hashes differ')
        require(any(h['algo'] == 1 and h['value'] == row['sha1'] for h in file['hashes']), 'Official SHA-1 differs')
        if row['kind'] == 'resourcepacks':
            with zipfile.ZipFile(io.BytesIO(data)) as resource:
                require(resource.testzip() is None, 'Corrupt resource pack')
                pack = json.loads(resource.read('pack.mcmeta'))['pack']
                if pack.get('pack_format', 0) > 64:
                    require('min_format' in pack and 'max_format' in pack, 'Missing mandatory resource format fields')
                def format_number(value):
                    return value[0] if isinstance(value, list) else value
                require(format_number(pack['min_format']) <= 88 <= format_number(pack['max_format']), 'Resource metadata excludes Minecraft format 88')
        if not row['replacement']:
            require(row['source_sha512'] == row['sha512'] and row['source_path'] == row['path'], 'Unexpected content change')
        for dependency in file['dependencies']:
            if dependency['relationType'] == 3: require(dependency['modId'] in present, 'Missing catalog dependency')
            if dependency['relationType'] == 5: require(dependency['modId'] not in present, 'Declared catalog conflict')
    for provider in mapping['embedded_providers']:
        origin, nested_path = provider['origin'].split('!', 1)
        container = downloaded['mods/' + origin]
        with zipfile.ZipFile(io.BytesIO(container)) as jar:
            nested = jar.read(nested_path)
        require(hashlib.sha1(nested).hexdigest() == provider['sha1'] and hashlib.sha512(nested).hexdigest() == provider['sha512'], 'Embedded provider differs')
        key = 'embedded_placeholder_files' if provider['slug'] == 'placeholder-api' else 'embedded_midnight_files'
        meta = next(f for f in publications[key]['data'] if f['id'] == provider['official_file_id'])
        require(meta['modId'] == provider['project_id'] and meta['isAvailable'] and meta['fileStatus'] == 4 and '26.2' in meta['gameVersions'] and 'Fabric' in meta['gameVersions'], 'Embedded publication incompatible')
        require(any(h['algo'] == 1 and h['value'] == provider['sha1'] for h in meta['hashes']), 'Embedded official hash differs')
        with zipfile.ZipFile(io.BytesIO(nested)) as jar:
            meta = json.loads(jar.read('fabric.mod.json'))
            require(meta['id'] == provider['fabric_id'] and meta['version'] == provider['fabric_version'], 'Embedded identity differs')


def build(mapping, packwiz):
    stage = ROOT / '.build/curseforge-26.2-beta1/export'
    if stage.exists(): shutil.rmtree(stage)
    stage.mkdir(parents=True)
    for name in ('pack.toml', 'index.toml', '.packwizignore'):
        if (PACK / name).exists(): shutil.copy2(PACK / name, stage / name)
    with zipfile.ZipFile(SOURCE) as archive:
        for name, data in expected_overrides(archive, mapping).items():
            path = stage / name.removeprefix('overrides/')
            path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(data)
    for row in mapping['files']:
        source = tomllib.loads((PACK / row['kind'] / row['descriptor']).read_text())
        path = stage / row['kind'] / row['descriptor']; path.parent.mkdir(exist_ok=True)
        path.write_text(f'name = {json.dumps(source["name"])}\nfilename = {json.dumps(Path(row["path"]).name)}\nside = {json.dumps(source["side"])}\npin = true\n\n[download]\nhash-format = "sha512"\nhash = "{row["sha512"]}"\nmode = "metadata:curseforge"\n\n[update.curseforge]\nproject-id = {row["project_id"]}\nfile-id = {row["file_id"]}\n')
    executable = shutil.which(packwiz); require(executable is not None, 'packwiz missing')
    command = [str(Path(executable).resolve()), '--cache', str(ROOT / '.build/edition-26.2/packwiz-cache'), '-y']
    subprocess.run([*command, 'refresh'], cwd=stage, check=True)
    subprocess.run([*command, 'curseforge', 'export', '--side', 'client', '--output', str(OUTPUT)], cwd=stage, check=True)


def verify_zip(mapping):
    with zipfile.ZipFile(SOURCE) as before, zipfile.ZipFile(OUTPUT) as archive:
        require(archive.testzip() is None, 'Corrupt ZIP')
        names = [n for n in archive.namelist() if not n.endswith('/')]
        require(len(names) == len(set(names)) and all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts for n in names), 'Unsafe ZIP paths')
        overrides = expected_overrides(before, mapping)
        require(set(names) == {'manifest.json', 'modlist.html', *overrides}, 'Unexpected files or embedded binaries')
        require(all(archive.read(n) == data for n, data in overrides.items()), 'Configuration changed')
        manifest = json.loads(archive.read('manifest.json'))
        require(manifest['name'].strip() == 'Lumina Optimized' and manifest['version'] == VERSION and manifest['manifestType'] == 'minecraftModpack' and manifest['manifestVersion'] == 1 and manifest['overrides'] == 'overrides', 'Wrong manifest identity')
        require(manifest['minecraft'] == {'version': '26.2', 'modLoaders': [{'id': 'fabric-0.19.5', 'primary': True}]}, 'Wrong target')
        expected = sorted((r['project_id'], r['file_id'], True) for r in mapping['files'])
        require(sorted((r['projectID'], r['fileID'], r['required']) for r in manifest['files']) == expected, 'Incomplete manifest')
        require(not json.loads(archive.read('overrides/config/sodium-extra-options.json'))['extra_settings']['reduce_resolution_on_mac'], 'macOS default changed')
        selection = dict(line.split(':', 1) for line in archive.read('overrides/options.txt').decode().splitlines())
        selected_files = [p for p in json.loads(selection['resourcePacks']) if p.startswith('file/')]
        require(set(selected_files) == {'file/' + Path(r['path']).name for r in mapping['files'] if r['kind'] == 'resourcepacks'} and len(selected_files) == 3, 'Selected resources differ from manifest')
    require(hashlib.sha256(SOURCE.read_bytes()).hexdigest() == mapping['source_mrpack_sha256'], 'Modrinth export changed')
    sha = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    report = {'version': VERSION, 'evidence_date': mapping['verified_on'], 'archive': OUTPUT.name, 'sha256': sha, 'size': OUTPUT.stat().st_size,
              'checks': {k: 'PASS' for k in ('official_ids_hashes_and_compatibility', 'catalog_dependencies_and_conflicts', 'nested_providers', 'zip_crc_and_safe_paths', 'complete_manifest', 'configs_and_resources', 'modrinth_unchanged')},
              'counts': {'manifest_references': 48, 'root_jars': 43, 'resourcepacks': 3, 'shaderpacks': 2, 'external_binaries_in_overrides': 0, 'overrides': 13}, 'approved_replacements': mapping['approved_replacements'], 'omissions': mapping['omissions'],
              'pending': list(mapping['publication_pending']), 'minecraft_tests': 'No gameplay test of the corrected CurseForge archive claimed.'}
    runtime_path = DOCS / 'runtime-curseforge.json'
    if runtime_path.exists():
        runtime = json.loads(runtime_path.read_text())
        if runtime.get('artifact_sha256') == sha or runtime.get('equivalent_archive_sha256') == sha:
            report['runtime_evidence'] = runtime_path.name
            report['minecraft_tests'] = runtime['scope']
            report['resource_startup'] = 'PASS' if runtime['observations']['resource_reload_completed'] and not runtime['observations']['mandala_metadata_error'] else 'FAIL'
    app_path = DOCS / 'curseforge-app-validation.json'
    if app_path.exists():
        app = json.loads(app_path.read_text())
        if app.get('archive_sha256') == sha and app.get('same_file_references') is True and app.get('same_override_bytes') is True and app.get('import') == app.get('export') == 'PASS':
            report['app_import_export'] = 'PASS'
            report['app_evidence'] = app_path.name
            report['artifact_origin'] = 'Corrected CurseForge App export, preserved byte-for-byte'
            report['pending'] = [item for item in report['pending']
                                 if 'CurseForge App' not in item]
    (DOCS / 'validation-curseforge.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    (OUTPUT.parent / (OUTPUT.name + '.sha256')).write_text(sha + '  ' + OUTPUT.name + '\n')
    print(json.dumps(report, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packwiz', default='packwiz')
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    mapping = json.loads((DOCS / 'curseforge-mapping.json').read_text())
    verify_mapping(mapping)
    if not args.verify_only: build(mapping, args.packwiz)
    verify_zip(mapping)


if __name__ == '__main__': main()
