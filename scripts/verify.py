"""Validación estática. Usa VersionPredicate de Fabric; no arranca Minecraft."""
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tomllib
import urllib.request
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
        request = urllib.request.Request(url, headers={'User-Agent': 'Lumina-Optimized/0.1.0-alpha.3'})
        with urllib.request.urlopen(request, timeout=60) as response:
            path.write_bytes(response.read())
    return path.read_bytes()

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
        metadata = json.loads(jar.read('fabric.mod.json'))
        inventory.append({'origin': origin, 'id': metadata['id'], 'version': metadata['version'],
                          'jar_sha512': hashlib.sha512(data).hexdigest(),
                          'depends': metadata.get('depends', {}), 'breaks': metadata.get('breaks', {}),
                          'conflicts': metadata.get('conflicts', {}), 'provides': metadata.get('provides', []),
                          'environment': metadata.get('environment', '*')})
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

def validate_modrinth_dependencies(projects):
    for version in projects.values():
        for dep in version['dependencies']:
            target = projects.get(dep['project_id'])
            matches = target is not None and (not dep['version_id'] or target['id'] == dep['version_id'])
            if dep['dependency_type'] == 'required':
                require(matches, 'Dependencia Modrinth incorrecta: ' + str(dep))
            elif dep['dependency_type'] == 'incompatible':
                require(not matches, 'Incompatibilidad Modrinth: ' + str(dep))

def main():
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
        for path in all_descriptors:
            mod = tomllib.loads(path.read_text())
            require(mod.get('pin') is True, f'Versión no fijada: {path}')
            version = json.loads(fetch('https://api.modrinth.com/v2/version/' + mod['update']['modrinth']['version']))
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
        reports = {}
        for name, profile in matrix.items():
            check_index(ROOT / '.build' / name)
            selected = {('mods/'+sources[p][0]['filename']):sources[p] for p in descriptors(profile)}
            inventory = loader_inventory.copy()
            for source in selected.values():
                inventory.extend(source[4])
            available, chosen, alternatives = resolve(inventory, engine)
            projects = {source[3]['project_id']:source[3] for source in selected.values()}
            validate_modrinth_dependencies(projects)
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
            reports[name] = {'files':len(selected), 'resolved':available,
                             'selected_jar_origins':{k:v['origin'] for k,v in chosen.items()},
                             'nested_alternatives':alternatives,
                             'config_sha256':{p:hashlib.sha256(data).hexdigest() for p,data in expected_configs.items()},
                             'mrpack_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
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
        for release in ('alpha.1','alpha.2'):
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
                  'historical_assets':history_assets,
                  'minecraft_tests':{'import':'pending','startup':'pending','stability':'pending','performance':'pending'},
                  'jar_metadata':{p.name:sources[p][4] for p in all_descriptors}, 'variants':reports}
        (ROOT/'docs/validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
        print(f'OK: {len(reports)} paquetes, JAR anidados, predicados Fabric, configs, hashes y alpha.1/alpha.2 preservadas')
    finally:
        engine.close()

if __name__ == '__main__':
    main()
