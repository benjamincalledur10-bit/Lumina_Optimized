"""Regresiones de composición y resolución; no son benchmarks de Minecraft."""
import argparse
import json
from pathlib import Path
import subprocess
import unittest
from profiles import ROOT, configs, descriptors, profiles
from verify import FabricVersions, LOADER_URL, fetch, resolve

def record(mod_id, version, depends=None):
    return {'id':mod_id, 'version':version, 'origin':mod_id+'.jar', 'depends':depends or {},
            'breaks':{}, 'conflicts':{}, 'provides':[]}

class CompositionTests(unittest.TestCase):
    def test_isolated_mods_change_only_one_descriptor(self):
        matrix = profiles()
        for name, mod in [('entity','entityculling'),('more','moreculling'),('bbe','better-block-entities')]:
            for suffix in ('','-shaders'):
                control = {p.name for p in descriptors(matrix['dependencies'+suffix])}
                trial = {p.name for p in descriptors(matrix[name+suffix])}
                self.assertEqual(trial-control, {mod+'.pw.toml'})
                self.assertEqual(control-trial, set())

    def test_bbe_activation_changes_one_option(self):
        matrix = profiles()
        for control, trial in [('core','core-bbe-enabled'),('shaders','shaders-bbe-enabled')]:
            self.assertEqual(descriptors(matrix[control]),descriptors(matrix[trial]))
            a, b = configs(matrix[control]),configs(matrix[trial])
            for name in a:
                if name!='config/BBEConfig.json':
                    self.assertEqual(a[name],b[name])
            before, after = json.loads(a['config/BBEConfig.json']),json.loads(b['config/BBEConfig.json'])
            options_before = {x['option']:x['value'] for x in before['bbe.config.storage.main']}
            options_after = {x['option']:x['value'] for x in after['bbe.config.storage.main']}
            delta = {key for key in options_before if options_before[key]!=options_after[key]}
            self.assertEqual(delta,{'optimize.master'})
            self.assertTrue(options_after['optimize.master'])

    def test_c2me_is_a_single_addition(self):
        matrix = profiles()
        for control, trial in [('core','c2me'),('shaders','c2me-shaders')]:
            a = {p.name for p in descriptors(matrix[control])}
            b = {p.name for p in descriptors(matrix[trial])}
            self.assertEqual(b-a,{'c2me-fabric.pw.toml'})
            self.assertEqual(a-b,set())
            old, new = configs(matrix[control]),configs(matrix[trial])
            self.assertEqual(set(new)-set(old),{'config/c2me.toml'})
            for key in old:
                self.assertEqual(old[key],new[key])

    def test_baseline_does_not_change_reference_configs(self):
        matrix = profiles()
        self.assertEqual(len(descriptors(matrix['baseline'])),4)
        self.assertEqual(configs(matrix['baseline']),{})
        self.assertEqual(configs(matrix['dependencies']),{})

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
