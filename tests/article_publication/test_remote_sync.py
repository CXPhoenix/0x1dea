"""Approved P10-P12 public trusted writer seam; no live GitHub authority."""
import copy
import base64
import hashlib
import importlib
from pathlib import Path
import sys
import subprocess
import shutil
import os
import tempfile
import threading
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]/'scripts'))


def activation():
    return {'repository': 'owner/example', 'permissions_verified': True,
            'latest_base_verified': True, 'dispatch_verified': True,
            'candidate_isolation_verified': True, 'exercise_run_id': 123,
            'workflow': 'staging-sync-validate.yml', 'workflow_sha256': 'a'*64,
            'branch_seed': None}


class FakeGitHub:
    def __init__(self):
        self.state = {'main': '1'*40, 'staging': '2'*40, 'branch': None}
        self.prs = []
        self.commits = {}
        self.runs = []
        self.calls = []

    def refs(self):
        return copy.deepcopy(self.state)

    def pulls(self):
        return copy.deepcopy(self.prs)

    def commit(self, head):
        return self.commits[head]

    def upload(self, prepared, operation):
        self.calls.append('upload')
        self.commits[prepared['head']] = {'tree': prepared['tree'], 'owner': operation['owner'],
                                         'operation': operation['id'], 'parents': prepared['parents']}

    def advance(self, head, previous):
        assert previous == self.state['branch']
        self.calls.append('advance')
        self.state['branch'] = head

    def workflow(self, main):
        return {'sha256': 'a'*64, 'main': main}

    def dispatch(self, operation, head):
        self.calls.append('dispatch')
        self.runs.append({'id': 456, 'event': 'workflow_dispatch', 'main': operation['main'],
                          'workflow': 'staging-sync-validate.yml', 'operation': operation['id'],
                          'head': head, 'status': 'completed', 'conclusion': 'success'})

    def validation_runs(self, operation, head):
        return copy.deepcopy(self.runs)

    def create_pull(self, operation, head):
        self.calls.append('create_pull')
        self.prs.append({'number': 7, 'state': 'open', 'base': 'staging',
                         'head': head, 'branch': 'tickets/T-0016/main-to-staging-sync',
                         'repository': 'owner/example', 'owner': operation['owner'],
                         'operation': operation['id']})

    def update_pull(self, number, operation, head):
        self.calls.append('update_pull')
        for p in self.prs:
            if p['number'] == number:
                p.update(operation=operation['id'], head=head)


def prepare(refs):
    return {'status': 'ready', 'tree': '3'*40, 'head': '4'*40,
            'parents': list(dict.fromkeys([refs['staging'], refs['main']] +
                                         ([refs['branch']] if refs['branch'] else [])))}


class RemoteSyncTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='remote-sync-')
        self.addCleanup(self.tmp.cleanup)
        self.api = FakeGitHub()

    def run_sync(self, **kwargs):
        module = importlib.import_module('publication_remote')
        options = dict(repository='owner/example', policy='b'*64,
                       state_dir=Path(self.tmp.name), activation=activation(), authorized=True)
        options.update(kwargs)
        return module.run_sync(self.api, prepare, **options)

    def test_run_cli_does_not_pass_writer_token_to_git_preparation(self):
        import json
        directory=Path(self.tmp.name)
        marker=directory/'git-env.jsonl'
        bindir=directory/'bin';bindir.mkdir()
        real_git=shutil.which('git')
        wrapper=bindir/'git'
        wrapper.write_text('#!'+sys.executable+'\nimport os,sys,json\n'
            +'with open('+repr(str(marker))+',"a") as f:f.write(json.dumps({"writer":bool(os.environ.get("PUBLICATION_WRITER_TOKEN"))})+"\\n")\n'
            +'os.execv('+repr(real_git)+',['+repr(real_git)+',*sys.argv[1:]])\n')
        wrapper.chmod(0o755)
        registry=directory/'registry.json';registry.write_text('{}')
        authority=directory/'authority.json';authority.write_text('{}')
        root=Path(__file__).resolve().parents[2]
        policy=hashlib.sha256((root/'maintenance/publication-workflow/engineering-v1.json').read_bytes()).hexdigest()
        env=dict(os.environ,PATH=str(bindir)+os.pathsep+os.environ['PATH'],
                 PUBLICATION_WRITER_TOKEN='synthetic-writer-must-not-reach-git')
        result=subprocess.run([sys.executable,str(root/'scripts/staging-sync-remote.py'),'run',
            '--allow-remote-write','--repository','owner/example','--policy-sha256',policy,
            '--registry',str(registry),'--registry-sha256',hashlib.sha256(registry.read_bytes()).hexdigest(),
            '--activation',str(authority),'--activation-sha256',hashlib.sha256(authority.read_bytes()).hexdigest(),
            '--state-dir',str(directory/'state')],capture_output=True,text=True,env=env)
        self.assertEqual(result.returncode,2,result.stdout+result.stderr)
        observations=[json.loads(line) for line in marker.read_text().splitlines()]
        self.assertTrue(observations)
        self.assertFalse(any(row['writer'] for row in observations))
        self.assertNotIn('synthetic-writer-must-not-reach-git',result.stdout+result.stderr)

    def test_bootstrap_cannot_skip_observed_exact_merged_implementation_pull(self):
        for variant in ('missing','wrong-number','wrong-head','unmerged','open'):
            with self.subTest(variant=variant):
                self.api=FakeGitHub()
                self.api.state['branch']='5'*40
                self.api.commits['5'*40]={'owner':None,'tree':'6'*40,'parents':['1'*40]}
                self.api.is_ancestor=lambda *args: True
                pr={'number':8,'state':'closed','base':'main','head':'5'*40,
                    'branch':'tickets/T-0016/main-to-staging-sync','repository':'owner/example',
                    'owner':None,'operation':None,'merged':True}
                if variant=='wrong-number':pr['number']=9
                if variant=='wrong-head':pr['head']='6'*40
                if variant=='unmerged':pr['merged']=False
                if variant=='open':pr['state']='open'
                self.api.prs=[] if variant=='missing' else [pr]
                result=self.run_sync(activation=dict(activation(),branch_seed='5'*40,bootstrap_pr=8))
                self.assertEqual(result['status'],'blocked')
                self.assertEqual(self.api.calls,[])

    def test_manual_pull_close_during_validation_prevents_ready_and_body_update(self):
        self.assertEqual(self.run_sync()['status'],'ready')
        original=self.api.validation_runs
        def closed(operation,head):
            self.api.prs[0]['state']='closed'
            return original(operation,head)
        self.api.validation_runs=closed
        self.api.calls.clear()
        result=self.run_sync()
        self.assertEqual(result['status'],'blocked')
        self.assertNotIn('update_pull',self.api.calls)
        self.assertEqual(len(self.api.prs),1)

    def test_uploaded_commit_readback_must_match_independent_operation(self):
        for field,value in [('tree','9'*40),('owner','unrelated'),('parents',[])]:
            with self.subTest(field=field):
                self.api=FakeGitHub()
                original=self.api.upload
                def corrupt(prepared,operation):
                    original(prepared,operation)
                    self.api.commits[prepared['head']][field]=value
                self.api.upload=corrupt
                self.assertEqual(self.run_sync()['status'],'blocked')
                self.assertIsNone(self.api.state['branch'])
                self.assertEqual(self.api.prs,[])

    def test_operation_record_exists_before_remote_mutation(self):
        import json
        original=self.api.upload
        def upload(prepared,operation):
            records=list(Path(self.tmp.name).glob('*.json'))
            self.assertEqual(len(records),1)
            value=json.loads(records[0].read_text())
            self.assertEqual(value['operation'],operation)
            self.assertEqual(value['head'],prepared['head'])
            self.assertEqual(value['status'],'prepared')
            original(prepared,operation)
        self.api.upload=upload
        self.assertEqual(self.run_sync()['status'],'ready')

    def test_transport_keeps_payload_out_of_shell_and_filters_credentials(self):
        import json
        module = importlib.import_module('publication_remote')
        calls=[]
        payload={'value':'$(touch /tmp/must-not-run); `id`'}
        def process(command, **options):
            calls.append((command,options))
            return subprocess.CompletedProcess(command,0,'HTTP/2.0 204 No Content\r\n\r\n','')
        client=module.GhTransport('writer-secret',state_dir=Path(self.tmp.name),
                                 executable='/fixture/gh',process=process)
        self.assertEqual(client('POST','repos/owner/example/actions/workflows/x/dispatches',payload),{})
        command,options=calls[0]
        self.assertNotIn(payload['value'],' '.join(command))
        self.assertEqual(json.loads(options['input']),payload)
        self.assertFalse(options.get('shell',False))
        self.assertEqual(options['env']['GH_TOKEN'],'writer-secret')
        self.assertNotIn('PUBLICATION_WRITER_TOKEN',options['env'])
        self.assertNotIn('AWS_SECRET_ACCESS_KEY',options['env'])

    def test_real_local_preparation_builds_only_independent_tree_without_source_writes(self):
        module = importlib.import_module('publication_remote_git')
        import json
        import os
        repo = Path(self.tmp.name)/'source'
        repo.mkdir()
        def git(*args, data=None):
            return subprocess.check_output(['git','-C',str(repo),*args], input=data).decode().strip()
        git('init','-q','-b','main')
        git('config','user.name','Fixture')
        git('config','user.email','fixture@example.invalid')
        def commit(parent=None):
            git('add','--all')
            return git('commit-tree',git('write-tree'),*(['-p',parent] if parent else []),'-m','Synthetic fixture')
        (repo/'engineering.txt').write_text('base\n')
        (repo/'blog').mkdir()
        (repo/'blog/B.md').write_text('published\n')
        base = commit()
        git('update-ref','refs/heads/main',base)
        git('switch','-q','-c','staging')
        (repo/'blog/B.md').write_text('candidate full metadata and bytes\n')
        stage = commit(base)
        git('update-ref','refs/heads/staging',stage)
        git('switch','-q','main')
        (repo/'engineering.txt').write_text('approved engineering\n')
        main = commit(base)
        git('update-ref','refs/heads/main',main)
        def entries(ref):
            result = {}
            for row in git('ls-tree','-r',ref).splitlines():
                meta,path = row.split('\t');mode,kind,blob=meta.split()
                result[path]={'mode':mode,'blob':blob}
            return result
        mt,st=entries(main),entries(stage)
        registry={'version':1,'target':'staging','repository':str(repo),
            'main':{'ref':'main','sha':main},'staging':{'ref':'staging','sha':stage},
            'trees':{'main':mt,'staging':st},
            'candidates':[{'id':'B','source':{'ref':'staging','sha':stage},'paths':{'blog/B.md':st['blog/B.md']}}],
            'engineering':['engineering.txt'],'checks':{}}
        before = git('show-ref')
        objects = {p.relative_to(repo).as_posix():p.read_bytes() for p in (repo/'.git/objects').rglob('*') if p.is_file()}
        preparer = module.LocalPreparation(registry, repository='owner/example', policy='b'*64,
                                           directory=Path(self.tmp.name)/'prepared')
        result = preparer({'main':main,'staging':stage,'branch':None})
        self.assertEqual(result['status'],'ready')
        store=result['store']
        read=lambda path: subprocess.check_output(['git','-C',str(store),'show',result['head']+':'+path])
        self.assertEqual(read('engineering.txt'),b'approved engineering\n')
        self.assertEqual(read('blog/B.md'),b'candidate full metadata and bytes\n')
        self.assertEqual(result['parents'],[stage,main])
        import publication_remote as remote
        uploads=[]
        def request(method, endpoint, data=None):
            uploads.append((method,endpoint,data))
            if endpoint.endswith('git/trees'):
                self.assertEqual({e['path'] for e in data['tree']},{'engineering.txt','blog/B.md'})
                return {'sha':result['tree']}
            if endpoint.endswith('git/commits'):
                self.assertEqual(data['tree'],result['tree'])
                self.assertEqual(data['parents'],[stage,main])
                self.assertIn('0x1DEA-operation: ',data['message'])
                return {'sha':result['head']}
            raise AssertionError(endpoint)
        api=remote.GitHubAdapter('owner/example',request)
        api.upload(result,module.operation_for('owner/example','b'*64,
                    {'main':main,'staging':stage,'branch':None},result['tree']))
        self.assertEqual(len(uploads),2)
        self.assertFalse(any('/git/refs' in endpoint for _,endpoint,_ in uploads))
        self.assertEqual(git('show-ref'),before)
        self.assertEqual(objects,{p.relative_to(repo).as_posix():p.read_bytes() for p in (repo/'.git/objects').rglob('*') if p.is_file()})
        self.assertEqual(preparer({'main':'9'*40,'staging':stage,'branch':None})['status'],'stale')
        (repo/'engineering.txt').write_text('later approved engineering\n')
        newer=commit(main)
        git('update-ref','refs/heads/main',newer)
        refreshed=preparer({'main':newer,'staging':stage,'branch':None})
        self.assertEqual(refreshed['status'],'ready')
        self.assertEqual(subprocess.check_output(['git','-C',refreshed['store'],'show',
                         refreshed['head']+':engineering.txt']),b'later approved engineering\n')
        self.assertEqual(subprocess.check_output(['git','-C',refreshed['store'],'show',
                         refreshed['head']+':blog/B.md']),b'candidate full metadata and bytes\n')
        git('switch','-q','staging')
        (repo/'engineering.txt').write_text('conflicting staging engineering\n')
        conflicting=commit(stage)
        git('update-ref','refs/heads/staging',conflicting)
        conflict=preparer({'main':newer,'staging':conflicting,'branch':None})
        self.assertEqual(conflict['status'],'conflict')
        self.assertEqual(conflict['paths'],['engineering.txt'])

    def test_supported_cli_schema_and_inert_run_need_no_credentials(self):
        cli = Path(__file__).resolve().parents[2]/'scripts/staging-sync-remote.py'
        schema = subprocess.run([sys.executable, str(cli), 'schema'], capture_output=True, text=True)
        self.assertEqual(schema.returncode, 0, schema.stderr)
        import json
        self.assertEqual(json.loads(schema.stdout)['operations'], ['schema', 'run', 'validate'])
        run = subprocess.run([sys.executable, str(cli), 'run'], capture_output=True, text=True,
                             env={'PATH':'/usr/bin:/bin'})
        self.assertEqual(run.returncode, 2)
        self.assertEqual(json.loads(run.stdout)['status'], 'blocked')
        self.assertIn('authority', json.loads(run.stdout)['reason'])

    def test_implementation_branch_bootstrap_requires_exact_approved_main_ancestor(self):
        self.api.state['branch']='5'*40
        self.api.commits['5'*40]={'owner':None,'tree':'6'*40,'parents':['1'*40]}
        self.api.is_ancestor=lambda ancestor,descendant: ancestor=='5'*40 and descendant=='1'*40
        self.api.prs=[{'number':8,'state':'closed','base':'main','head':'5'*40,
                      'branch':'tickets/T-0016/main-to-staging-sync','repository':'owner/example',
                      'owner':None,'operation':None,'merged':True}]
        self.assertEqual(self.run_sync(activation=dict(activation(),branch_seed='5'*40,bootstrap_pr=8))['status'],'ready')
        self.api=FakeGitHub()
        self.api.state['branch']='5'*40
        self.api.commits['5'*40]={'owner':None,'tree':'6'*40,'parents':['1'*40]}
        self.api.is_ancestor=lambda *args: False
        self.assertEqual(self.run_sync(activation=dict(activation(),branch_seed='5'*40))['status'],'blocked')
        self.assertEqual(self.api.calls,[])

    def test_conflict_report_retains_exact_paths_without_writes(self):
        module=importlib.import_module('publication_remote')
        result=module.run_sync(self.api,lambda refs:{'status':'conflict','paths':['blog/B.md'],
                              'reason':'independent merge conflict'},repository='owner/example',
            policy='b'*64,state_dir=Path(self.tmp.name),activation=activation(),authorized=True)
        self.assertEqual(result['status'],'conflict')
        self.assertEqual(result['paths'],['blog/B.md'])
        self.assertEqual(self.api.calls,[])

    def test_github_branch_update_is_only_owned_nonforce_ref(self):
        module = importlib.import_module('publication_remote')
        calls = []
        api = module.GitHubAdapter('owner/example', lambda *args: calls.append(args))
        api.advance('4'*40, None)
        api.advance('5'*40, '4'*40)
        self.assertEqual(calls[0], ('POST', 'repos/owner/example/git/refs',
            {'ref':'refs/heads/'+module.BRANCH, 'sha':'4'*40}))
        self.assertEqual(calls[1], ('PATCH', 'repos/owner/example/git/refs/heads/'+module.BRANCH,
            {'sha':'5'*40, 'force':False}))

    def test_github_resources_bind_existing_commit_run_and_pull(self):
        module = importlib.import_module('publication_remote')
        operation = {'version': 1, 'repository': 'owner/example', 'target': 'staging',
                     'branch': module.BRANCH, 'owner': module.OWNER, 'main': '1'*40,
                     'staging': '2'*40, 'policy': 'b'*64, 'tree': '3'*40}
        operation['id'] = hashlib.sha256(module.canonical(operation)).hexdigest()
        prs = []
        calls = []
        def request(method, endpoint, data=None):
            path = endpoint.removeprefix('repos/owner/example/')
            calls.append((method, path, data))
            if path.startswith('git/ref/heads/'):
                role = path.removeprefix('git/ref/heads/')
                return {'object': {'sha': {'main':'1'*40, 'staging':'2'*40}.get(role, '4'*40)}}
            if path == 'git/commits/'+'4'*40:
                return {'tree': {'sha':'3'*40}, 'parents':[{'sha':'2'*40},{'sha':'1'*40}],
                        'message': 'sync\n\n0x1DEA-operation: '+module.canonical(operation).decode().strip()}
            if path.startswith('contents/'):
                return {'encoding':'base64', 'content':base64.b64encode(b'workflow').decode()}
            if '/runs?' in path:
                return {'workflow_runs':[{'id':456, 'event':'workflow_dispatch', 'head_sha':'1'*40,
                    'path':'.github/workflows/staging-sync-validate.yml',
                    'display_title':'staging-sync:'+operation['id']+':'+'4'*40,
                    'status':'completed', 'conclusion':'success'}]}
            if path.startswith('pulls?'):
                return prs
            if path == 'pulls' and method == 'POST':
                prs.append({'number':7,'state':'open','body':data['body'],
                    'base':{'ref':'staging'},'head':{'ref':module.BRANCH,'sha':'4'*40,
                                                  'repo':{'full_name':'owner/example'}}})
                return prs[0]
            raise AssertionError((method, path, data))
        api = module.GitHubAdapter('owner/example', request, poll_attempts=1)
        result = module.run_sync(api, prepare, repository='owner/example', policy='b'*64,
            state_dir=Path(self.tmp.name), authorized=True,
            activation=dict(activation(), workflow_sha256=hashlib.sha256(b'workflow').hexdigest()))
        self.assertEqual(result['status'], 'ready')
        self.assertEqual(result['run_id'], 456)
        self.assertEqual(len(prs), 1)
        self.assertFalse(any(method=='PATCH' and path.startswith('git/') for method,path,_ in calls))

    def test_github_dispatch_treats_all_inputs_as_json_data(self):
        module = importlib.import_module('publication_remote')
        requests = []
        def request(method, endpoint, data=None):
            requests.append((method, endpoint, data))
            return {}
        api = module.GitHubAdapter('owner/example', request, poll_attempts=1)
        operation = {'id': 'a'*64, 'main': '1'*40, 'staging': '2'*40,
                     'tree': '3'*40, 'policy': 'b'*64}
        api.dispatch(operation, '4'*40)
        method, endpoint, data = requests[0]
        self.assertEqual(method, 'POST')
        self.assertEqual(endpoint, 'repos/owner/example/actions/workflows/staging-sync-validate.yml/dispatches')
        self.assertEqual(data['ref'], 'main')
        self.assertEqual(data['inputs']['main'], '1'*40)
        self.assertEqual(data['inputs']['head'], '4'*40)
        self.assertEqual(data['inputs']['operation'], 'a'*64)

    def test_shared_lock_serializes_sync_and_other_participating_writer(self):
        module = importlib.import_module('publication_remote')
        started = threading.Event()
        completed = threading.Event()
        errors = []
        def sync():
            started.set()
            try:
                self.run_sync()
            except Exception as error:
                errors.append(error)
            finally:
                completed.set()
        with module.writer_lock(Path(self.tmp.name), 'owner/example'):
            thread = threading.Thread(target=sync)
            thread.start()
            self.assertTrue(started.wait(2))
            self.assertFalse(completed.wait(0.05))
            self.assertEqual(self.api.calls, [])
        thread.join(3)
        self.assertTrue(completed.is_set())
        self.assertEqual(errors, [])
        self.assertEqual(len(self.api.prs), 1)

    def test_denied_or_unobserved_outcome_never_creates_duplicate(self):
        module = importlib.import_module('publication_remote')
        for uncertain in (False, True):
            self.api = FakeGitHub()
            def refusal(*args):
                raise module.RemoteError('denied/timeout', uncertain=uncertain)
            self.api.create_pull = refusal
            result = self.run_sync()
            self.assertEqual(result['status'], 'blocked')
            self.assertEqual(self.api.prs, [])
            self.assertLessEqual(result['retries'], 3)
        self.api = FakeGitHub()
        self.api.dispatch = lambda *args: self.api.calls.append('dispatch')
        self.assertEqual(self.run_sync()['status'], 'blocked')
        self.assertEqual(self.api.calls.count('dispatch'), 1)
        self.assertEqual(self.api.prs, [])

    def test_only_exact_observed_trusted_success_satisfies_validation(self):
        variants = [('main', '9'*40), ('head', '9'*40), ('operation', '9'*64),
                    ('event', 'push'), ('workflow', 'candidate.yml'),
                    ('status', 'queued'), ('conclusion', 'failure'), ('id', None)]
        for key, value in variants:
            with self.subTest(key=key):
                self.api = FakeGitHub()
                original = self.api.dispatch
                def wrong(operation, head):
                    original(operation, head)
                    self.api.runs[-1][key] = value
                self.api.dispatch = wrong
                result = self.run_sync()
                self.assertEqual(result['status'], 'blocked')
                self.assertEqual(self.api.prs, [])
        self.api = FakeGitHub()
        self.api.workflow = lambda main: {'sha256': '9'*64, 'main': main}
        self.assertEqual(self.run_sync()['status'], 'blocked')
        self.assertEqual(self.api.calls, [])

    def test_accepted_but_lost_response_is_read_back_without_duplicate(self):
        module = importlib.import_module('publication_remote')
        for method in ('advance', 'dispatch', 'create_pull'):
            with self.subTest(method=method):
                self.api = FakeGitHub()
                original = getattr(self.api, method)
                def lost(*args):
                    original(*args)
                    raise module.RemoteError('transport timeout', uncertain=True)
                setattr(self.api, method, lost)
                result = self.run_sync()
                self.assertEqual(result['status'], 'ready')
                self.assertEqual(len(self.api.prs), 1)
                self.assertEqual(self.api.calls.count('create_pull'), 1)
                self.assertEqual(self.api.calls.count('dispatch'), 1)

    def test_drift_coalesces_latest_pins_and_is_bounded(self):
        calls = 0
        original = self.api.refs
        def drift():
            nonlocal calls
            calls += 1
            self.api.state['main'] = format(calls, '040x')
            return original()
        self.api.refs = drift
        result = self.run_sync()
        self.assertEqual(result['status'], 'stale')
        self.assertEqual(result['retries'], 3)
        self.assertEqual(self.api.calls, [])

    def test_wrong_branch_or_pull_ownership_and_closed_operation_stop(self):
        for mutation in ('owner', 'base', 'duplicate', 'closed', 'branch'):
            with self.subTest(mutation=mutation):
                self.api = FakeGitHub()
                self.run_sync()
                if mutation in ('owner', 'base'):
                    self.api.prs[0][mutation] = 'unrelated'
                elif mutation == 'duplicate':
                    self.api.prs.append(copy.deepcopy(self.api.prs[0]))
                elif mutation == 'closed':
                    self.api.prs[0]['state'] = 'closed'
                else:
                    self.api.state['branch'] = '9'*40
                    self.api.commits['9'*40] = {'owner': 'unrelated', 'tree': '3'*40}
                self.api.calls.clear()
                result = self.run_sync()
                self.assertEqual(result['status'], 'blocked')
                self.assertEqual(self.api.calls, [])

    def test_missing_authority_or_activation_prerequisites_cannot_write(self):
        for options in ({'authorized': False}, {'activation': {}},
                        {'activation': dict(activation(), latest_base_verified=False)},
                        {'activation': dict(activation(), repository='other/repo')}):
            with self.subTest(options=options):
                result = self.run_sync(**options)
                self.assertEqual(result['status'], 'blocked')
                self.assertEqual(self.api.calls, [])

    def test_contained_main_noop_does_not_create_branch_or_pull(self):
        module = importlib.import_module('publication_remote')
        result = module.run_sync(self.api, lambda refs: {'status': 'no-op'},
            repository='owner/example', policy='b'*64, state_dir=Path(self.tmp.name),
            activation=activation(), authorized=True)
        self.assertEqual(result['status'], 'no-op')
        self.assertEqual(self.api.calls, [])

    def test_repeat_event_updates_at_most_one_owned_pull(self):
        first = self.run_sync()
        self.assertEqual(first['status'], 'ready')
        self.assertEqual(first['run_id'], 456)
        second = self.run_sync()
        self.assertEqual(second['status'], 'ready')
        self.assertEqual(len(self.api.prs), 1)
        self.assertEqual(self.api.calls.count('create_pull'), 1)
        self.assertEqual(self.api.state['main'], '1'*40)
        self.assertEqual(self.api.state['staging'], '2'*40)


if __name__ == '__main__':
    unittest.main()
