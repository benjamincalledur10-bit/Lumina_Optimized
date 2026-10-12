"""Regresiones de composición y del resolvedor; no mide FPS ni ejecuta Minecraft."""
import copy,json,sys,tomllib,unittest
from profiles import ROOT,configs,descriptors,profiles,resource_descriptors
from verify import FabricVersions,fetch,LOADER_URL,resolve,validate_modrinth_dependencies

class CompositionTests(unittest.TestCase):
    def test_clean_selection_and_library_counts(self):
        data=json.loads((ROOT/'docs/research/selection-26.3-beta.1.json').read_text());rows=data['selection']
        self.assertEqual(sum(row['requested'] for row in rows),42)
        self.assertEqual(sum(row['role']=='principal' for row in rows),35)
        self.assertEqual({p.name for p in descriptors({})},{r['descriptor'] for r in rows if r['distribution']=='external'})
        self.assertNotIn('scalablelux',{r['slug'] for r in rows})
        self.assertEqual([r['slug'] for r in rows if not r['requested']],['zconfig','polytone'])
        self.assertEqual([r['slug'] for r in rows if r['distribution']=='embedded'],['placeholder-api'])
    def test_single_profile_preserves_visual_reference(self):
        self.assertEqual(set(profiles()),{'main'});files=configs({})
        self.assertFalse(any(p.startswith(('shaderpacks/','resourcepacks/')) for p in files))
        options=dict(line.split(':',1) for line in files['options.txt'].decode().splitlines())
        self.assertEqual(set(options),{'version','resourcePacks','incompatibleResourcePacks'})
        resources=json.loads((ROOT/'docs/research/resourcepacks-26.3-beta.1.json').read_text())['selection']
        self.assertEqual(len(resources),4)
        self.assertEqual({p.name for p in resource_descriptors({})},{r['descriptor'] for r in resources})
        self.assertEqual(json.loads(options['resourcePacks']),['vanilla']+['file/'+r['filename'] for r in resources])
        self.assertEqual(json.loads(options['incompatibleResourcePacks']),['file/'+r['filename'] for r in resources if not r['published_for_26_3']])
        bbe=json.loads(files['config/BBEConfig.json']);options={x['option']:x['value'] for x in bbe['bbe.config.storage.main']}
        self.assertTrue(options['optimize.master']);self.assertTrue(all(options[k] for k in ('animation.chest','animation.shulker','animation.bell','animation.decoratedpot')))
        self.assertEqual(files['config/iris.properties'].strip(),b'enableShaders=false')
        self.assertEqual(tomllib.loads(files['config/lambdynlights.toml'].decode())['mode'],'off')
        more=tomllib.loads(files['config/moreculling.toml'].decode());self.assertEqual(more['leavesCullingMode'],'DEFAULT');self.assertFalse(more['useBlockStateCulling'])
    def test_publication_exact_dependency_requires_exact_version(self):
        selected={'sodium':{'id':'stable','dependencies':[]},'iris':{'id':'iris','dependencies':[{'project_id':'sodium','version_id':'stable','dependency_type':'required'}]}}
        validate_modrinth_dependencies(selected)
        wrong=copy.deepcopy(selected);wrong['sodium']['id']='alpha'
        with self.assertRaises(ValueError):validate_modrinth_dependencies(wrong)

class ResolverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.engine=FabricVersions(fetch(LOADER_URL))
    @classmethod
    def tearDownClass(cls):cls.engine.close()
    def mod(self,id,version='1.0.0',**fields):return {'id':id,'version':version,'depends':{},'breaks':{},'conflicts':{},'provides':[],**fields}
    def test_nested_highest_version_and_aliases(self):
        available,chosen,alternatives=resolve([self.mod('lib','1.0.0'),self.mod('lib','2.0.0',provides=['old-lib']),self.mod('consumer',depends={'old-lib':'^2.0.0'})],self.engine)
        self.assertEqual(chosen['lib']['version'],'2.0.0');self.assertIn('lib',alternatives)
    def test_rejects_missing_requirement(self):
        with self.assertRaisesRegex(ValueError,'Dependencia no resuelta'):resolve([self.mod('consumer',depends={'missing':'*'})],self.engine)
    def test_rejects_declared_break(self):
        with self.assertRaisesRegex(ValueError,'Incompatibilidad'):resolve([self.mod('a',breaks={'b':'>=1'}),self.mod('b')],self.engine)
    def test_rejects_declared_soft_conflict(self):
        with self.assertRaisesRegex(ValueError,'Conflictos'):resolve([self.mod('a',conflicts={'b':'*'}),self.mod('b')],self.engine)

if __name__=='__main__':unittest.main()
