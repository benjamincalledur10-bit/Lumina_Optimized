"""Validación estática. Usa VersionPredicate de Fabric; no arranca Minecraft."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tomllib
import urllib.request
from urllib.parse import urlsplit, unquote
import zipfile
from profiles import ROOT, configs, descriptors, pack_version, profiles

CACHE = ROOT / '.build/downloads'
LOADER_URL = 'https://maven.fabricmc.net/net/fabricmc/fabric-loader/0.19.5/fabric-loader-0.19.5.jar'

def require(condition, message):
    if not condition:
        raise ValueError(message)

def fetch(url):
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / hashlib.sha256(url.encode()).hexdigest()
    if not path.exists():
        request = urllib.request.Request(url, headers={'User-Agent': 'Lumina-Optimized/0.1.0-alpha.4'})
        with urllib.request.urlopen(request, timeout=60) as response:
            path.write_bytes(response.read())
    return path.read_bytes()

def publication_or_local_pin(mod, require_publications=False):
    """Never label locally computed hashes/dependencies as published metadata."""
    api_url = 'https://api.modrinth.com/v2/version/' + mod['update']['modrinth']['version']
    if require_publications:
        return json.loads(fetch(api_url)), 'published_metadata_and_hashes'
    local = ROOT / 'docs/research/local-jars-alpha.4.json'
    evidence = json.loads(local.read_text())['jars'] if local.exists() else []
    matches = [item for item in evidence if item['version_id'] == mod['update']['modrinth']['version']]
    if matches and not matches[0]['publication_metadata_verified']:
        item = matches[0]
        # Prefer full API metadata whenever it is actually available in the download cache.
        api_url = 'https://api.modrinth.com/v2/version/' + item['version_id']
        if (CACHE / hashlib.sha256(api_url.encode()).hexdigest()).exists():
            return json.loads(fetch(api_url)), 'published_metadata_and_hashes'
        url = urlsplit(item['official_url'])
        require(url.scheme == 'https' and url.netloc == 'cdn.modrinth.com', 'Origen local no oficial')
        require(item['download_origins'][0].split('?')[0] == item['official_url'], 'Origen diferente')
        require(unquote(url.path).split('/') == ['', 'data', item['project_id'], 'versions', item['version_id'], item['filename']], 'IDs/ruta no corresponden al origen')
        require(item['pin_record']['dependencies'] is None, 'No inventar dependencias de publicación no consultada')
        return item['pin_record'], 'local_hashes_and_official_download_origin; publication_metadata_pending'
    version = json.loads(fetch('https://api.modrinth.com/v2/version/' + mod['update']['modrinth']['version']))
    return version, 'published_metadata_and_hashes'

def validate_sha512_evidence(sources):
    """Check supplied published hashes only against the exact recorded identities."""
    path = ROOT/'docs/research/modrinth-sha512-alpha.4.json'
    if not path.exists():
        return {}
    evidence = json.loads(path.read_text())
    checked = {}
    by_name = {path.name:source for path,source in sources.items()}
    for record in evidence['records']:
        name = record['descriptor']
        require(name not in checked and name in by_name, 'Evidencia duplicada o sin mod: '+name)
        mod, _, data, version, inventory = by_name[name]
        identity = mod['update']['modrinth']
        require(identity['mod-id'] == record['project_id'] and identity['version'] == record['version_id'], 'IDs distintos de la evidencia: '+name)
        require(version['version_number'] == record['publication_version'] and mod['filename'] == record['filename'], 'Versión/archivo distintos de la evidencia: '+name)
        require(inventory[0]['id'] == record['fabric_mod_id'] and inventory[0]['version'] == record['fabric_mod_version'], 'Versión interna distinta de la evidencia: '+name)
        require(hashlib.sha512(data).hexdigest() == record['sha512'], 'SHA-512 publicado aportado no coincide: '+name)
        require(mod['download']['hash-format'] == 'sha512' and mod['download']['hash'] == record['sha512'], 'Packwiz no usa el SHA-512 aportado: '+name)
        checked[name] = {**record, 'status':'matched_local_jar_and_packwiz', 'evidence_date':evidence['evidence_date'], 'verified_date':evidence['verified_date'], 'source':evidence['source']}
    return checked

class FabricVersions:
    def __init__(self, loader):
        target = ROOT / '.build/validator'
        target.mkdir(parents=True, exist_ok=True)
        jar = target / 'fabric-loader.jar'
        jar.write_bytes(loader)
        subprocess.run(['javac', '-cp', str(jar), '-d', str(target), str(ROOT / 'scripts/FabricVersions.java')], check=True)
        self.process = subprocess.Popen(['java', '-cp', str(target) + os.pathsep + str(jar), 'FabricVersions'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    def query(self, operation, a, b):
        require(not any(c in a+b for c in '\t\n\r'), 'Predicado con delimitadores')
        self.process.stdin.write(f'{operation}\t{a}\t{b}\n')
        self.process.stdin.flush()
        result = self.process.stdout.readline().strip()
        require(bool(result), 'Falló el parser de versiones de Fabric')
        return result
    def matches(self, version, expressions):
        if isinstance(expressions, list):
            return any(self.matches(version, expression) for expression in expressions)
        return self.query('match', version, expressions) == 'true'
    def compare(self, a, b):
        return int(self.query('compare', a, b))
    def close(self):
        self.process.stdin.close()
        require(self.process.wait(timeout=10) == 0, 'Falló el helper de Fabric')

def inspect_jar(data, origin, inventory):
    with zipfile.ZipFile(io.BytesIO(data)) as jar:
        require(jar.testzip() is None, f'JAR corrupto: {origin}')
        if 'fabric.mod.json' not in jar.namelist():
            return
        raw_metadata = jar.read('fabric.mod.json')
        try:
            metadata = json.loads(raw_metadata)
            metadata_note = None
        except json.JSONDecodeError:
            # BetterGrassify contiene un salto literal en description; no modificar el JAR.
            metadata = json.loads(raw_metadata, strict=False)
            metadata_note = 'Control literal en string; requiere parser permisivo de Fabric. JAR conservado sin cambios.'
        inventory.append({'origin': origin, 'id': metadata['id'], 'version': metadata['version'],
                          'jar_sha512': hashlib.sha512(data).hexdigest(),
                          'depends': metadata.get('depends', {}), 'breaks': metadata.get('breaks', {}),
                          'recommends': metadata.get('recommends', {}), 'suggests': metadata.get('suggests', {}),
                          'conflicts': metadata.get('conflicts', {}), 'provides': metadata.get('provides', []),
                          'environment': metadata.get('environment', '*'), 'metadata_note': metadata_note})
        for nested in metadata.get('jars', []):
            inspect_jar(jar.read(nested['file']), origin + '!' + nested['file'], inventory)

def check_index(folder):
    manifest = tomllib.loads((folder / 'pack.toml').read_text())
    index_bytes = (folder / manifest['index']['file']).read_bytes()
    require(hashlib.new(manifest['index']['hash-format'], index_bytes).hexdigest() == manifest['index']['hash'], 'Hash del índice inválido')
    index = tomllib.loads(index_bytes.decode())
    for entry in index.get('files', []):
        data = (folder / entry['file']).read_bytes()
        require(hashlib.new(entry.get('hash-format', index['hash-format']), data).hexdigest() == entry['hash'], f"Hash de fuente inválido: {entry['file']}")

def resolve(inventory, engine):
    chosen, alternatives = {}, {}
    for record in inventory:
        key = record['id']
        alternatives.setdefault(key, []).append(record)
        if key not in chosen or engine.compare(record['version'], chosen[key]['version']) > 0:
            chosen[key] = record
    available = {'minecraft': '26.3', 'java': '25', 'fabricloader': '0.19.5'}
    for record in chosen.values():
        available[record['id']] = record['version']
        for alias in record['provides']:
            require(alias not in available, 'Alias duplicado: '+alias)
            available[alias] = record['version']
    soft_conflicts = []
    for record in chosen.values():
        for dependency, predicate in record['depends'].items():
            require(dependency in available and engine.matches(available[dependency], predicate), f"Dependencia no resuelta: {record['id']} -> {dependency} {predicate}")
        for conflict, predicate in record['breaks'].items():
            require(conflict not in available or not engine.matches(available[conflict], predicate), f"Incompatibilidad: {record['id']} -> {conflict}")
        for conflict, predicate in record['conflicts'].items():
            if conflict in available and engine.matches(available[conflict], predicate):
                soft_conflicts.append(f"{record['id']} -> {conflict}")
    require(not soft_conflicts, 'Conflictos advertidos: '+str(soft_conflicts))
    return available, chosen, {k:v for k,v in alternatives.items() if len(v)>1}

def validate_configs():
    for path in (ROOT / 'pack/config').glob('*.json'):
        json.loads(path.read_text())
    ec = json.loads((ROOT / 'pack/config/entityculling.json').read_text())
    mc = json.loads((ROOT / 'pack/config/moreculling.json').read_text())
    bbe = json.loads((ROOT / 'pack/config/BBEConfig.json').read_text())
    require(ec['safeMode'] and not ec['tickCulling'] and not ec['solidLeaves'], 'Referencia Entity Culling alterada')
    require(mc['leavesCullingMode']=='DEFAULT' and not mc['useItemFrameLOD'] and not mc['useItemFrame3FaceCulling'], 'Calidad More Culling alterada')
    require(tomllib.loads((ROOT/'variants/moreculling.toml').read_text()) == mc, 'TOML More Culling debe conservar valores del JSON histórico')
    options = {x['option']:x['value'] for x in bbe['bbe.config.storage.main']}
    require(options['optimize.master'] is False and options['optimize.banner'] is False and options['optimize.sign'] is False, 'Referencia BBE alterada')
    require(all(options[x] for x in ['animation.chest','animation.shulker','animation.bell','animation.decoratedpot']), 'Animaciones desactivadas')
    c2me = tomllib.loads((ROOT / 'variants/c2me.toml').read_text())
    require(c2me['version']==3 and c2me['clientSideConfig']['modifyMaxVDConfig']['enableExtRenderDistanceProtocol'] is False, 'C2ME config inválida')
    # Comprobar nombres contra campos/strings de las clases publicadas, no un esquema inventado.
    for filename, cls, keys in [
        ('entityculling','dev.tr7zw.entityculling.versionless.Config',ec.keys()),
        ('moreculling','ca.fxco.moreculling.config.MoreCullingConfig',mc.keys()),
        ('better-block-entities','betterblockentities.client.gui.config.builder.ConfigBuilder',options.keys())]:
        descriptor = tomllib.loads((ROOT / 'pack/mods' / (filename+'.pw.toml')).read_text())
        jar = ROOT / '.build/validator' / (filename+'.jar')
        jar.write_bytes(fetch(descriptor['download']['url']))
        disassembly = subprocess.run(['javap','-p','-c','-classpath',str(jar),cls], check=True, capture_output=True, text=True).stdout
        for key in keys:
            require(key in disassembly, 'Opción ausente en JAR: '+key)
    code = subprocess.run(['javap','-p','-c','-classpath',str(ROOT/'.build/validator/moreculling.jar'),'ca.fxco.moreculling.MoreCulling$1'],check=True,capture_output=True,text=True).stdout
    require('Toml4jConfigSerializer' in code, 'Serializador More Culling no coincide')
    slo = json.loads((ROOT/'variants/structure_layout_optimizer.jsonc').read_text())
    require(slo == {'deduplicateShuffledTemplatePoolElementList': False}, 'Deduplicación SLO debe permanecer desactivada')
    for filename, cls, expected in [
        ('structure-layout-optimizer','telepathicgrunt.structure_layout_optimizer.SloConfig', ['deduplicateShuffledTemplatePoolElementList', 'structure_layout_optimizer']),
        ('resourceful-config','com.teamresourceful.resourcefulconfig.common.loader.ParsedConfig', ['.jsonc', 'getConfigPath']),
        ('resourceful-config','com.teamresourceful.resourcefulconfig.common.loader.Loader', ['loadConfig', 'JsonObject.get'])]:
        mod = tomllib.loads((ROOT/'variants'/(filename+'.pw.toml')).read_text())
        jar = ROOT/'.build/validator'/(filename+'.jar')
        jar.write_bytes(fetch(mod['download']['url']))
        code = subprocess.run(['javap','-p','-c','-v','-classpath',str(jar),cls],check=True,capture_output=True,text=True).stdout
        require(all(key in code for key in expected), 'Esquema/ruta SLO no verificado: '+cls)
    modernfix = (ROOT/'variants/modernfix-mixins.properties').read_text()
    require('mixin.perf.remove_biome_temperature_cache=false' in modernfix, 'Colisión de caché de biomas no desactivada')
    mod = tomllib.loads((ROOT/'variants/modernfix-mvus.pw.toml').read_text())
    with zipfile.ZipFile(io.BytesIO(fetch(mod['download']['url']))) as jar:
        require(any('perf/remove_biome_temperature_cache/' in path for path in jar.namelist()), 'Mixin ModernFix ausente')
    require((ROOT/'variants/iris.properties').read_text().strip()=='enableShaders=false', 'Shaders deben comenzar desactivados')
    iris = tomllib.loads((ROOT/'variants/iris.pw.toml').read_text())
    path = ROOT/'.build/validator/iris.jar'
    path.write_bytes(fetch(iris['download']['url']))
    code = subprocess.run(['javap','-p','-c','-classpath',str(path),'net.irisshaders.iris.config.IrisConfig'],check=True,capture_output=True,text=True).stdout
    require('String enableShaders' in code and 'Properties.getProperty' in code, 'Opción real Iris no encontrada')
    servercore = tomllib.loads((ROOT/'variants/servercore.pw.toml').read_text())
    jar_path = ROOT/'.build/validator/servercore.jar'
    jar_path.write_bytes(fetch(servercore['download']['url']))
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
        code = subprocess.run(['javap','-p','-v','-classpath',str(jar_path),'me.wesley1808.servercore.common.config.'+cls],check=True,capture_output=True,text=True).stdout
        require(all('value="'+key+'"' in code for key in keys), 'ServerCore schema changed: '+cls)
    with zipfile.ZipFile(jar_path) as container:
        yaml_jar = ROOT/'.build/validator/snakeyaml.jar'
        yaml_jar.write_bytes(container.read('META-INF/jars/snakeyaml-2.7.jar'))
    subprocess.run(['javac','-cp',str(yaml_jar),'-d',str(yaml_jar.parent),str(ROOT/'scripts/ServerCoreConfigCheck.java')],check=True)
    subprocess.run(['java','-cp',str(yaml_jar.parent)+os.pathsep+str(yaml_jar),'ServerCoreConfigCheck',str(ROOT/'variants/servercore/config.yml'),str(ROOT/'variants/servercore/optimizations.yml')],check=True)
    async_config = tomllib.loads((ROOT/'variants/asynclogger.toml').read_text())
    require(async_config['enabled'] and not async_config['noDebugLog'] and not async_config['testPerformance'] and not async_config['filtering']['enabled'], 'Async Logger must preserve diagnostic messages')
    async_mod = tomllib.loads((ROOT/'variants/asynclogger.pw.toml').read_text())
    async_jar = ROOT/'.build/validator/asynclogger.jar'
    async_jar.write_bytes(fetch(async_mod['download']['url']))
    code = subprocess.run(['javap','-p','-v','-classpath',str(async_jar),'me.decce.asynclogger.core.AsyncLoggerConfig'],check=True,capture_output=True,text=True).stdout
    require('filtering.enabled' in code and 'noDebugLog' in code and 'testPerformance' in code, 'Async Logger schema changed')
    require((ROOT/'variants/biome-blend-options.txt').read_bytes() == b'version:5023\nbiomeBlendRadius:2\nbetterBiomeBlendRadius:2\n', 'Conservar mezcla de biomas de referencia; no fijar otros ajustes gráficos')
    bbb_mod = tomllib.loads((ROOT/'variants/better-biome-blend.pw.toml').read_text())
    bbb_jar = ROOT/'.build/validator/better-biome-blend.jar'
    bbb_jar.write_bytes(fetch(bbb_mod['download']['url']))
    code = subprocess.run(['javap','-p','-c','-classpath',str(bbb_jar),'fionathemortal.betterbiomeblend.mixin.MixinOptions'],check=True,capture_output=True,text=True).stdout
    require('String betterBiomeBlendRadius' in code and 'OptionAccess.process' in code, 'Persistencia BBB no encontrada en el JAR')
    c2me_mod = tomllib.loads((ROOT/'variants/c2me-fabric.pw.toml').read_text())
    with zipfile.ZipFile(io.BytesIO(fetch(c2me_mod['download']['url']))) as container:
        for part, cls, expected_strings in [
            ('base','com.ishland.c2me.base.common.config.ConfigSystem',['c2me.toml']),
            ('client-uncapvd','com.ishland.c2me.client.uncapvd.common.Config',
             ['clientSideConfig.modifyMaxVDConfig.maxViewDistance','clientSideConfig.modifyMaxVDConfig.enableExtRenderDistanceProtocol']),
            ('notickvd','com.ishland.c2me.notickvd.ModuleEntryPoint',['com.ishland.c2me.notickvd.disable'])]:
            nested = next(n for n in container.namelist() if n.startswith('META-INF/jars/c2me-fabric-'+part+'-'))
            jar = ROOT/'.build/validator'/('c2me-'+part+'.jar')
            jar.write_bytes(container.read(nested))
            code = subprocess.run(['javap','-p','-c','-classpath',str(jar),cls],check=True,capture_output=True,text=True).stdout
            require(all(s in code for s in expected_strings),'Claves C2ME ausentes: '+part)

def validate_modrinth_dependencies(projects, embedded_projects=None):
    providers = dict(embedded_projects or {})
    providers.update(projects)
    for version in projects.values():
        if version['dependencies'] is None:
            continue  # Reported explicitly as pending; actual JAR dependencies still checked.
        for dep in version['dependencies']:
            target = providers.get(dep['project_id'])
            matches = target is not None and (not dep['version_id'] or target['id'] == dep['version_id'])
            if dep['dependency_type'] == 'required':
                require(matches, 'Dependencia Modrinth incorrecta: ' + str(dep))
            elif dep['dependency_type'] == 'incompatible':
                require(not matches, 'Incompatibilidad Modrinth: ' + str(dep))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--require-publications', action='store_true', help='Exigir respuestas reales de publicación para todos los pins; requiere red o caché completa')
    args = parser.parse_args()
    require(shutil.which('java') and shutil.which('javac') and shutil.which('javap'), 'Validar requiere un JDK 17+; Minecraft requiere Java 25')
    check_index(ROOT / 'pack')
    loader = fetch(LOADER_URL)
    require(hashlib.sha1(loader).hexdigest() == fetch(LOADER_URL + '.sha1').decode().strip(), 'Hash de Loader inválido')
    engine = FabricVersions(loader)
    try:
        validate_configs()
        loader_inventory = []
        with zipfile.ZipFile(io.BytesIO(loader)) as jar:
            require(jar.testzip() is None, 'Loader corrupto')
            for name in jar.namelist():
                if name.startswith('META-INF/jars/') and name.endswith('.jar'):
                    inspect_jar(jar.read(name), 'fabric-loader!' + name, loader_inventory)
        matrix = profiles()
        all_descriptors = sorted({p for profile in matrix.values() for p in descriptors(profile)})
        sources = {}
        publication_checks = {}
        for path in all_descriptors:
            mod = tomllib.loads(path.read_text())
            require(mod.get('pin') is True, f'Versión no fijada: {path}')
            version, evidence_status = publication_or_local_pin(mod, args.require_publications)
            publication_checks[path.name] = evidence_status
            require(version['project_id'] == mod['update']['modrinth']['mod-id'], 'Proyecto incorrecto')
            require('26.3' in version['game_versions'] and 'fabric' in version['loaders'], 'Publicación incompatible')
            file = next(f for f in version['files'] if f['filename'] == mod['filename'])
            require(file['url'] == mod['download']['url'], 'URL diferente de la publicación')
            data = fetch(file['url'])
            for algorithm, expected in file['hashes'].items():
                require(hashlib.new(algorithm, data).hexdigest() == expected, f'Hash de JAR inválido: {path.name}')
            require(hashlib.new(mod['download']['hash-format'], data).hexdigest() == mod['download']['hash'], 'Hash packwiz inválido')
            require(len(data) == file['size'], 'Tamaño de JAR incorrecto')
            inventory = []
            inspect_jar(data, mod['filename'], inventory)
            sources[path] = (mod, file, data, version, inventory)
        supplied_sha512 = validate_sha512_evidence(sources)
        for name in supplied_sha512:
            if 'pending' in publication_checks[name]:
                publication_checks[name] = 'published_sha512_supplied_by_user_'+supplied_sha512[name]['evidence_date']+'; full_publication_metadata_pending'
        reports = {}
        for name, profile in matrix.items():
            check_index(ROOT / '.build' / name)
            selected = {('mods/'+sources[p][0]['filename']):sources[p] for p in descriptors(profile)}
            inventory = loader_inventory.copy()
            for source in selected.values():
                inventory.extend(source[4])
            available, chosen, alternatives = resolve(inventory, engine)
            projects = {source[3]['project_id']:source[3] for source in selected.values()}
            embedded_projects = {}
            # Solo acreditar una publicación integrada si sus bytes coinciden con hashes publicados.
            publication_path = ROOT/'docs/research/embedded-placeholder-alpha.4.json'
            if publication_path.exists():
                publication = json.loads(publication_path.read_text())
                expected_hashes = {f['hashes']['sha512'] for f in publication['files']}
                matches = [rec for rec in inventory if '!' in rec['origin'] and rec['jar_sha512'] in expected_hashes]
                if matches:
                    embedded_projects[publication['project_id']] = publication
            validate_modrinth_dependencies(projects, embedded_projects)
            expected_configs = configs(profile)
            path = ROOT / 'dist' / f'Lumina-Optimized-{pack_version()}-{name}.mrpack'
            with zipfile.ZipFile(path) as archive:
                require(archive.testzip() is None, 'Exportación corrupta')
                files = [n for n in archive.namelist() if not n.endswith('/')]
                require(len(files)==len(set(files)), 'Archivos duplicados en ZIP')
                expected = {'modrinth.index.json'} | {'overrides/'+p for p in expected_configs}
                require(set(files)==expected, 'Overrides inesperados: '+str(set(files)^expected))
                for config, data in expected_configs.items():
                    require(archive.read('overrides/'+config)==data, 'Configuración diferente en ZIP')
                manifest = json.loads(archive.read('modrinth.index.json'))
                require(manifest['formatVersion']==1 and manifest['game']=='minecraft', 'Formato incorrecto')
                require(manifest['versionId']==pack_version() and manifest['name']==profile['name'], 'Versión/nombre incorrecto')
                require(manifest['dependencies']=={'minecraft':'26.3','fabric-loader':'0.19.5'}, 'Dependencias de exportación incorrectas')
                require(len(manifest['files'])==len(selected) and {f['path'] for f in manifest['files']}==set(selected), 'Contenido incorrecto')
                for entry in manifest['files']:
                    require(not PurePosixPath(entry['path']).is_absolute() and '..' not in PurePosixPath(entry['path']).parts, 'Ruta insegura')
                    mod, file, data, _, _ = selected[entry['path']]
                    require(entry['downloads']==[file['url']] and entry['fileSize']==len(data), 'Descarga incorrecta')
                    require({'sha1','sha512'}<=set(entry['hashes']), 'Faltan hashes')
                    for algorithm, expected_hash in entry['hashes'].items():
                        require(hashlib.new(algorithm,data).hexdigest()==expected_hash, 'Hash de exportación inválido')
                    require(entry['env']=={'client':'required','server':'unsupported' if mod['side']=='client' else 'required'}, 'Lado incorrecto')
            external_dependencies = {'fabric-api.pw.toml','cloth-config.pw.toml','resourceful-config.pw.toml','zconfig.pw.toml'}
            external_count = sum(p.name in external_dependencies for p in descriptors(profile))
            nested_records = [rec for rec in inventory if '!' in rec['origin'] and not rec['origin'].startswith('fabric-loader!')]
            nested_selected = [rec for rec in chosen.values() if '!' in rec['origin'] and not rec['origin'].startswith('fabric-loader!')]
            reports[name] = {'files':len(selected),
                             'principal_mods':len(selected)-external_count,
                             'external_dependency_jars':external_count,
                             'integrated_module_occurrences':len(nested_records),
                             'integrated_distinct_ids':len({rec['id'] for rec in nested_records}),
                             'integrated_selected_ids':len(nested_selected),
                             'loader_provided_modules':{rec['id']:rec['version'] for rec in loader_inventory},
                             'modrinth_dependencies_satisfied_by_embedded':{key:value['id'] for key,value in embedded_projects.items()}, 'resolved':available,
                             'selected_jar_origins':{k:v['origin'] for k,v in chosen.items()},
                             'nested_alternatives':alternatives,
                             'config_sha256':{p:hashlib.sha256(data).hexdigest() for p,data in expected_configs.items()},
                             'mrpack_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
        for descriptor, evidence in supplied_sha512.items():
            evidence['exports_checked'] = [name for name,profile in matrix.items() if descriptor in {p.name for p in descriptors(profile)}]
            evidence['status'] = 'matched_local_jar_packwiz_and_all_exports_containing_mod'
        checksums = ROOT / 'dist' / f'SHA256SUMS-{pack_version()}'
        checked = set()
        for line in checksums.read_text().splitlines():
            expected, filename = line.split('  ',1)
            require(hashlib.sha256((ROOT/'dist'/filename).read_bytes()).hexdigest()==expected,'SHA256SUMS inválido')
            checked.add(filename)
        require(checked=={f'Lumina-Optimized-{pack_version()}-{name}.mrpack' for name in matrix}, 'Faltan checksums')
        with zipfile.ZipFile(ROOT/'dist'/f'Lumina-Optimized-{pack_version()}-test-packages.zip') as bundle:
            require(bundle.testzip() is None and set(bundle.namelist())==checked|{checksums.name}, 'Bundle incorrecto')
            for name in bundle.namelist():
                require(bundle.read(name)==(ROOT/'dist'/name).read_bytes(), 'Bundle desactualizado')
        history_assets = {}
        for release in ('alpha.1','alpha.2','alpha.3'):
            history_assets[release] = {}
            for line in (ROOT/'docs/history'/release/'SHA256SUMS').read_text().splitlines():
                expected, filename = line.split('  ',1)
                original = ROOT/'dist'/filename
                if original.exists():
                    require(hashlib.sha256(original.read_bytes()).hexdigest()==expected, release+' modificada')
                    history_assets[release][filename] = 'hash verificado; intacto'
                else:
                    history_assets[release][filename] = 'no presente localmente; hash histórico conservado'
        report = {'scope':'Validación estática con VersionPredicate de Fabric 0.19.5; selección del candidato más reciente de cada módulo anidado. No ejecuta el resolvedor completo, mixins, launcher, Minecraft ni benchmarks.',
                  'version':pack_version(), 'loader_sha256':hashlib.sha256(loader).hexdigest(),
                  'publication_checks':publication_checks,
                  'publication_metadata_pending':[name for name,status in publication_checks.items() if 'pending' in status],
                  'supplied_publication_sha512':supplied_sha512,
                  'publication_hashes_pending':[name for name,status in publication_checks.items() if 'pending' in status and name not in supplied_sha512],
                  'historical_assets':history_assets,
                  'minecraft_tests':{'import':'pending','startup':'pending','stability':'pending','performance':'pending'},
                  'jar_metadata':{p.name:sources[p][4] for p in all_descriptors}, 'variants':reports}
        (ROOT/'docs/validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
        print(f'OK: {len(reports)} paquetes, JAR anidados, predicados Fabric, configs, hashes y alpha.1/alpha.2/alpha.3 preservadas; hashes publicados pendientes: {len(report["publication_hashes_pending"])}; metadatos completos pendientes: {len(report["publication_metadata_pending"])}')
    finally:
        engine.close()

if __name__ == '__main__':
    main()
