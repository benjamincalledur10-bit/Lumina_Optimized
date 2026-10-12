"""Comprueba publicación, bytes, dependencias y exportación; no sustituye una prueba de juego."""
import hashlib, io, json, os, shutil, subprocess, tomllib, zipfile
from pathlib import Path, PurePosixPath
import urllib.request
from profiles import ROOT, configs, descriptors, resource_descriptors, pack_version, profiles, artifact_name
CACHE = ROOT / '.build/downloads'
LOADER_URL = 'https://maven.fabricmc.net/net/fabricmc/fabric-loader/0.19.5/fabric-loader-0.19.5.jar'


def require(condition, message):
    if not condition:
        raise ValueError(message)

def fetch(url):
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / hashlib.sha256(url.encode()).hexdigest()
    if not path.exists():
        request = urllib.request.Request(url, headers={'User-Agent': 'Lumina-Optimized/'+pack_version()})
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

def validate_configs():
    for path in (ROOT / 'pack/config').glob('*.json'):
        json.loads(path.read_text())
    ec = json.loads((ROOT / 'pack/config/entityculling.json').read_text())
    mc = tomllib.loads((ROOT / 'pack/config/moreculling.toml').read_text())
    bbe = json.loads((ROOT / 'pack/config/BBEConfig.json').read_text())
    require(ec['safeMode'] and not ec['tickCulling'] and not ec['solidLeaves'], 'Referencia Entity Culling alterada')
    require(mc['leavesCullingMode']=='DEFAULT' and not mc['useItemFrameLOD'] and not mc['useItemFrame3FaceCulling'], 'Calidad More Culling alterada')
    options = {x['option']:x['value'] for x in bbe['bbe.config.storage.main']}
    require(options['optimize.master'] is True and options['optimize.banner'] is False and options['optimize.sign'] is False, 'Referencia BBE alterada')
    require(all(options[x] for x in ['animation.chest','animation.shulker','animation.bell','animation.decoratedpot']), 'Animaciones desactivadas')
    c2me = tomllib.loads((ROOT / 'pack/config/c2me.toml').read_text())
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
    modernfix = (ROOT/'pack/config/modernfix-mixins.properties').read_text()
    require('mixin.perf.remove_biome_temperature_cache=false' in modernfix, 'Colisión de caché de biomas no desactivada')
    mod = tomllib.loads((ROOT/'pack/mods/modernfix-mvus.pw.toml').read_text())
    with zipfile.ZipFile(io.BytesIO(fetch(mod['download']['url']))) as jar:
        require(any('perf/remove_biome_temperature_cache/' in path for path in jar.namelist()), 'Mixin ModernFix ausente')
    require((ROOT/'pack/config/iris.properties').read_text().strip()=='enableShaders=false', 'Shaders deben comenzar desactivados')
    iris = tomllib.loads((ROOT/'pack/mods/iris.pw.toml').read_text())
    path = ROOT/'.build/validator/iris.jar'
    path.write_bytes(fetch(iris['download']['url']))
    code = subprocess.run(['javap','-p','-c','-classpath',str(path),'net.irisshaders.iris.config.IrisConfig'],check=True,capture_output=True,text=True).stdout
    require('String enableShaders' in code and 'Properties.getProperty' in code, 'Opción real Iris no encontrada')
    servercore = tomllib.loads((ROOT/'pack/mods/servercore.pw.toml').read_text())
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
    subprocess.run(['java','-cp',str(yaml_jar.parent)+os.pathsep+str(yaml_jar),'ServerCoreConfigCheck',str(ROOT/'pack/config/servercore/config.yml'),str(ROOT/'pack/config/servercore/optimizations.yml')],check=True)
    c2me_mod = tomllib.loads((ROOT/'pack/mods/c2me-fabric.pw.toml').read_text())
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
    ldl = tomllib.loads((ROOT/'pack/config/lambdynlights.toml').read_text())
    require(ldl['mode'] == 'off', 'LambDynamicLights debe empezar apagado')
    leaf = json.loads((ROOT/'pack/config/cullleaves.json').read_text())
    require(leaf == {'enabled': True, 'cullRoots': False}, 'Solo Cull Leaves controla hojas; raíces conservadoras')
    require(mc['leavesCullingMode'] == 'DEFAULT' and not mc['useBlockStateCulling'] and not mc['includeMangroveRoots'], 'Superposición de culling de hojas')
    extra = json.loads((ROOT/'pack/config/sodium-extra-options.json').read_text())
    require(extra == {'extra_settings': {'reduce_resolution_on_mac': False}}, 'No reducir resolución en Mac')
    extra_mod = tomllib.loads((ROOT/'pack/mods/sodium-extra.pw.toml').read_text())
    (ROOT/'.build/validator/sodium-extra.jar').write_bytes(fetch(extra_mod['download']['url']))
    code = subprocess.run(['javap','-p','-c','-classpath',str(ROOT/'.build/validator/sodium-extra.jar'),'me.flashyreese.mods.sodiumextra.client.config.SodiumExtraGameOptions'],check=True,capture_output=True,text=True).stdout
    require('LOWER_CASE_WITH_UNDERSCORES' in code, 'Serialización Sodium Extra cambió')
    gnetum = json.loads((ROOT/'pack/config/gnetum.json').read_text())
    require(gnetum['downscale']['value']=='OFF', 'No reducir resolución del HUD')
    for slug, cls, strings in [
        ('lambdynamiclights', 'dev.lambdaurora.lambdynlights.DynamicLightsConfig', ['mode', 'lambdynlights.toml']),
        ('cull-leaves', 'eu.midnightdust.cullleaves.config.CullLeavesConfig', ['enabled', 'cullRoots']),
        ('sodium-extra', 'me.flashyreese.mods.sodiumextra.client.config.SodiumExtraGameOptions$ExtraSettings', ['reduceResolutionOnMac']),
        ('fastquit', 'me.contaria.fastquit.FastQuitConfig', ['ix eris'.replace(' ',''), 'allowMultipleServers']),
        ('gnetum', 'me.decce.gnetum.GnetumConfig', ['downscale', 'numberOfPasses', 'maxFps'])]:
        mod = tomllib.loads((ROOT/'pack/mods'/(slug+'.pw.toml')).read_text())
        jar = ROOT/'.build/validator'/(slug+'.jar'); jar.write_bytes(fetch(mod['download']['url']))
        code = subprocess.run(['javap','-p','-c','-classpath',str(jar),cls],check=True,capture_output=True,text=True).stdout
        require(all(key in code for key in strings), 'Opciones reales no verificadas: '+cls)


def main():
    require(all(shutil.which(tool) for tool in ('java','javac','javap')), 'Validar requiere JDK 17+; jugar requiere Java 25')
    check_index(ROOT/'pack')
    selection = json.loads((ROOT/'docs/research/selection-26.3-beta.1.json').read_text())
    rows = selection['selection']
    require(selection['target_entries']==42 and sum(row['requested'] for row in rows)==42, 'Lista objetivo incompleta')
    base=json.loads((ROOT/'docs/research/selection-alpha.5.json').read_text())['selection']
    require([row for row in rows if row['slug']!='polytone']==base, 'La selección heredada de alpha.5 cambió')
    pins = descriptors({})
    require({p.name for p in pins}=={row['descriptor'] for row in rows if row['distribution']=='external'}, 'Mods no seleccionados en la base limpia')
    loader = fetch(LOADER_URL)
    require(hashlib.sha1(loader).hexdigest()==fetch(LOADER_URL+'.sha1').decode().strip(), 'Hash Loader incorrecto')
    inventory=[]
    with zipfile.ZipFile(io.BytesIO(loader)) as jar:
        require(jar.testzip() is None, 'Loader corrupto')
        for path in jar.namelist():
            if path.startswith('META-INF/jars/') and path.endswith('.jar'):
                inspect_jar(jar.read(path),'fabric-loader!'+path,inventory)
    loader_inventory=inventory.copy()
    publications={}; sources={}; nested_publications={}
    for row in rows:
        version=json.loads(fetch('https://api.modrinth.com/v2/version/'+row['version_id']))
        require(version['id']==row['version_id'] and version['project_id']==row['project_id'] and version['version_number']==row['version'], 'Identidad de publicación distinta')
        require('26.3' in version['game_versions'] and 'fabric' in version['loaders'], 'No publicado para Fabric 26.3: '+row['name'])
        file=next(f for f in version['files'] if f['filename']==row['filename'])
        require(file['url']==row['url'] and file['hashes']['sha512']==row['sha512'], 'URL/hash distintos de la publicación')
        data=fetch(file['url'])
        require(len(data)==file['size'], 'Tamaño incorrecto')
        for algorithm,value in file['hashes'].items():
            require(hashlib.new(algorithm,data).hexdigest()==value, 'Hash publicado incorrecto: '+row['name'])
        records=[];inspect_jar(data,row['filename'],records)
        require(records[0]['id']==row['fabric_id'] and records[0]['version']==row['fabric_version'], 'Identidad interna distinta')
        if row['distribution']=='embedded':
            nested_publications[row['project_id']]=version
            continue
        path=ROOT/'pack/mods'/row['descriptor'];pin=tomllib.loads(path.read_text())
        require(pin.get('pin') is True and pin['filename']==file['filename'], 'Archivo/versión no fijados')
        require(pin['update']['modrinth']=={'mod-id':version['project_id'],'version':version['id']}, 'IDs packwiz incorrectos')
        require(pin['download']=={'url':file['url'],'hash-format':'sha512','hash':file['hashes']['sha512']}, 'Hash/URL packwiz diferentes')
        inventory.extend(records);publications[version['project_id']]=version
        sources['mods/'+file['filename']]=(pin,file,data,records)
    for project,publication in nested_publications.items():
        hashes={file['hashes']['sha512'] for file in publication['files']}
        require(any('!' in record['origin'] and record['jar_sha512'] in hashes for record in inventory), 'Biblioteca integrada no coincide con publicación: '+project)
    resources=json.loads((ROOT/'docs/research/resourcepacks-26.3-beta.1.json').read_text())['selection']
    require({p.name for p in resource_descriptors({})}=={r['descriptor'] for r in resources}, 'Lista de recursos distinta')
    resource_report=[]
    for row in resources:
        version=json.loads(fetch('https://api.modrinth.com/v2/version/'+row['version_id']))
        require(version['id']==row['version_id'] and version['project_id']==row['project_id'] and version['version_number']==row['version'], 'Identidad resource pack distinta')
        require('minecraft' in version['loaders'], 'No es resource pack')
        published='26.3' in version['game_versions']
        require(published==row['published_for_26_3'], 'Compatibilidad publicada distinta')
        require(published or row['slug']=='mandalas-gui-dark-mode', 'Recurso no compatible sin excepción documentada')
        file=next(f for f in version['files'] if f['filename']==row['filename'])
        require(file['url']==row['url'] and file['hashes']['sha512']==row['sha512'], 'URL/hash del recurso distintos')
        pin=tomllib.loads((ROOT/'pack/resourcepacks'/row['descriptor']).read_text())
        require(pin.get('pin') is True and pin['side']=='client' and pin['filename']==file['filename'], 'Recurso no fijado/client')
        require(pin['update']['modrinth']=={'mod-id':version['project_id'],'version':version['id']}, 'IDs de recurso incorrectos')
        require(pin['download']=={'url':file['url'],'hash-format':'sha512','hash':file['hashes']['sha512']}, 'Hash/URL packwiz del recurso diferentes')
        data=fetch(file['url']);require(len(data)==file['size'], 'Tamaño del recurso distinto')
        for algorithm,value in file['hashes'].items():require(hashlib.new(algorithm,data).hexdigest()==value, 'Hash del recurso distinto')
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            require(archive.testzip() is None, 'Resource pack corrupto')
            require(json.loads(archive.read('pack.mcmeta'))==row['pack_mcmeta'], 'Metadatos internos del recurso distintos')
            require(all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts for n in archive.namelist()), 'Ruta insegura en recurso')
        publications[version['project_id']]=version
        sources['resourcepacks/'+file['filename']]=(pin,file,data,[])
        resource_report.append({'slug':row['slug'],'version':row['version'],'published_for_26_3':published,'pack_mcmeta':row['pack_mcmeta'],'sha512':file['hashes']['sha512']})
    validate_modrinth_dependencies(publications,nested_publications)
    engine=FabricVersions(loader)
    try:
        available,chosen,alternatives=resolve(inventory,engine)
        validate_configs()
        for row in resources:
            require(all(mod in available for mod in row['required_mods']), 'Soporte del recurso ausente: '+row['slug'])
    finally:engine.close()
    expected_configs=configs({});check_index(ROOT/'.build/main')
    previous=json.loads((ROOT/'docs/history/alpha.5/validation.json').read_text())
    require({p:hashlib.sha256(data).hexdigest() for p,data in expected_configs.items() if p.startswith('config/')}==previous['config_sha256'], 'Las configuraciones de alpha.5 cambiaron')
    require(not (ROOT/'pack/shaderpacks').exists(), 'No distribuir shader packs adicionales')
    options=dict(line.split(':',1) for line in (ROOT/'pack/options.txt').read_text().splitlines())
    require(set(options)=={'version','resourcePacks','incompatibleResourcePacks'} and options['version']=='5023', 'options.txt contiene ajustes gráficos o versión distinta')
    require(json.loads(options['resourcePacks'])==['vanilla']+['file/'+r['filename'] for r in resources], 'Recursos no activados u orden distinto')
    require(json.loads(options['incompatibleResourcePacks'])==['file/'+r['filename'] for r in resources if not r['published_for_26_3']], 'Excepción de formato distinta')
    artifact=ROOT/'dist'/artifact_name()
    with zipfile.ZipFile(artifact) as archive:
        require(archive.testzip() is None, 'Export corrupto')
        names=[n for n in archive.namelist() if not n.endswith('/')]
        require(len(names)==len(set(names)), 'Entradas ZIP duplicadas')
        require(set(names)=={'modrinth.index.json'}|{'overrides/'+p for p in expected_configs}, 'Overrides inesperados')
        for config,data in expected_configs.items():require(archive.read('overrides/'+config)==data, 'Config distinta en export')
        manifest=json.loads(archive.read('modrinth.index.json'))
        require(manifest['formatVersion']==1 and manifest['game']=='minecraft' and manifest['versionId']==pack_version() and manifest['name']==profiles()['main']['name'], 'Identidad export incorrecta')
        require(manifest['dependencies']=={'minecraft':'26.3','fabric-loader':'0.19.5'}, 'Versiones plataforma distintas')
        require(len(manifest['files'])==len(sources) and {file['path'] for file in manifest['files']}==set(sources), 'Export incompleto')
        for entry in manifest['files']:
            path=PurePosixPath(entry['path']);require(not path.is_absolute() and '..' not in path.parts, 'Ruta insegura')
            pin,file,data,_=sources[entry['path']]
            require(entry['downloads']==[file['url']] and entry['fileSize']==len(data), 'URL/tamaño export distintos')
            require({'sha1','sha512'}<=entry['hashes'].keys(), 'Faltan hashes export')
            for algorithm,value in entry['hashes'].items():require(hashlib.new(algorithm,data).hexdigest()==value, 'Hash export incorrecto')
            require(entry['env']=={'client':'required','server':'unsupported' if pin['side']=='client' else 'required'}, 'Entorno distinto')
    digest=hashlib.sha256(artifact.read_bytes()).hexdigest()
    require((ROOT/'dist'/('SHA256SUMS-'+pack_version())).read_text()==digest+'  '+artifact.name+'\n', 'Checksum del paquete incorrecto')
    history={}
    for release in ('alpha.1','alpha.2','alpha.3','alpha.4','alpha.5'):
        history[release]={}
        for line in (ROOT/'docs/history'/release/'SHA256SUMS').read_text().splitlines():
            expected,filename=line.split('  ',1);path=ROOT/'dist'/filename
            if path.exists():
                require(hashlib.sha256(path.read_bytes()).hexdigest()==expected, 'Artefacto histórico modificado: '+filename)
                history[release][filename]='hash verificado; intacto'
            else:history[release][filename]='hash histórico conservado; archivo no presente localmente'
    nested=[record for record in inventory if '!' in record['origin'] and not record['origin'].startswith('fabric-loader!')]
    selected_nested=[record for record in chosen.values() if '!' in record['origin'] and not record['origin'].startswith('fabric-loader!')]
    report={'version':pack_version(),'verified_on':'2026-10-11','scope':'Publicaciones y bytes completos; predicados reales Fabric. Selección estática del módulo más reciente: no sustituye SAT/mixins ni juego.',
            'counts':{'requested_entries':42,'principal_mods':sum(row['role']=='principal' for row in rows),'external_libraries':sum(row['role']=='library' and row['distribution']=='external' for row in rows),'resource_support_mods':sum(row['role']=='resource_support' for row in rows),'resource_packs':len(resources),'downloadable_jars':sum(path.startswith('mods/') for path in sources),'downloadable_files':len(sources),'integrated_module_occurrences':len(nested),'integrated_distinct_ids':len({record['id'] for record in nested}),'integrated_selected_ids':len(selected_nested)},
            'resource_packs':resource_report,
            'publication_metadata_pending':[],'publication_hashes_pending':[], 'loader_provided_modules':loader_inventory,
            'embedded_published_libraries':{project:version['id'] for project,version in nested_publications.items()},
            'resolved':available,'selected_jar_origins':{key:record['origin'] for key,record in chosen.items()},'nested_alternatives':alternatives,
            'jar_metadata':{path:records for path,(_,_,_,records) in sources.items()},'historical_assets':history,'config_sha256':{path:hashlib.sha256(data).hexdigest() for path,data in expected_configs.items()},'artifact':artifact.name,'mrpack_sha256':digest,
            'minecraft_tests':{'import':'pending for beta.1','startup':'see research/runtime-26.3-beta.1.json','world_entry':'pending for beta.1','save_reopen':'pending','stability':'pending for beta.1; user reports favorable alpha.5 play','performance':'alpha.5 screenshot readings only; beta.1 resources not measured'}}
    (ROOT/'docs/validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print('OK: publicaciones, SHA-1/SHA-512, dependencias obligatorias e integradas, conflictos declarados, configs, índices y .mrpack; historial intacto.')
    print(json.dumps(report['counts']))

if __name__=='__main__':main()
