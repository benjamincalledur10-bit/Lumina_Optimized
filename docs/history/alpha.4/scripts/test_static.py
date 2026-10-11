"""Regresiones de composición y resolución; no son benchmarks de Minecraft."""
import argparse
import json
from pathlib import Path
import subprocess
import unittest
from profiles import ROOT, configs, descriptors, profiles
from verify import FabricVersions, LOADER_URL, fetch, resolve, validate_modrinth_dependencies

def record(mod_id, version, depends=None):
    return {'id':mod_id, 'version':version, 'origin':mod_id+'.jar', 'depends':depends or {},
            'breaks':{}, 'conflicts':{}, 'provides':[]}

class CompositionTests(unittest.TestCase):
    def test_reference_is_alpha3_core(self):
        import zipfile
        old=json.loads((ROOT/'docs/history/alpha.3/profiles.json').read_text())['core']
        ref=profiles()['alpha3-reference']
        self.assertEqual(descriptors(old),descriptors(ref))
        self.assertEqual(configs(old),configs(ref))
        path=ROOT/'dist/Lumina-Optimized-0.1.0-alpha.3-core.mrpack'
        if path.exists():
            with zipfile.ZipFile(path) as z:
                for key,value in configs(ref).items(): self.assertEqual(z.read('overrides/'+key),value)
                current=ROOT/'dist/Lumina-Optimized-0.1.0-alpha.4-alpha3-reference.mrpack'
                if current.exists():
                    with zipfile.ZipFile(current) as trial:
                        before=json.loads(z.read('modrinth.index.json'));after=json.loads(trial.read('modrinth.index.json'))
                        self.assertEqual(before['files'],after['files'])
                        self.assertEqual(before['dependencies'],after['dependencies'])
    def test_bbe_and_visual_reference_preserved(self):
        reference=configs(profiles()['alpha3-reference'])
        for profile in profiles().values():
            actual=configs(profile)
            for key,value in reference.items(): self.assertEqual(actual[key],value)
            bbe=json.loads(actual['config/BBEConfig.json'])
            self.assertTrue(next(x['value'] for x in bbe['bbe.config.storage.main'] if x['option']=='optimize.master'))
            if 'better-biome-blend.pw.toml' in {p.name for p in descriptors(profile)}:
                self.assertEqual(actual['options.txt'], b'version:5023\nbiomeBlendRadius:2\nbetterBiomeBlendRadius:2\n')
            else:
                self.assertNotIn('options.txt',actual)
    def test_shaders_adds_only_iris(self):
        matrix=profiles()
        for core,shaders in [('core','shaders'),('core-conservative','shaders-conservative')]:
            a={p.name for p in descriptors(matrix[core])};b={p.name for p in descriptors(matrix[shaders])}
            self.assertEqual(b-a,{'iris.pw.toml'});self.assertFalse(a-b)
            old,new=configs(matrix[core]),configs(matrix[shaders])
            self.assertEqual(set(new)-set(old),{'config/iris.properties'})
            self.assertEqual(new['config/iris.properties'],b'enableShaders=false\n')
            for key,value in old.items():self.assertEqual(value,new[key])
    def test_optimizations_precede_utilities_visuals(self):
        matrix=profiles();a={p.name for p in descriptors(matrix['optimizations'])};b={p.name for p in descriptors(matrix['core'])}
        self.assertEqual(b-a,{x+'.pw.toml' for x in ['fast-ip-ping','crash-assistant','chunky','modmenu','bettergrassify','better-biome-blend']})
        self.assertFalse(a-b)
    def test_conservative_removes_only_experiments_and_hud_caching(self):
        matrix=profiles()
        for core,fallback in [('core','core-conservative'),('shaders','shaders-conservative')]:
            a={p.name for p in descriptors(matrix[core])};b={p.name for p in descriptors(matrix[fallback])}
            self.assertEqual(a-b,{'c2me-fabric.pw.toml','scalablelux.pw.toml','gnetum.pw.toml'});self.assertFalse(b-a)
    def test_gnetum_control_changes_one_mod(self):
        matrix=profiles();a={p.name for p in descriptors(matrix['core'])};b={p.name for p in descriptors(matrix['gnetum-control'])}
        self.assertEqual(a-b,{'gnetum.pw.toml'});self.assertFalse(b-a)
        self.assertIn('immediatelyfast.pw.toml',a & b)
    def test_no_duplicate_dependencies_or_unverified_targets(self):
        targets=json.loads((ROOT/'variants/targets-alpha.4.json').read_text())['targets']
        for profile in profiles().values():
            files={p.name for p in descriptors(profile)}
            self.assertNotIn('placeholder-api.pw.toml',files)
            self.assertNotIn('mixinextras.pw.toml',files)
            self.assertNotIn('sodium-options-api.pw.toml',files)
            for target in targets:
                if target['status']!='included':self.assertNotIn(target['slug']+'.pw.toml',files)
    def test_modernfix_collision_disabled(self):
        for profile in profiles().values():
            if 'modernfix-mvus.pw.toml' in {p.name for p in descriptors(profile)}:
                self.assertIn(b'mixin.perf.remove_biome_temperature_cache=false',configs(profile)['config/modernfix-mixins.properties'])
    def test_full_target_and_shared_worldgen_dependencies(self):
        matrix=profiles()
        self.assertEqual(len(descriptors(matrix['core'])),33)
        self.assertEqual(len(descriptors(matrix['shaders'])),34)
        for name in ['core','shaders']:
            files={p.name for p in descriptors(matrix[name])}
            self.assertTrue({x+'.pw.toml' for x in ['c2me-fabric','scalablelux','zfastnoise','zfastsurface','zconfig','krypton','servercore']} <= files)
    def test_async_logger_preserves_errors(self):
        import tomllib
        settings=tomllib.loads((ROOT/'variants/asynclogger.toml').read_text())
        self.assertFalse(settings['filtering']['enabled'])
        self.assertFalse(settings['noDebugLog'])
        self.assertFalse(settings['testPerformance'])
    def test_moreculling_real_format_preserves_agreed_settings(self):
        import tomllib
        expected=json.loads((ROOT/'pack/config/moreculling.json').read_text())
        for name,profile in profiles().items():
            actual=configs(profile)
            if name=='alpha3-reference':
                self.assertNotIn('config/moreculling.toml',actual)
            else:
                self.assertEqual(tomllib.loads(actual['config/moreculling.toml'].decode()),expected)
    def test_embedded_publication_satisfies_required_dependency(self):
        consumer={'id':'consumer-v','dependencies':[{'project_id':'embedded','version_id':'embedded-v','dependency_type':'required'}]}
        with self.assertRaisesRegex(ValueError,'Dependencia'):validate_modrinth_dependencies({'consumer':consumer})
        validate_modrinth_dependencies({'consumer':consumer},{'embedded':{'id':'embedded-v'}})
    def test_modrinth_incompatibility_rejected(self):
        projects={'a':{'id':'1','dependencies':[{'project_id':'b','version_id':None,'dependency_type':'incompatible'}]},'b':{'id':'2','dependencies':[]}}
        with self.assertRaisesRegex(ValueError,'Incompatibilidad'): validate_modrinth_dependencies(projects)

class ResolutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = FabricVersions(fetch(LOADER_URL))
    @classmethod
    def tearDownClass(cls):
        cls.engine.close()
    def test_prerelease_and_calendar_predicates(self):
        self.assertTrue(self.engine.matches('26.3','>=26.3-rc.1'))
        self.assertTrue(self.engine.matches('26.3','~26.3-'))
        self.assertTrue(self.engine.matches('0.9.2+mc26.3','>=0.9.2-beta.2'))
        self.assertFalse(self.engine.matches('0.9.2-alpha.1','>=0.9.2-beta.2'))
        self.assertFalse(self.engine.matches('26.4','~26.3.0'))
    def test_missing_dependency_is_rejected(self):
        with self.assertRaisesRegex(ValueError,'cloth-config'):
            resolve([record('moreculling','1.9.0',{'cloth-config':'>=16.0.0'})],self.engine)
    def test_higher_nested_version_is_selected(self):
        candidates = [record('renderer','17.0.14+old'), record('renderer','17.0.15+new'),
                      record('consumer','1.0.0',{'renderer':'>=17.0.15'})]
        available, _, alternatives = resolve(candidates,self.engine)
        self.assertEqual(available['renderer'],'17.0.15+new')
        self.assertEqual(len(alternatives['renderer']),2)
    def test_incompatible_newest_candidate_fails_closed(self):
        candidates = [record('renderer','17.0.14'),record('renderer','17.0.15'),
                      record('consumer','1.0.0',{'renderer':'=17.0.14'})]
        with self.assertRaisesRegex(ValueError,'renderer'):
            resolve(candidates,self.engine)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sodium-source',type=Path,help='Checkout del commit Sodium revisado para git apply --check')
    args = parser.parse_args()
    suite = unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromTestCase(cls)
                               for cls in (CompositionTests,ResolutionTests)])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    if args.sodium_source:
        source = args.sodium_source.resolve()
        # --no-index permite validar contra un checkout fuera del repositorio principal.
        subprocess.run(['git','apply','--check','--no-index',str(ROOT/'experiments/sodium-upload-budget.patch')],cwd=source,check=True)
        print('OK: parche aplica al checkout Sodium indicado')
