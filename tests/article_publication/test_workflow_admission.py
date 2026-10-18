"""PA-01–06: finite workflow admission at real public Git/native/CLI seams."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[2]
POLICY = 'maintenance/publication-workflow/engineering-v1.json'
WORKFLOW = '.github/workflows/staging-sync-validate.yml'
RAW = (b'name: inert admission fixture\non: workflow_dispatch\njobs:\n'
       b'  probe:\n    runs-on: ubuntu-latest\n    steps:\n'
       b'      - run: touch EXECUTION_MARKER\n')


class WorkflowAdmissionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='workflow-admission-')
        self.addCleanup(self.tmp.cleanup)
        self.directory = Path(self.tmp.name).resolve()
        self.control = self.directory/'control'
        subprocess.run(['git', 'clone', '--shared', '--no-checkout', '--template=',
                        str(SOURCE), str(self.control)], check=True, capture_output=True)
        self.git('checkout', '--detach', '8b31956f47075a831cfd0339339f616af96b3dae')
        data = json.loads((SOURCE/POLICY).read_bytes())
        for name in data['common']:
            p = self.control/name
            p.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SOURCE/name, p)
            p.chmod(0o755 if data['common'][name]['mode'] == '100755' else 0o644)
        path = self.control/WORKFLOW
        path.parent.mkdir(parents=True)
        self.workflow_raw = RAW.replace(b'EXECUTION_MARKER', str(self.directory/'workflow-executed').encode())
        path.write_bytes(self.workflow_raw)
        self.entry = {'mode':'100644', 'sha256':hashlib.sha256(self.workflow_raw).hexdigest()}
        data['common'][WORKFLOW] = self.entry
        (self.control/POLICY).write_text(json.dumps(data, indent=2)+'\n')
        self.git('add', '-A')
        tree = self.git('write-tree').strip().decode()
        parent = self.git('rev-parse', 'HEAD').strip().decode()
        raw = (f'tree {tree}\nparent {parent}\nauthor Fixture <fixture@example.invalid> 1 +0000\n'
               'committer Fixture <fixture@example.invalid> 1 +0000\n\nadmission fixture\n').encode()
        self.main = self.git('hash-object', '-t', 'commit', '-w', '--stdin', data=raw).strip().decode()
        self.git('update-ref', 'HEAD', self.main)
        self.git('update-ref', 'refs/heads/main', self.main)
        self.git('update-ref', 'refs/heads/staging', 'd2e59426fe545116f2c2b637fc6f181dcfcdbaf5')
        self.grant = {'version':1, 'repository':'owner/example', 'main':self.main,
                      'policies':dict.fromkeys(('main','staging'), hashlib.sha256((self.control/POLICY).read_bytes()).hexdigest()),
                      'roles':['main','staging'], 'approval':'owner-approved-local-fixture',
                      'workflows':{WORKFLOW:self.entry}}
        self.admission = self.directory/'admission.json'
        self.save_grant()

    def git(self, *args, data=None):
        return subprocess.check_output(['git', '-C', str(self.control), *args], input=data,
                                       stderr=subprocess.PIPE)

    def save_grant(self):
        self.admission.write_text(json.dumps(self.grant)+'\n')

    def reseal(self, index_mode=None, unlisted_gitlink=None):
        """Publish independently pinned synthetic main after a fixture source change."""
        self.git('add', '-A')
        if index_mode:
            self.git('update-index', '--cacheinfo', index_mode+','+self.main+','+WORKFLOW)
        if unlisted_gitlink:
            self.git('update-index', '--add', '--cacheinfo', '160000,'+self.main+','+unlisted_gitlink)
        tree = self.git('write-tree').strip().decode()
        raw = (f'tree {tree}\nparent {self.main}\nauthor Fixture <fixture@example.invalid> 1 +0000\n'
               'committer Fixture <fixture@example.invalid> 1 +0000\n\nnext fixture\n').encode()
        self.main = self.git('hash-object', '-t', 'commit', '-w', '--stdin', data=raw).strip().decode()
        self.git('update-ref', 'HEAD', self.main)
        self.git('update-ref', 'refs/heads/main', self.main)
        self.grant['main'] = self.main
        self.grant['policies'] = dict.fromkeys(('main','staging'), hashlib.sha256((self.control/POLICY).read_bytes()).hexdigest())
        self.save_grant()

    def options(self):
        return ['--workflow-admission', str(self.admission), '--workflow-admission-sha256',
                hashlib.sha256(self.admission.read_bytes()).hexdigest(),
                '--trusted-repository', 'owner/example', '--trusted-main', self.main]

    def cli(self, *args, control=None, options=True, native=False):
        script = (control or self.control)/'scripts'/('verify-harness-adoption.py' if native else 'publication-baseline.py')
        return subprocess.run([sys.executable, str(script), *args,
                               *(self.options() if options else [])], capture_output=True, text=True,
                              env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))

    def test_exact_approved_workflow_reaches_both_projections_and_native_readback(self):
        """PA-02: full positive public flow, never an installed/executed workflow."""
        output = self.directory/'projection'
        result = self.cli('prepare', '--output', str(output))
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        for role in ('main','staging'):
            with self.subTest(role=role):
                target = output/role
                self.assertEqual((target/WORKFLOW).read_bytes(), self.workflow_raw)
                checked = self.cli(control=target, native=True)
                self.assertEqual(checked.returncode, 0, checked.stdout+checked.stderr)
                self.assertEqual(json.loads(checked.stdout)['target_role'], role)
                self.assertFalse(json.loads(checked.stdout)['publishable'])
        self.assertFalse((self.directory/'workflow-executed').exists())

    def test_trusted_main_ref_drift_expires_grant_even_with_pinned_control_head(self):
        """PA-05: an old detached control cannot hide an advanced/replaced main ref."""
        before = self.cli(native=True)
        self.assertEqual(before.returncode, 0, before.stdout+before.stderr)
        self.git('update-ref', 'refs/heads/main', '8b31956f47075a831cfd0339339f616af96b3dae')
        after = self.cli(native=True)
        self.assertNotEqual(after.returncode, 0, after.stdout+after.stderr)
        self.assertIn('main', after.stderr)

    def test_no_grant_preserves_default_denial_at_both_public_entries(self):
        """PA-01: an engineering digest alone grants no workflow authority."""
        output = self.directory/'unapproved'
        prepared = self.cli('prepare', '--output', str(output), options=False)
        self.assertNotEqual(prepared.returncode, 0)
        self.assertIn('protected', prepared.stderr)
        self.assertFalse(output.exists())
        native = self.cli(native=True, options=False)
        self.assertNotEqual(native.returncode, 0)
        self.assertIn('protected', native.stderr)

    def test_undeclared_github_and_path_mode_type_hash_mutations_refuse(self):
        """PA-03: finite admission cannot grant any other deployment path/type."""
        import copy
        baseline = copy.deepcopy(self.grant)
        for name in ('.github/workflows/unlisted.yml', '.github/CODEOWNERS'):
            with self.subTest(unregistered_physical=name):
                path = self.control/name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'unregistered control source')
                output = self.directory/('unregistered-'+path.name)
                prepared = self.cli('prepare', '--output', str(output))
                self.assertNotEqual(prepared.returncode, 0, prepared.stdout+prepared.stderr)
                self.assertFalse(output.exists())
                native = self.cli(native=True)
                self.assertNotEqual(native.returncode, 0)
                path.unlink()
        # An uninitialized gitlink has no physical file for source_names to see.
        name = '.github/unlisted-module'
        (self.control/name).mkdir()
        self.reseal(unlisted_gitlink=name)
        for granted in (True, False):
            with self.subTest(unlisted_gitlink=name, granted=granted):
                output = self.directory/('gitlink-'+str(granted))
                prepared = self.cli('prepare', '--output', str(output), options=granted)
                self.assertNotEqual(prepared.returncode, 0, prepared.stdout+prepared.stderr)
                self.assertFalse(output.exists())
                native = self.cli(native=True, options=granted)
                self.assertNotEqual(native.returncode, 0, native.stdout+native.stderr)
        self.git('update-index', '--force-remove', name)
        (self.control/name).rmdir()
        self.reseal()
        baseline = copy.deepcopy(self.grant)
        # Stage control and a distinct readback root must not hide Git-only sources.
        projection = self.directory/'stage-boundary'
        clean = self.cli('prepare','--output',str(projection))
        self.assertEqual(clean.returncode,0,clean.stdout+clean.stderr)
        trusted = projection/'staging'
        candidate = self.directory/'stage-with-unlisted-gitlink'
        shutil.copytree(trusted,candidate,symlinks=True)
        def stage_git(*args,data=None):
            return subprocess.check_output(['git','-C',str(candidate),*args],input=data,stderr=subprocess.PIPE)
        name = '.github/unlisted-module'
        (candidate/name).mkdir()
        stage_git('add','-A')
        stage_git('update-index','--add','--cacheinfo','160000,'+self.main+','+name)
        tree = stage_git('write-tree').decode().strip()
        parent = stage_git('rev-parse','HEAD').decode().strip()
        raw = (f'tree {tree}\nparent {parent}\nparent {self.main}\n'
               'author Fixture <fixture@example.invalid> 1 +0000\n'
               'committer Fixture <fixture@example.invalid> 1 +0000\n\nstage fixture\n').encode()
        head = stage_git('hash-object','-t','commit','-w','--stdin',data=raw).decode().strip()
        stage_git('update-ref','HEAD',head)
        for surface in ('stage-prepare','stage-native','separate-root-native'):
            with self.subTest(unlisted_stage_gitlink=surface):
                output = self.directory/surface
                if surface=='stage-prepare':
                    refused=self.cli('prepare','--output',str(output),control=candidate)
                elif surface=='stage-native':
                    refused=self.cli(control=candidate,native=True)
                else:
                    refused=self.cli('--root',str(candidate),control=trusted,native=True)
                self.assertNotEqual(refused.returncode,0,refused.stdout+refused.stderr)
                self.assertFalse(output.exists())
        variants = ('unknown-workflow','other-github','wildcard','traversal','wrong-mode',
                    'wrong-hash','wrong-repo','wrong-role','link','submodule','duplicate')
        for variant in variants:
            with self.subTest(variant=variant):
                self.grant = copy.deepcopy(baseline)
                if variant in ('unknown-workflow','other-github','wildcard','traversal'):
                    name = {'unknown-workflow':'.github/workflows/unlisted.yml',
                            'other-github':'.github/CODEOWNERS',
                            'wildcard':'.github/workflows/*.yml',
                            'traversal':'.github/workflows/../escape.yml'}[variant]
                    self.grant['workflows'][name] = self.entry
                elif variant == 'wrong-mode':
                    self.grant['workflows'][WORKFLOW]['mode'] = '100755'
                elif variant == 'wrong-hash':
                    self.grant['workflows'][WORKFLOW]['sha256'] = '0'*64
                elif variant == 'wrong-repo':
                    self.grant['repository'] = 'attacker/other'
                elif variant == 'wrong-role':
                    self.grant['roles'] = ['candidate']
                elif variant == 'link':
                    (self.control/WORKFLOW).unlink()
                    (self.control/WORKFLOW).symlink_to('../../package.json')
                elif variant == 'submodule':
                    self.reseal(index_mode='160000')
                self.save_grant()
                if variant == 'duplicate':
                    raw = self.admission.read_text()
                    self.admission.write_text(raw[:-2]+',"version":1}\n')
                output = self.directory/variant
                prepared = self.cli('prepare', '--output', str(output))
                self.assertNotEqual(prepared.returncode, 0, prepared.stdout+prepared.stderr)
                self.assertFalse(output.exists())
                native = self.cli(native=True)
                self.assertNotEqual(native.returncode, 0, native.stdout+native.stderr)
                if variant == 'link':
                    (self.control/WORKFLOW).unlink()
                    (self.control/WORKFLOW).write_bytes(self.workflow_raw)
                if variant == 'submodule':
                    self.reseal()
                    baseline = copy.deepcopy(self.grant)
        # Even an independently re-pinned policy must not expand the finite grant.
        for name in ('.github/workflows/unlisted.yml', '.github/CODEOWNERS'):
            with self.subTest(unlisted_common=name):
                path = self.control/name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'unlisted')
                data = json.loads((self.control/POLICY).read_bytes())
                data['common'][name] = {'mode':'100644','sha256':hashlib.sha256(b'unlisted').hexdigest()}
                (self.control/POLICY).write_text(json.dumps(data, indent=2)+'\n')
                self.reseal()
                output = self.directory/('common-'+path.name)
                refused = self.cli('prepare', '--output', str(output))
                self.assertNotEqual(refused.returncode, 0, refused.stdout+refused.stderr)
                self.assertIn('protected', refused.stderr)
                self.assertFalse(output.exists())
                native = self.cli(native=True)
                self.assertNotEqual(native.returncode, 0)
                self.assertIn('protected', native.stderr)

    def test_candidate_admission_and_independent_digest_or_source_swap_refuse(self):
        """PA-04: approved bytes cannot select their own authority or source."""
        import copy
        baseline = copy.deepcopy(self.grant)
        original = self.admission
        copied = self.control/'candidate-grant.json'
        copied.write_bytes(original.read_bytes())
        self.admission = copied
        result = self.cli('prepare', '--output', str(self.directory/'candidate-grant'))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('outside control and candidate', result.stderr)
        copied.unlink()
        self.admission = original
        approved_options = self.options()
        self.grant['approval'] = 'swapped'
        self.save_grant()
        result = self.cli('prepare', '--output', str(self.directory/'digest-swap'),
                          *approved_options, options=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('digest changed', result.stderr)
        self.grant = baseline
        self.grant['main'] = '8b31956f47075a831cfd0339339f616af96b3dae'
        self.save_grant()
        source = self.cli(native=True)
        self.assertNotEqual(source.returncode, 0)
        self.assertIn('authority', source.stderr)
        self.assertFalse((self.directory/'candidate-grant').exists())
        self.assertFalse((self.directory/'digest-swap').exists())

    def test_historical_cli_fixture_needs_no_current_workflow_helper(self):
        """PA-06: the original three-file historical CLI overlay still runs alone."""
        fixture = self.directory/'historical-cli'
        subprocess.run(['git', 'clone', '--shared', '--no-checkout', '--template=',
                        str(SOURCE), str(fixture)], check=True, capture_output=True)
        subprocess.run(['git', '-C', str(fixture), 'checkout', '--detach',
                        '69ff85f5fe1baddb54102070a436dff9ac1c5b73'],
                       check=True, capture_output=True)
        for name in ('scripts/verify-harness-adoption.py', 'scripts/harness_reconciliation.py',
                     'maintenance/harness-reconciliation/staging.json'):
            source = SOURCE/name
            if source.exists():
                target = fixture/name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
        self.assertFalse((fixture/'scripts/publication_workflows.py').exists())
        command = [sys.executable, str(fixture/'scripts/verify-harness-adoption.py')]
        checked = subprocess.run(command, cwd=fixture, capture_output=True, text=True)
        self.assertEqual(checked.returncode, 0, checked.stdout+checked.stderr)
        self.assertEqual(json.loads(checked.stdout)['status'], 'pass')
        unknown = subprocess.run(command+['--workflow-admission', str(self.admission)],
                                 cwd=fixture, capture_output=True, text=True)
        self.assertNotEqual(unknown.returncode, 0)
        self.assertIn('unrecognized arguments', unknown.stderr)
        # Current help/argument errors must exit before probing the target Git repo.
        tools = self.directory/'git-probe-bin'
        tools.mkdir()
        marker = self.directory/'target-git-probed'
        real_git = shutil.which('git')
        probe = tools/'git'
        probe.write_text('#!'+sys.executable+'\n'+
            'import os,sys\nfrom pathlib import Path\n'+
            'args=sys.argv[1:]\n'+
            'if "-C" in args and args[args.index("-C")+1]=='+repr(str(fixture))+':\n'+
            ' Path('+repr(str(marker))+').write_text("target Git queried")\n'+
            'os.execv('+repr(real_git)+', ["git", *args])\n')
        probe.chmod(0o755)
        env = dict(os.environ, PATH=str(tools)+os.pathsep+os.environ['PATH'])
        current = [sys.executable, str(SOURCE/'scripts/verify-harness-adoption.py'),
                   '--root', str(fixture)]
        for option in ('--help', '--unknown-option'):
            marker.unlink(missing_ok=True)
            result = subprocess.run(current+[option], cwd=SOURCE, env=env,
                                    capture_output=True, text=True)
            self.assertFalse(marker.exists(), result.stdout+result.stderr)
            if option == '--help':
                self.assertEqual(result.returncode, 0)
                self.assertIn('--workflow-admission', result.stdout)
            else:
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('unrecognized arguments', result.stderr)

    def test_projection_retains_noncommon_baseline_bytes_aliases_and_historical_oracle(self):
        """PA-06: complete M0 ownership retention, not only the admitted path."""
        output = self.directory/'preserved'
        prepared = self.cli('prepare', '--output', str(output))
        self.assertEqual(prepared.returncode, 0, prepared.stdout+prepared.stderr)
        inventory = json.loads((SOURCE/'.proj.specs/0012-publication-workflow/implementation/T-0013/M0-inventory.proposed.json').read_bytes())
        common = json.loads((self.control/POLICY).read_bytes())['common']
        for role, entries in inventory['trees'].items():
            for name, entry in entries.items():
                if name in common or name == POLICY:
                    continue
                p = output/role/name
                with self.subTest(role=role, path=name):
                    raw = os.readlink(p).encode() if entry['mode'] == '120000' else p.read_bytes()
                    actual = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
                    self.assertEqual(actual, entry['blob'])
        # Current stage's post-M0 management evidence must also survive the common baseline.
        stage_pin='05fc16c30f978bbafab4b8cc89f24f8657ab3045'
        main_pin='8b31956f47075a831cfd0339339f616af96b3dae'
        stage_policy=json.loads(self.git('show',stage_pin+':'+POLICY))
        main_policy=json.loads(self.git('show',main_pin+':'+POLICY))
        extra=set(stage_policy['common'])-set(main_policy['common'])
        self.assertEqual(len(extra),22)
        for name in extra:
            expected=self.git('show',stage_pin+':'+name)
            for role in ('main','staging'):
                with self.subTest(current_stage_management=name,role=role):
                    self.assertEqual((output/role/name).read_bytes(),expected)
                    self.assertEqual(common[name],stage_policy['common'][name])
        sys.path.insert(0,str(SOURCE/'scripts'))
        import publication_current as current
        from publication_workflows import WorkflowAdmission
        grant=WorkflowAdmission(self.admission,hashlib.sha256(self.admission.read_bytes()).hexdigest(),
                                'owner/example',self.main)
        readback=current.verify_staging_sync(output/'main',output/'staging',workflow_admission=grant)
        self.assertEqual(readback['target_role'],'staging')
        self.assertEqual(readback['candidate_paths_preserved'],50)
        oracle = 'tests/article_publication/test_current_baseline.py'
        self.assertEqual((self.control/oracle).read_bytes(),
                         self.git('show', '001b26f8e931e0cf1e62373c5aa088a1b5ed09eb:'+oracle))


if __name__ == '__main__':
    unittest.main()
