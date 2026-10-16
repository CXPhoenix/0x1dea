"""PB-01–06 public job CLI/system-boundary tests, not Actions capability evidence."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from article_publication import test_staging_sync as fixtures

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT/'scripts/publication-job.py'


class JobInputTests(unittest.TestCase):
    def setUp(self):
        self.fixture = fixtures.StagingSyncTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        f = self.fixture
        self.directory = f.root
        self.state = self.directory/'durable-state'
        self.state.mkdir(mode=0o700)
        self.state_identity = self.state/'identity.json'
        self.state_identity.write_text(json.dumps({'version':1,'repository':'owner/example','store_id':'a'*64})+'\n')
        self.state_identity.chmod(0o400)
        policy = (ROOT/'maintenance/publication-workflow/engineering-v1.json').read_bytes()
        f.put('maintenance/publication-workflow/engineering-v1.json', policy)
        f.main = f.commit()
        self.registry = f.make_registry()
        self.registry['engineering'].append('maintenance/publication-workflow/engineering-v1.json')
        self.registry_path = self.directory/'registry.json'
        self.registry_path.write_text(json.dumps(self.registry)+'\n')
        self.runtime_path = self.directory/'runtime.json'
        dependencies = Path(os.environ.get('PUBLICATION_TEST_DEPENDENCIES',ROOT/'node_modules')).resolve()
        self.assertTrue(dependencies.is_dir(),'reviewed installed dependencies required; no skip')
        self.assertIsNotNone(shutil.which('node'),'reviewed installed Node required')
        self.assertIsNotNone(shutil.which('pnpm'),'reviewed installed pnpm required')
        self.runtime_path.write_text(json.dumps({'version':1,'node':str(Path(shutil.which('node')).resolve()),
            'node_version':'v24.13.0','dependencies':str(dependencies)})+'\n')
        self.config = {'version':1,'repository':'owner/example','role':'writer',
            'main':self.registry['main']['sha'],'staging':self.registry['staging']['sha'],
            'policy_sha256':hashlib.sha256(policy).hexdigest(),'source':str(f.repo),
            'registry':{'path':str(self.registry_path),'sha256':self.sha(self.registry_path)},
            'runtime':{'path':str(self.runtime_path),'sha256':self.sha(self.runtime_path)},
            'pnpm':{'path':str(Path(shutil.which('pnpm')).resolve()),'version':'10.28.0'},
            'snapshot_root':str(self.directory/'writer-inputs'),
            'state_directory':str(self.state),'state_identity_sha256':self.sha(self.state_identity)}
        self.config_path = self.directory/'job-config.json'

    @staticmethod
    def sha(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def prepare(self, role='writer', env=None):
        self.config['role'] = role
        self.config_path.write_text(json.dumps(self.config)+'\n')
        child = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        for key in ('PUBLICATION_WRITER_TOKEN','PUBLICATION_REPORTER_TOKEN','GH_TOKEN','GITHUB_TOKEN'):
            child.pop(key, None)
        if env:
            child.update(env)
        return subprocess.run([sys.executable,str(CLI),'prepare','--manifest',str(self.config_path),
            '--manifest-sha256',self.sha(self.config_path),'--repository','owner/example','--role',role],
            capture_output=True,text=True,env=child)

    def test_fresh_writer_validator_snapshots_recompute_same_operation_with_independent_digests(self):
        """PB-02: actual local Git/runtime/isolation with separate fresh job inputs."""
        writer = self.prepare()
        self.assertEqual(writer.returncode,0,writer.stdout+writer.stderr)
        a = json.loads(writer.stdout)
        self.config['snapshot_root'] = str(self.directory/'validator-inputs')
        validator = self.prepare('validator')
        self.assertEqual(validator.returncode,0,validator.stdout+validator.stderr)
        b = json.loads(validator.stdout)
        self.assertEqual(a['operation'],b['operation'])
        self.assertNotEqual(a['snapshot_root'],b['snapshot_root'])
        for receipt in (a,b):
            root = Path(receipt['snapshot_root'])
            self.addCleanup(root.chmod,0o700)
            self.assertEqual(root.stat().st_mode & 0o777,0o500)
            self.assertEqual((root/'registry.json').stat().st_mode & 0o777,0o400)
            self.assertEqual((root/'runtime.json').stat().st_mode & 0o777,0o400)
            self.assertEqual(receipt['isolation'],{'inside':True,'outside_read':'denied',
                                                 'outside_write':'denied','network':'denied'})
            self.assertFalse(receipt['publishable'])
            wrong_role='validator' if receipt['role']=='writer' else 'writer'
            refused=subprocess.run([sys.executable,str(CLI),'verify','--snapshot-root',str(root),
                '--binding-sha256',receipt['binding_sha256'],'--repository','owner/example',
                '--role',wrong_role],capture_output=True,text=True)
            self.assertNotEqual(refused.returncode,0,refused.stdout+refused.stderr)
            self.assertIn('role/repository',refused.stdout)
            self.assertEqual(receipt['surface'],'local job input preparation; no remote capability proof')

    def verify(self, receipt):
        return subprocess.run([sys.executable,str(CLI),'verify','--snapshot-root',receipt['snapshot_root'],
            '--binding-sha256',receipt['binding_sha256'],'--repository','owner/example','--role','writer'],
            capture_output=True,text=True)

    def test_snapshot_consumption_rejects_each_filesystem_predicate_and_input_tamper(self):
        """PB-03: public consumption refuses mutable, substituted or misowned inputs."""
        prepared = self.prepare()
        self.assertEqual(prepared.returncode,0,prepared.stdout+prepared.stderr)
        receipt = json.loads(prepared.stdout)
        root = Path(receipt['snapshot_root'])
        self.addCleanup(root.chmod,0o700)
        checked = self.verify(receipt)
        self.assertEqual(checked.returncode,0,checked.stdout+checked.stderr)
        # Real consumer must recheck sealed predicates and consume those bytes itself.
        target = root/'registry.json'
        target.chmod(0o600)
        consumer = subprocess.run([sys.executable,str(ROOT/'scripts/staging-sync-remote.py'),'run','--allow-remote-write',
            '--state-dir',str(self.state),'--repository','owner/example','--job-snapshot-root',str(root),
            '--job-binding-sha256',receipt['binding_sha256']],capture_output=True,text=True)
        self.assertNotEqual(consumer.returncode,0)
        self.assertIn('snapshot file ownership/mode',consumer.stdout,consumer.stdout+consumer.stderr)
        target.chmod(0o400)
        for mutation in ('directory-mode','file-mode','content','symlink','hardlink','directory-input','extra-file'):
            with self.subTest(mutation=mutation):
                target = root/'registry.json'
                original = target.read_bytes()
                root.chmod(0o700)
                if mutation == 'file-mode':
                    target.chmod(0o600)
                elif mutation == 'content':
                    target.chmod(0o600); target.write_bytes(b'{}'); target.chmod(0o400)
                elif mutation == 'symlink':
                    target.unlink(); target.symlink_to(self.registry_path)
                elif mutation == 'hardlink':
                    os.link(target,self.directory/'linked-input')
                elif mutation == 'directory-input':
                    target.unlink(); target.mkdir(mode=0o500)
                elif mutation == 'extra-file':
                    (root/'unregistered').write_text('not approved')
                if mutation != 'directory-mode':
                    root.chmod(0o500)
                refused = self.verify(receipt)
                self.assertNotEqual(refused.returncode,0,refused.stdout+refused.stderr)
                self.assertEqual(json.loads(refused.stdout)['status'],'blocked')
                root.chmod(0o700)
                if target.is_dir():
                    target.rmdir(); target.write_bytes(original)
                elif target.is_symlink():
                    target.unlink(); target.write_bytes(original)
                else:
                    target.chmod(0o600); target.write_bytes(original)
                target.chmod(0o400)
                if (self.directory/'linked-input').exists():
                    (self.directory/'linked-input').unlink()
                (root/'unregistered').unlink(missing_ok=True)
                root.chmod(0o500)
        alias = self.directory/'snapshot-alias'
        alias.symlink_to(root,target_is_directory=True)
        for path in (str(alias),os.path.relpath(root,ROOT)):
            with self.subTest(noncanonical_root=path):
                refused=self.verify(dict(receipt,snapshot_root=path))
                self.assertNotEqual(refused.returncode,0,refused.stdout+refused.stderr)
                self.assertIn('canonical',refused.stdout)
        self.config['snapshot_root']=str(self.fixture.repo/'forbidden-inputs')
        refused=self.prepare()
        self.assertNotEqual(refused.returncode,0,refused.stdout+refused.stderr)
        self.assertIn('overlaps',refused.stdout)
        self.assertFalse(Path(self.config['snapshot_root']).exists())
        # Explicit system-observation fixtures: no claim that the host changed UID/time.
        from unittest.mock import patch
        from types import SimpleNamespace
        sys.path.insert(0,str(ROOT/'scripts'))
        import publication_jobs as jobs
        with patch.object(jobs.os,'geteuid',return_value=os.geteuid()+1):
            with self.assertRaisesRegex(ValueError,'ownership'):
                jobs.verify_job(root,receipt['binding_sha256'],repository='owner/example',role='writer')
        original_fstat = os.fstat
        for changed_field,at_call in (('st_uid',1),('st_dev',1),('st_ino',1),
                ('st_dev',2),('st_ino',2),('st_size',2),('st_mtime_ns',2),('st_ctime_ns',2)):
            calls = [0]
            def observed(fd):
                info = original_fstat(fd); calls[0] += 1
                if calls[0] == at_call:
                    fields = ('st_dev','st_ino','st_size','st_mode','st_uid','st_nlink','st_mtime_ns','st_ctime_ns')
                    data = {key:getattr(info,key) for key in fields}
                    data[changed_field] += 1
                    return SimpleNamespace(**data)
                return info
            with self.subTest(observation_fixture=changed_field,at_call=at_call), patch.object(jobs.os,'fstat',side_effect=observed):
                with self.assertRaises(ValueError):
                    jobs.verify_job(root,receipt['binding_sha256'],repository='owner/example',role='writer')

    def test_preflight_refuses_credentials_without_git_or_build_exposure(self):
        """PB-04: token presence is refusal, never an input/config permission grant."""
        objects = sorted(str(p.relative_to(self.fixture.repo))
                         for p in (self.fixture.repo/'.git/objects').rglob('*'))
        for role in ('writer','validator'):
            for token in ('PUBLICATION_WRITER_TOKEN','PUBLICATION_REPORTER_TOKEN','GH_TOKEN','GITHUB_TOKEN'):
                with self.subTest(role=role,token=token):
                    result = self.prepare(role,{token:'SYNTHETIC-DO-NOT-EXPOSE'})
                    self.assertNotEqual(result.returncode,0)
                    self.assertIn('credentials',json.loads(result.stdout)['reason'])
                    self.assertNotIn('SYNTHETIC-DO-NOT-EXPOSE',result.stdout+result.stderr)
                    self.assertFalse(Path(self.config['snapshot_root']).exists())
        self.assertEqual(objects,sorted(str(p.relative_to(self.fixture.repo))
                         for p in (self.fixture.repo/'.git/objects').rglob('*')))

    def test_missing_or_wrong_runtime_stops_without_install_or_source_git_writes(self):
        """PB-01: named missing prerequisites; unavailable capability never falls back."""
        import copy
        base_config = copy.deepcopy(self.config)
        base_runtime = json.loads(self.runtime_path.read_bytes())
        objects = sorted(str(p.relative_to(self.fixture.repo))
                         for p in (self.fixture.repo/'.git/objects').rglob('*'))
        for variant in ('node-version','pnpm-version','missing-node','missing-pnpm',
                        'missing-dependencies','noncanonical-node','dependency-escape'):
            with self.subTest(variant=variant):
                self.config = copy.deepcopy(base_config)
                runtime = copy.deepcopy(base_runtime)
                if variant == 'node-version': runtime['node_version'] = 'v22.0.0'
                elif variant == 'pnpm-version': self.config['pnpm']['version'] = '10.0.0'
                elif variant == 'missing-node': runtime['node'] = str(self.directory/'missing-node')
                elif variant == 'missing-pnpm': self.config['pnpm']['path'] = str(self.directory/'missing-pnpm')
                elif variant == 'missing-dependencies': runtime['dependencies'] = str(self.directory/'missing-dependencies')
                elif variant == 'noncanonical-node':
                    runtime['node'] = str(Path(runtime['node']).parent/'..'/'bin'/'node')
                elif variant == 'dependency-escape':
                    deps = self.directory/'bad-dependencies'; deps.mkdir()
                    (deps/'vitepress').symlink_to(Path(base_runtime['dependencies'])/'vitepress')
                    runtime['dependencies'] = str(deps)
                self.runtime_path.write_text(json.dumps(runtime)+'\n')
                self.config['runtime']['sha256'] = self.sha(self.runtime_path)
                result = self.prepare()
                self.assertNotEqual(result.returncode,0,result.stdout+result.stderr)
                self.assertEqual(json.loads(result.stdout)['status'],'blocked')
                self.assertNotIn('Operation not permitted',json.loads(result.stdout)['reason'])
                self.assertFalse(Path(self.config['snapshot_root']).exists())
        # Runtime-observation fixtures are not execution on an older Python/Linux host.
        from unittest.mock import patch
        sys.path.insert(0,str(ROOT/'scripts'))
        import publication_jobs as jobs
        self.config = base_config
        self.runtime_path.write_text(json.dumps(base_runtime)+'\n')
        self.config['runtime']['sha256'] = self.sha(self.runtime_path)
        self.config_path.write_text(json.dumps(self.config)+'\n')
        for name,value in (('version_info',(3,10,0)),('platform','linux')):
            with self.subTest(observation_fixture=name), patch.object(jobs.sys,name,value):
                with self.assertRaises(ValueError):
                    jobs.materialize_job(self.config_path,self.sha(self.config_path),repository='owner/example',role='writer')
        self.assertEqual(objects,sorted(str(p.relative_to(self.fixture.repo))
                         for p in (self.fixture.repo/'.git/objects').rglob('*')))

    def test_durable_journal_recovery_and_unknown_source_identity_refuse(self):
        """PB-05: fresh jobs reuse durable state; an API ack never replaces readback."""
        import copy
        from article_publication import test_remote_sync as transport_fixture
        import publication_remote as remote
        state_config=copy.deepcopy(self.config)
        original_identity=self.state_identity.read_bytes()
        self.config['state_directory']=str(self.directory/'missing-durable-source')
        missing=self.prepare()
        self.assertNotEqual(missing.returncode,0,missing.stdout+missing.stderr)
        self.assertFalse(Path(self.config['snapshot_root']).exists())
        self.config=copy.deepcopy(state_config)
        foreign=json.loads(original_identity);foreign['repository']='other/repository'
        self.state_identity.chmod(0o600)
        self.state_identity.write_text(json.dumps(foreign)+'\n');self.state_identity.chmod(0o400)
        self.config['state_identity_sha256']=self.sha(self.state_identity)
        rejected=self.prepare()
        self.assertNotEqual(rejected.returncode,0,rejected.stdout+rejected.stderr)
        self.assertIn('state repository/identity',rejected.stdout)
        self.assertFalse(Path(self.config['snapshot_root']).exists())
        self.state_identity.chmod(0o600);self.state_identity.write_bytes(original_identity);self.state_identity.chmod(0o400)
        self.config=state_config
        first = self.prepare()
        self.assertEqual(first.returncode,0,first.stdout+first.stderr)
        snapshot = json.loads(first.stdout)
        self.addCleanup(Path(snapshot['snapshot_root']).chmod,0o700)
        self.assertNotEqual(snapshot['writer_group'],snapshot['validation_group'])
        self.assertFalse(snapshot['cancel_in_progress'])
        # Render public inactive workflow contracts using the existing YAML parser.
        parser = "const fs=require('fs'),yaml=require(process.argv[1]);console.log(JSON.stringify(process.argv.slice(2).map(p=>yaml.load(fs.readFileSync(p,'utf8')).concurrency)))"
        yaml_module = str(Path(os.environ.get('PUBLICATION_TEST_DEPENDENCIES',ROOT/'node_modules')).resolve()/'js-yaml')
        paths = [str(ROOT/'maintenance/publication-workflow/automation'/name)
                 for name in ('staging-sync-writer.yml.inactive','staging-sync-validate.yml.inactive')]
        parsed = subprocess.run([shutil.which('node'),'-e',parser,yaml_module,*paths],
                                capture_output=True,text=True,check=True)
        groups = json.loads(parsed.stdout)
        for contract,key in zip(groups,('writer_group','validation_group')):
            self.assertEqual(contract['group'].replace('${{ github.repository }}','owner/example'),snapshot[key])
            self.assertIs(contract['cancel-in-progress'],False)
        api = transport_fixture.FakeGitHub()
        api.state.update(main=self.config['main'],staging=self.config['staging'])
        original = api.advance
        def accepted_but_unknown(head,previous):
            original(head,previous)
            raise remote.RemoteError('synthetic accepted but unobserved response',uncertain=True)
        api.advance = accepted_but_unknown
        def prepared(refs):
            return {'status':'ready','tree':snapshot['operation']['tree'],'head':'4'*40,
                    'parents':list(dict.fromkeys([refs['main'],refs['staging']]
                                  +([refs['branch']] if refs['branch'] else [])))}
        for _ in range(2):
            result = remote.run_sync(api,prepared,repository='owner/example',
                policy=self.config['policy_sha256'],state_dir=self.state,
                activation=transport_fixture.activation(),authorized=True)
            self.assertEqual(result['status'],'ready',result)
        self.assertEqual(api.calls.count('advance'),1)
        self.assertEqual(api.calls.count('create_pull'),1)
        self.config['snapshot_root'] = str(self.directory/'retry-inputs')
        retried = self.prepare()
        self.assertEqual(retried.returncode,0,retried.stdout+retried.stderr)
        same = json.loads(retried.stdout)
        self.addCleanup(Path(same['snapshot_root']).chmod,0o700)
        self.assertEqual(same['operation'],snapshot['operation'])
        journal = self.state/(hashlib.sha256(b'owner/example').hexdigest()+'.json')
        value = json.loads(journal.read_bytes())
        foreign = copy.deepcopy(value)
        foreign['operation'] = remote.operation_for('owner/example',self.config['policy_sha256'],
            {'main':'0'*40,'staging':self.config['staging']},snapshot['operation']['tree'])
        journal.write_text(json.dumps(foreign)+'\n')
        self.config['snapshot_root'] = str(self.directory/'unknown-journal-inputs')
        refused = self.prepare()
        if Path(self.config['snapshot_root']).exists():
            self.addCleanup(Path(self.config['snapshot_root']).chmod,0o700)
        self.assertNotEqual(refused.returncode,0,refused.stdout+refused.stderr)
        self.assertIn('journal',json.loads(refused.stdout)['reason'])

    def test_incomplete_history_wrong_inputs_and_invented_capability_fields_refuse(self):
        """PB-06: source/config evidence stays distinct from live capability claims."""
        import copy
        baseline = copy.deepcopy(self.config)
        original_registry = self.registry_path.read_bytes()
        original_runtime = self.runtime_path.read_bytes()
        cases = [('shallow','complete'),('missing-ref','Git'),('wrong-source','source'),
                 ('wrong-pin','pins'),('wrong-tree','tree'),('registry-target','staging'),
                 ('registry-digest','digest'),('state-digest','digest'),
                 ('fake-permission','schema'),('fake-dispatch','schema'),('fake-exercise','schema')]
        for variant,reason in cases:
            with self.subTest(variant=variant):
                self.config = copy.deepcopy(baseline)
                self.registry_path.write_bytes(original_registry)
                if variant == 'shallow':
                    (self.fixture.repo/'.git/shallow').write_text(self.fixture.base+'\n')
                elif variant == 'missing-ref':
                    self.fixture.git('update-ref','-d','refs/heads/staging')
                elif variant == 'wrong-source':
                    self.config['source'] = str(self.directory/'missing-source')
                elif variant == 'wrong-pin': self.config['main'] = '0'*40
                elif variant in ('wrong-tree','registry-target'):
                    value = json.loads(original_registry)
                    if variant == 'wrong-tree': value['trees']['main']['engineering.txt']['blob'] = '0'*40
                    else: value['target'] = 'main'
                    self.registry_path.write_text(json.dumps(value)+'\n')
                    self.config['registry']['sha256'] = self.sha(self.registry_path)
                elif variant == 'registry-digest': self.config['registry']['sha256'] = '0'*64
                elif variant == 'state-digest': self.config['state_identity_sha256'] = '0'*64
                elif variant == 'fake-permission': self.config['permissions_verified'] = True
                elif variant == 'fake-dispatch': self.config['dispatch_verified'] = True
                elif variant == 'fake-exercise': self.config['exercise_run_id'] = 123
                result = self.prepare()
                self.assertNotEqual(result.returncode,0,result.stdout+result.stderr)
                self.assertIn(reason,json.loads(result.stdout)['reason'])
                self.assertFalse(Path(self.config['snapshot_root']).exists())
                (self.fixture.repo/'.git/shallow').unlink(missing_ok=True)
                if variant == 'missing-ref':
                    self.fixture.git('update-ref','refs/heads/staging',self.fixture.stage)
        self.config = baseline
        self.registry_path.write_bytes(original_registry)
        self.runtime_path.write_bytes(original_runtime)


if __name__ == '__main__':
    unittest.main()
