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
    def test_candidates_are_isolated(self):
        matrix = profiles()
        for control, trial, mod in [('baseline','bad','badoptimizations'),('resourceful-control','structure','structure-layout-optimizer'),('zconfig-control','fastnoise','zfastnoise')]:
            a={p.name for p in descriptors(matrix[control])}; b={p.name for p in descriptors(matrix[trial])}
            self.assertEqual(b-a,{mod+'.pw.toml'}); self.assertFalse(a-b)
    def test_all_profiles_preserve_bbe_and_reference(self):
        reference=configs(profiles()['baseline'])
        for profile in profiles().values():
            actual=configs(profile)
            for key,value in reference.items(): self.assertEqual(actual[key],value)
            options={x['option']:x['value'] for x in json.loads(actual['config/BBEConfig.json'])['bbe.config.storage.main']}
            self.assertTrue(options['optimize.master'])
    def test_baseline_matches_alpha2_bbe_package(self):
        import zipfile, tomllib
        historical=json.loads((ROOT/'docs/history/alpha.2/profiles.json').read_text())['core-bbe-enabled']
        self.assertEqual(descriptors(historical),descriptors(profiles()['baseline']))
        self.assertEqual(configs(historical),configs(profiles()['baseline']))
        path=ROOT/'dist/Lumina-Optimized-0.1.0-alpha.2-core-bbe-enabled.mrpack'
        if path.exists():
            with zipfile.ZipFile(path) as z:
                for key,value in configs(historical).items(): self.assertEqual(z.read('overrides/'+key),value)
                current=ROOT/'dist/Lumina-Optimized-0.1.0-alpha.3-baseline.mrpack'
                if current.exists():
                    with zipfile.ZipFile(current) as trial:
                        before=json.loads(z.read('modrinth.index.json'))
                        after=json.loads(trial.read('modrinth.index.json'))
                        self.assertEqual(before['dependencies'],after['dependencies'])
                        self.assertEqual(sorted(before['files'],key=lambda x:x['path']),sorted(after['files'],key=lambda x:x['path']))
    def test_trio_is_union(self):
        matrix=profiles(); union=set()
        for name in ['bad','structure','fastnoise']: union.update(p.name for p in descriptors(matrix[name]))
        self.assertEqual(union,{p.name for p in descriptors(matrix['core'])})
    def test_gnetum_factorial(self):
        matrix=profiles()
        for control,trial in [('baseline','gnetum'),('baseline-noif','gnetum-noif'),('baseline-shaders','gnetum-shaders')]:
            a={p.name for p in descriptors(matrix[control])}; b={p.name for p in descriptors(matrix[trial])}
            self.assertEqual(b-a,{'gnetum.pw.toml'}); self.assertFalse(a-b)
        for name in ['baseline-noif','gnetum-noif']:
            self.assertNotIn('immediatelyfast.pw.toml',{p.name for p in descriptors(matrix[name])})
    def test_c2me_separate(self):
        matrix=profiles()
        for control,trial in [('baseline','c2me'),('core','c2me-all'),('shaders','c2me-shaders')]:
            a={p.name for p in descriptors(matrix[control])}; b={p.name for p in descriptors(matrix[trial])}
            self.assertEqual(b-a,{'c2me-fabric.pw.toml'}); self.assertFalse(a-b)
    def test_deduplication_disabled(self):
        for profile in profiles().values():
            actual=configs(profile)
            if 'structure-layout-optimizer.pw.toml' in {p.name for p in descriptors(profile)}:
                self.assertIs(json.loads(actual['config/structure_layout_optimizer.jsonc'])['deduplicateShuffledTemplatePoolElementList'],False)
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
    def test_budget_hypothesis_preserves_control(self):
        # Ejecuta solo la política escalar, no temporiza renderizado ni simula chunks.
        for frame_ns in [1_000_100,8_333_333,16_666_667,33_333_333,100_000_000]:
            control = max(int(frame_ns*0.3),10_000_000)
            trial = max(int(frame_ns*0.3),2_000_000)
            self.assertLessEqual(trial,control)
            self.assertGreaterEqual(trial,2_000_000)
        self.assertEqual(max(int(16_666_667*0.3),10_000_000),10_000_000)
        self.assertEqual(max(int(16_666_667*0.3),2_000_000),5_000_000)

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
