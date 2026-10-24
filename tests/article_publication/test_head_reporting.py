"""PC-01–07 local Git + public REST adapter; never live GitHub/P13 proof."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from article_publication import test_staging_sync as sync_fixture
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import publication_remote as remote

WORKFLOW = '.github/workflows/staging-sync-validate.yml'
WORKFLOW_RAW = b'name: inert validation\non: workflow_dispatch\n'
POLICY_RAW = b'{"version":1,"fixture":"independently pinned source"}\n'


class Replay:
    """External REST seam with mutable server state, not an internal module mock."""
    def __init__(self, fixture):
        self.f = fixture
        self.calls = []
        self.checks = []
        self.mutate = None
        self.unknown = False
        self.visible = True
        self.run = {'id':71,'run_attempt':1,'event':'workflow_dispatch','head_sha':fixture.main,
            'head_branch':'main','path':WORKFLOW,'status':'completed','conclusion':'success',
            'repository':{'full_name':'owner/example'},
            'head_repository':{'full_name':'owner/example'},
            'display_title':'staging-sync:'+fixture.operation['id']+':'+fixture.head}
        self.protection = {'required_status_checks':{'strict':True,'checks':[
            {'context':'0x1DEA-publication-validation','app_id':15368}]},
            'enforce_admins':{'enabled':True}}
    def __call__(self, method, endpoint, data=None):
        self.calls.append((method,endpoint,copy.deepcopy(data)))
        suffix=endpoint.removeprefix('repos/owner/example/')
        if self.mutate:
            self.mutate(method,suffix)
        if method=='POST' and suffix=='check-runs':
            row=dict(data,id=81,app={'id':15368})
            self.checks.append(row)
            row.update(getattr(self,'report_mutation',{}))
            if self.unknown: raise remote.RemoteError('SYNTHETIC-SECRET must stay redacted',uncertain=True)
            return copy.deepcopy(row)
        if method!='GET': raise AssertionError('forbidden REST mutation '+endpoint)
        if suffix=='pulls/9': return {'number':9,'state':'open','base':{'ref':'staging','sha':self.f.pin('staging')},'head':{'sha':self.f.head,'ref':remote.BRANCH,'repo':{'full_name':'owner/example'}}}
        if suffix.startswith('git/ref/heads/'):
            role=suffix.removeprefix('git/ref/heads/')
            return {'object':{'sha':self.f.pin(role)}}
        if suffix.startswith('git/commits/'):
            sha=suffix.removeprefix('git/commits/')
            return {'tree':{'sha':self.f.git('show','-s','--format=%T',sha)},'parents':[{'sha':s} for s in self.f.git('show','-s','--format=%P',sha).split()]}
        if suffix.startswith('contents/'):
            import base64
            name,ref=suffix.removeprefix('contents/').split('?ref=')
            raw=subprocess.check_output(['git','-C',str(self.f.repo),'show',ref+':'+name])
            return {'encoding':'base64','content':base64.b64encode(raw).decode()}
        if suffix.startswith('actions/workflows/staging-sync-validate.yml/runs?'):
            return {'workflow_runs':[copy.deepcopy(self.run)]*(2 if getattr(self,'duplicate',False) else 1)}
        if suffix=='actions/runs/71': return copy.deepcopy(self.run)
        if suffix.startswith('commits/') and '/check-runs?' in suffix:
            return {'check_runs':copy.deepcopy(self.checks) if self.visible else []}
        if suffix.startswith('check-runs/'):
            matches=[r for r in self.checks if r['id']==int(suffix.split('/')[-1])]
            if len(matches)!=1:raise remote.RemoteError('check unavailable',status=404)
            return copy.deepcopy(matches[0])
        if suffix=='branches/staging/protection': return copy.deepcopy(self.protection)
        if suffix.startswith('rulesets?'):
            if 'includes_parents=true' not in suffix:raise AssertionError('incomplete ruleset inventory')
            return copy.deepcopy(getattr(self,'ruleset_rows',[]))
        if suffix.startswith('rulesets/'):
            key=int(suffix.split('/')[1].split('?')[0])
            return copy.deepcopy(self.ruleset_details[key])
        if suffix=='collaborators/limited-landing/permission': return copy.deepcopy(getattr(self,'actor',{'permission':'write','role_name':'write','user':{'login':'limited-landing','id':23,'site_admin':False}}))
        raise AssertionError('unhandled REST read '+suffix)


class HeadReportingTests(unittest.TestCase):
    def setUp(self):
        self.f=sync_fixture.StagingSyncTests();self.f.setUp();self.addCleanup(self.f.doCleanups)
        self.repo=self.f.repo
        self.f.put(WORKFLOW,WORKFLOW_RAW);self.f.put('maintenance/publication-workflow/engineering-v1.json',POLICY_RAW)
        self.main=self.f.commit();self.stage=self.pin('staging')
        self.tree=self.git('rev-parse','main^{tree}')
        self.operation=remote.operation_for('owner/example',hashlib.sha256(POLICY_RAW).hexdigest(),{'main':self.main,'staging':self.stage},self.tree)
        raw=('tree '+self.tree+'\nparent '+self.main+'\nparent '+self.stage+'\nauthor Fixture <fixture@example.invalid> 1 +0000\ncommitter Fixture <fixture@example.invalid> 1 +0000\n\nSynthetic candidate\n').encode()
        self.head=subprocess.check_output(['git','-C',str(self.repo),'hash-object','-t','commit','-w','--stdin'],input=raw).decode().strip()
        self.expected={'repository':'owner/example','pull':9,'operation':self.operation,'head':self.head,
            'workflow':WORKFLOW,'workflow_sha256':hashlib.sha256(WORKFLOW_RAW).hexdigest(),
            'run_id':71,'run_attempt':1,'check':'0x1DEA-publication-validation','reporter_app_id':15368,'landing_actor':'limited-landing','landing_actor_id':23}
        self.server=Replay(self)
    def git(self,*args):return subprocess.check_output(['git','-C',str(self.repo),*args],text=True).strip()
    def pin(self,name):return self.git('rev-parse',name)
    def report(self,**options):
        import publication_reporting as reporting
        api=reporting.GitHubReportingAdapter('owner/example',self.server)
        reporter=reporting.CheckReporter('owner/example',self.server,app_id=15368,role='reporter')
        return reporting.report_validation(api,reporter,self.expected,state_dir=getattr(self,'report_state',self.f.root/'report-state'),**options)
    def test_exact_trusted_success_reports_only_candidate_head_and_reads_back_check(self):
        """PC-01: dispatched main run is distinct from the independently read candidate."""
        result=self.report()
        self.assertEqual(result['status'],'ready',result)
        self.assertTrue(result['local_ready']);self.assertFalse(result['live_ready'])
        self.assertFalse(result['publishable'])
        posts=[c for c in self.server.calls if c[0]!='GET']
        self.assertEqual(len(posts),1)
        self.assertEqual(posts[0][1],'repos/owner/example/check-runs')
        self.assertEqual(posts[0][2]['head_sha'],self.head)
        self.assertNotEqual(posts[0][2]['head_sha'],self.main)
        self.assertEqual(posts[0][2]['name'],'0x1DEA-publication-validation')
        self.assertEqual(posts[0][2]['conclusion'],'success')
        self.assertEqual(result['check_id'],81)
        self.assertEqual(result['surface'],'local API contract; live enforcement unverified')

    def test_non_success_missing_duplicate_and_wrong_run_bindings_never_report_success(self):
        """PC-02: ack-only and ambiguous run inventory cannot become candidate success."""
        for case in ('queued','in_progress','failure','cancelled','skipped','neutral','timed_out',
                     'missing','duplicate','wrong-main','wrong-event','wrong-attempt','wrong-repo',
                     'wrong-head-repository','wrong-workflow','wrong-title','denied'):
            with self.subTest(case=case):
                self.server=Replay(self)
                if case in ('queued','in_progress'):self.server.run['status']=case
                elif case in ('failure','cancelled','skipped','neutral','timed_out'):self.server.run['conclusion']=case
                elif case=='missing':self.server.run=None
                elif case=='duplicate':self.server.duplicate=True
                elif case=='wrong-main':self.server.run['head_sha']='0'*40
                elif case=='wrong-event':self.server.run['event']='pull_request'
                elif case=='wrong-attempt':self.server.run['run_attempt']=2
                elif case=='wrong-repo':self.server.run['repository']['full_name']='foreign/repo'
                elif case=='wrong-head-repository':self.server.run['head_repository']['full_name']='foreign/repo'
                elif case=='wrong-workflow':self.server.run['path']='.github/workflows/untrusted.yml'
                elif case=='wrong-title':self.server.run['display_title']='unbound'
                elif case=='denied':
                    def denied(method,suffix):raise remote.RemoteError('denied',status=403)
                    self.server.mutate=denied
                result=self.report()
                self.assertEqual(result['status'],'blocked',result)
                self.assertFalse(result['local_ready']);self.assertFalse(result['live_ready'])
                self.assertFalse(any(c[0]!='GET' for c in self.server.calls),self.server.calls)
        baseline=copy.deepcopy(self.expected)
        for field in ('id','tree','policy','main','staging'):
            self.expected=copy.deepcopy(baseline);self.server=Replay(self)
            self.expected['operation'][field]='0'*(64 if field in ('id','policy') else 40)
            result=self.report()
            self.assertEqual(result['status'],'blocked',result)
            self.assertFalse(any(c[0]=='POST' for c in self.server.calls))
        self.expected=copy.deepcopy(baseline);self.server=Replay(self)
        self.expected['operation']['version']=True
        self.assertEqual(self.report()['status'],'blocked')
        self.assertFalse(any(c[0]=='POST' for c in self.server.calls))
        self.expected=baseline

    def test_reporter_role_identity_permission_and_credential_boundaries(self):
        """PC-03: a configured reporter is separate from writer/build authority."""
        import publication_reporting as reporting
        from unittest.mock import patch
        api=reporting.GitHubReportingAdapter('owner/example',self.server)
        for role,app in [('writer',15368),('validator',15368),('reporter',99)]:
            with self.subTest(role=role,app=app):
                self.server.calls.clear()
                reporter=reporting.CheckReporter('owner/example',self.server,app_id=app,role=role)
                result=reporting.report_validation(api,reporter,self.expected,state_dir=self.f.root/'report-state')
                self.assertEqual(result['status'],'blocked',result)
                self.assertFalse(any(c[0]!='GET' for c in self.server.calls))
        import publication_remote_git as validator
        with patch.dict(os.environ,{'PUBLICATION_REPORTER_TOKEN':'REPORTER-SECRET'}):
            with self.assertRaisesRegex(ValueError,'credentials'):
                validator.validate_operation({},self.head,{}, {},'0'*64,self.f.root/'must-not-build')
        self.assertFalse((self.f.root/'must-not-build').exists())
        for status in (401,403):
            self.report_state=self.f.root/('permission-'+str(status))
            self.server=Replay(self)
            def denied(method,suffix):
                if method=='POST':raise remote.RemoteError('REPORTER-SECRET',status=status)
            self.server.mutate=denied
            result=self.report()
            self.assertEqual(result['status'],'blocked')
            self.assertNotIn('REPORTER-SECRET',json.dumps(result))
            self.assertFalse(self.server.checks)
            self.assertEqual(len([c for c in self.server.calls if c[0]=='POST']),1)


    def test_candidate_head_drift_expires_old_readiness_before_or_after_reporting(self):
        """PC-04: H1→H2 cannot reuse an H1 success or attempt any merge."""
        original=self.head
        for phase in ('before-write','during-write','after-readback'):
            with self.subTest(phase=phase):
                self.report_state=self.f.root/('report-'+phase)
                self.head=original;self.server=Replay(self);changed=[False]
                def advance(method,suffix):
                    trigger=((phase=='before-write' and suffix.startswith('commits/') and not self.server.checks)
                        or (phase=='during-write' and method=='POST')
                        or (phase=='after-readback' and suffix=='pulls/9' and bool(self.server.checks)))
                    if trigger and not changed[0]:
                        changed[0]=True
                        raw=('tree '+self.tree+'\nparent '+original+'\nauthor Fixture <fixture@example.invalid> 2 +0000\ncommitter Fixture <fixture@example.invalid> 2 +0000\n\nH2 fixture\n').encode()
                        self.head=subprocess.check_output(['git','-C',str(self.repo),'hash-object','-t','commit','-w','--stdin'],input=raw).decode().strip()
                self.server.mutate=advance
                result=self.report()
                self.assertEqual(result['status'],'blocked',result)
                self.assertIn('head',result['reason'])
                self.assertFalse(result['local_ready'])
                self.assertTrue(result['fresh_validation_required'])
                if phase=='before-write':self.assertFalse(any(c[0]=='POST' for c in self.server.calls))
                self.assertFalse(any('merge' in c[1] for c in self.server.calls))
        self.head=original


    def test_staging_or_capability_drift_and_local_only_evidence_refuse_live_readiness(self):
        """PC-05: strict/source/actor requirements are observed, never asserted by candidate data."""
        for case in ('missing-strict','wrong-check','wrong-app','admins-bypass','admin-actor','wrong-actor','staging-drift','protection-after'):
            with self.subTest(case=case):
                self.server=Replay(self)
                if case=='missing-strict':self.server.protection['required_status_checks']['strict']=False
                elif case=='wrong-check':self.server.protection['required_status_checks']['checks'][0]['context']='unrelated'
                elif case=='wrong-app':self.server.protection['required_status_checks']['checks'][0]['app_id']=99
                elif case=='admins-bypass':self.server.protection['enforce_admins']['enabled']=False
                elif case in ('admin-actor','wrong-actor'):
                    self.server.actor={'permission':'admin' if case=='admin-actor' else 'write','role_name':'admin' if case=='admin-actor' else 'write','user':{'login':'other' if case=='wrong-actor' else 'limited-landing','id':23,'site_admin':False}}
                elif case=='staging-drift':self.git('update-ref','refs/heads/staging',self.main)
                elif case=='protection-after':
                    def change(method,suffix):
                        if self.server.checks:self.server.protection['required_status_checks']['checks'][0]['app_id']=99
                    self.server.mutate=change
                result=self.report()
                self.assertEqual(result['status'],'blocked',result)
                self.assertFalse(result['local_ready']);self.assertFalse(result['live_ready'])
                if case=='staging-drift':
                    self.assertIn('staging',result['reason']);self.git('update-ref','refs/heads/staging',self.stage)
                if case!='protection-after':self.assertFalse(any(c[0]=='POST' for c in self.server.calls))
        self.server=Replay(self)
        self.expected['capability_verified']=True
        result=self.report(live=True)
        self.assertFalse(result['live_ready'])
        self.assertEqual(result['status'],'blocked')
        self.assertIn('live capability',result['reason'])
        self.assertFalse(any(c[0]=='POST' for c in self.server.calls))
        self.expected.pop('capability_verified')


    def test_main_policy_workflow_drift_keeps_candidate_head_but_expires_binding(self):
        """PC-06: unchanged candidate head cannot preserve an outdated source binding."""
        import base64
        original=self.main
        for case in ('main','main-during-read','policy','workflow'):
            with self.subTest(case=case):
                self.server=Replay(self)
                if case=='main':self.git('update-ref','refs/heads/main',self.stage)
                elif case=='main-during-read':
                    def drift(method,suffix):
                        if suffix.startswith('collaborators/') and self.server.checks:
                            self.git('update-ref','refs/heads/main',self.stage)
                    self.server.mutate=drift
                else:
                    base=self.server
                    class SwappedContent:
                        def __call__(proxy,method,endpoint,data=None):
                            result=base(method,endpoint,data)
                            name='engineering-v1.json' if case=='policy' else 'staging-sync-validate.yml'
                            if 'contents/' in endpoint and name in endpoint:
                                result['content']=base64.b64encode(b'changed source').decode()
                            return result
                    import publication_reporting as reporting
                    api=reporting.GitHubReportingAdapter('owner/example',SwappedContent())
                    reporter=reporting.CheckReporter('owner/example',self.server,app_id=15368,role='reporter')
                    result=reporting.report_validation(api,reporter,self.expected,state_dir=self.f.root/'report-state')
                if case.startswith('main'):result=self.report()
                self.assertEqual(result['status'],'blocked',result)
                self.assertIn('main' if case.startswith('main') else case,result['reason'])
                self.assertTrue(result['fresh_validation_required'])
                self.assertEqual(self.expected['head'],self.head)
                self.git('update-ref','refs/heads/main',original)


    def test_unknown_write_is_read_back_without_duplicate_and_old_results_are_not_locks(self):
        """PC-07: durable unknown-outcome recovery and repeated decision revalidation."""
        self.server.unknown=True
        first=self.report()
        self.assertEqual(first['status'],'ready',first)
        self.assertEqual(len([c for c in self.server.calls if c[0]=='POST']),1)
        second=self.report()
        self.assertEqual(second['status'],'ready',second)
        self.assertEqual(len([c for c in self.server.calls if c[0]=='POST']),1)
        self.assertIn('point-in-time',second['guarantee'])
        self.git('update-ref','refs/heads/main',self.stage)
        stale=self.report()
        self.assertEqual(stale['status'],'blocked')
        self.assertIn('main',stale['reason'])
        self.git('update-ref','refs/heads/main',self.main)
        self.server=Replay(self);self.server.unknown=True;self.server.visible=False
        # A distinct approved run is a distinct durable reporting intent.
        self.expected['run_attempt']=2;self.server.run['run_attempt']=2
        for _ in range(2):
            result=self.report()
            self.assertEqual(result['status'],'blocked',result)
            self.assertNotIn('SYNTHETIC-SECRET',json.dumps(result))
        self.assertEqual(len([c for c in self.server.calls if c[0]=='POST']),1)
        self.server.visible=True
        recovered=self.report()
        self.assertEqual(recovered['status'],'ready',recovered)
        self.assertEqual(len([c for c in self.server.calls if c[0]=='POST']),1)
        self.server.duplicate=True
        expired=self.report()
        self.assertEqual(expired['status'],'blocked')
        self.assertFalse(expired['local_ready'])
        self.assertFalse(any('merge' in c[1] for c in self.server.calls))


        for attempt,mutation in enumerate(({'app':{'id':99}},{'head_sha':'0'*40},
                {'external_id':'foreign'},{'status':'queued'},{'conclusion':'failure'},{'id':0}),start=3):
            with self.subTest(readback=mutation):
                self.server=Replay(self);self.expected['run_attempt']=attempt;self.server.run['run_attempt']=attempt
                self.server.report_mutation=mutation
                result=self.report()
                self.assertEqual(result['status'],'blocked',result)
                self.assertFalse(result['local_ready'])
                self.assertEqual(len([c for c in self.server.calls if c[0]=='POST']),1)

    def test_report_from_real_sealed_validator_inputs_and_finite_workflow_admission(self):
        """PC-01/03/06: actual A+B public inputs feed this R contract, not fixture capability flags."""
        import publication_reporting as reporting
        import publication_jobs as jobs
        from publication_remote_git import LocalPreparation,load
        from publication_workflows import WorkflowAdmission
        from article_publication import test_workflow_admission as admission_fixture
        import shutil
        w=admission_fixture.WorkflowAdmissionTests();w.setUp();self.addCleanup(w.doCleanups)
        # Current receipt metadata needs its actual trusted named histories; inert
        # future main remains based on real main, with no staging candidate parent.
        tree=w.git('write-tree').decode().strip()
        raw=('tree '+tree+'\nparent '+w.main+'\nauthor Fixture <fixture@example.invalid> 1 +0000\ncommitter Fixture <fixture@example.invalid> 1 +0000\n\nSynthetic reporting source\n').encode()
        w.main=w.git('hash-object','-t','commit','-w','--stdin',data=raw).decode().strip()
        w.git('update-ref','HEAD',w.main);w.git('update-ref','refs/heads/main',w.main)
        w.grant['main']=w.main;w.save_grant()
        native=w.cli(native=True);self.assertEqual(native.returncode,0,native.stdout+native.stderr)
        admission=WorkflowAdmission(w.admission,hashlib.sha256(w.admission.read_bytes()).hexdigest(),'owner/example',w.main)
        sync=load('staging-sync.py');stage=w.git('rev-parse','staging').decode().strip()
        trees={role:sync.identities(w.control,sha) for role,sha in [('main',w.main),('staging',stage)]}
        m0=json.loads((w.control/'.proj.specs/0012-publication-workflow/implementation/T-0013/M0-inventory.proposed.json').read_bytes())
        candidates=[{'id':c['id'],'source':{'ref':'staging','sha':stage},'paths':{n:trees['staging'][n] for n in c['paths']}} for c in m0['candidates']]
        owned={n for c in candidates for n in c['paths']}
        delta={n for n in set(trees['main'])|set(trees['staging']) if trees['main'].get(n)!=trees['staging'].get(n)}
        registry={'version':1,'target':'staging','repository':str(w.control),'main':{'ref':'main','sha':w.main},'staging':{'ref':'staging','sha':stage},'trees':trees,'candidates':candidates,'engineering':sorted(delta-owned),'checks':{n:trees['main'][n] if n in {
            # Independently pinned current main owns the reviewed fifth-package
            # inventories. All other protected checks retain staging ownership.
            'maintenance/harness-adoption/generated-writing-manifest.json',
            'maintenance/harness-adoption/runtime-source-policy.json',
        } else v for n,v in trees['staging'].items() if n.startswith('maintenance/harness-adoption/') or n in sync.PROTECTED_HISTORY}}
        state=w.directory/'durable';state.mkdir(mode=0o700)
        identity=state/'identity.json';identity.write_bytes(remote.canonical({'version':1,'repository':'owner/example','store_id':'c'*64}));identity.chmod(0o400)
        registry_file=w.directory/'registry.json';registry_file.write_bytes(remote.canonical(registry))
        runtime_file=w.directory/'runtime.json';runtime_file.write_bytes(remote.canonical({'version':1,'node':str(Path(shutil.which('node')).resolve()),'node_version':'v24.13.0','dependencies':str(Path(os.environ['PUBLICATION_TEST_DEPENDENCIES']).resolve())}))
        digest=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
        policy=digest(w.control/'maintenance/publication-workflow/engineering-v1.json')
        config={'version':1,'repository':'owner/example','role':'validator','main':w.main,'staging':stage,'policy_sha256':policy,'source':str(w.control),'registry':{'path':str(registry_file),'sha256':digest(registry_file)},'runtime':{'path':str(runtime_file),'sha256':digest(runtime_file)},'pnpm':{'path':str(Path(shutil.which('pnpm')).resolve()),'version':'10.28.0'},'snapshot_root':str(w.directory/'validator-inputs'),'state_directory':str(state),'state_identity_sha256':digest(identity)}
        config_file=w.directory/'config.json';config_file.write_bytes(remote.canonical(config))
        job=jobs.materialize_job(config_file,digest(config_file),repository='owner/example',role='validator')
        self.addCleanup(Path(job['snapshot_root']).chmod,0o700)
        prepared=LocalPreparation(registry,repository='owner/example',policy=policy,directory=w.directory/'prepare')({'main':w.main,'staging':stage,'branch':None})
        self.assertEqual(prepared['status'],'ready',prepared)
        w.git('fetch',prepared['store'],prepared['head'])
        self.repo=w.control;self.main=w.main;self.stage=stage;self.operation=job['operation'];self.head=prepared['head'];self.tree=prepared['tree']
        self.server=Replay(self)
        report_config={k:v for k,v in self.expected.items() if k not in ('operation','head','workflow_sha256')}
        report_config['head']=self.head
        api=reporting.GitHubReportingAdapter('owner/example',self.server)
        reporter=reporting.CheckReporter('owner/example',self.server,app_id=15368,role='reporter')
        result=reporting.report_from_job(api,reporter,control=w.control,snapshot_root=job['snapshot_root'],binding_sha256=job['binding_sha256'],admission=admission,config=report_config)
        self.assertEqual(result['status'],'ready',result)
        self.assertFalse(result['live_ready']);self.assertEqual(len(self.server.checks),1)
        self.assertEqual(self.server.checks[0]['head_sha'],prepared['head'])
        self.assertFalse((w.directory/'workflow-executed').exists())
        admission.path.write_bytes(b'changed external source')
        before=len(self.server.calls)
        refused=reporting.report_from_job(api,reporter,control=w.control,snapshot_root=job['snapshot_root'],binding_sha256=job['binding_sha256'],admission=admission,config=report_config)
        self.assertEqual(refused['status'],'blocked')
        self.assertEqual(len(self.server.calls),before)


    def test_explicit_reporter_credential_reaches_only_filtered_check_transport(self):
        """PC-03: no implicit credential fallback and no reporter secret in build processes."""
        import publication_reporting as reporting
        from unittest.mock import patch
        from types import SimpleNamespace
        calls=[]
        def process(command,**kwargs):
            calls.append((command,kwargs))
            return SimpleNamespace(returncode=0,stdout='HTTP/2.0 201 Created\n\n{}',stderr='')
        with patch.dict(os.environ,{'PATH':os.environ['PATH'],'PUBLICATION_REPORTER_TOKEN':'REPORTER-SECRET'},clear=True):
            reporter=reporting.check_reporter_from_environment('owner/example',15368,self.f.root/'transport',process=process)
            self.assertNotIn('PUBLICATION_REPORTER_TOKEN',os.environ)
            reporter.publish({'name':'only-check','head_sha':self.head,'status':'completed','conclusion':'success','external_id':'a'*64})
        self.assertEqual(len(calls),1)
        self.assertEqual(calls[0][1]['env']['GH_TOKEN'],'REPORTER-SECRET')
        self.assertNotIn('PUBLICATION_WRITER_TOKEN',calls[0][1]['env'])
        self.assertNotIn('REPORTER-SECRET',json.dumps(calls[0][0]))
        self.assertNotIn('REPORTER-SECRET',calls[0][1]['input'])
        for token in ('PUBLICATION_WRITER_TOKEN','GH_TOKEN','GITHUB_TOKEN'):
            with self.subTest(token=token),patch.dict(os.environ,{'PUBLICATION_REPORTER_TOKEN':'REPORTER-SECRET',token:'OTHER-SECRET'},clear=True):
                with self.assertRaisesRegex(ValueError,'credential'):
                    reporting.check_reporter_from_environment('owner/example',15368,self.f.root/'wrong',process=process)
        self.assertEqual(len(calls),1)


    def test_confirmed_check_id_and_journal_identity_are_pinned_across_calls(self):
        """PC-07 review regression: a replacement check is not the confirmed identity."""
        first=self.report();self.assertEqual(first['status'],'ready',first)
        self.server.checks[0]['id']=82
        replaced=self.report()
        self.assertEqual(replaced['status'],'blocked',replaced)
        self.assertTrue(replaced['fresh_validation_required'])
        self.assertEqual(len([c for c in self.server.calls if c[0]=='POST']),1)
        self.server.checks[0]['id']=81
        path=self.f.root/'report-state'/(first['binding']+'.json')
        original=path.read_bytes()
        for value in (None,True,0,-1,'81',82):
            with self.subTest(journal_check_id=value):
                journal=json.loads(original);journal['check_id']=value;path.write_bytes(remote.canonical(journal))
                result=self.report()
                self.assertEqual(result['status'],'blocked',result)
        path.write_bytes(original)
        self.assertEqual(self.report()['status'],'ready')

    def test_first_observed_or_acknowledged_check_id_cannot_change_during_one_call(self):
        """PC-07: initial inventory, pending recovery and known POST all pin identity."""
        for case in ('existing', 'pending', 'acknowledged'):
            with self.subTest(case=case):
                self.report_state=self.f.root/('same-call-'+case)
                self.server=Replay(self)
                first=self.report();self.assertEqual(first['status'],'ready',first)
                path=self.report_state/(first['binding']+'.json')
                if case=='pending':
                    journal=json.loads(path.read_bytes());journal.update(status='pending',check_id=None)
                    path.write_bytes(remote.canonical(journal))
                else:
                    path.unlink()
                if case=='acknowledged':self.server.checks=[]
                self.server.calls=[]
                reads=[]
                def replace_identity(method,suffix):
                    if method=='GET' and suffix.startswith('commits/') and '/check-runs?' in suffix:
                        reads.append(suffix)
                        if len(reads)==2:self.server.checks[0]['id']=82
                self.server.mutate=replace_identity
                replaced=self.report()
                self.assertEqual(replaced['status'],'blocked',replaced)
                self.assertTrue(replaced['fresh_validation_required'])
                self.assertEqual(len([c for c in self.server.calls if c[0]=='POST']),
                                 1 if case=='acknowledged' else 0)
                self.server.mutate=None
                retried=self.report()
                self.assertEqual(retried['status'],'blocked',retried)
                self.assertEqual(len([c for c in self.server.calls if c[0]=='POST']),
                                 1 if case=='acknowledged' else 0)

    def test_independent_non_bypass_observation_is_required_and_config_drift_expires_it(self):
        """PC-05 review regression: standard role plus complete inherited bypass inventory."""
        detail={'id':4,'source_type':'Organization','source':'owner','target':'branch',
                'enforcement':'active','bypass_actors':[],'rules':[]}
        actor={'permission':'write','role_name':'write','user':{'login':'limited-landing','id':23,'site_admin':False}}
        for case in ('missing-role','custom-role','hidden-bypass','bypass-user','bypass-team',
                     'bypass-app','bypass-role','unknown-rule','duplicate-rule','wrong-detail','denied-inventory'):
            with self.subTest(case=case):
                self.report_state=self.f.root/('non-bypass-'+case)
                self.server=Replay(self);self.server.actor=copy.deepcopy(actor)
                self.server.ruleset_rows=[{'id':4}];self.server.ruleset_details={4:copy.deepcopy(detail)}
                if case=='missing-role':self.server.actor.pop('role_name')
                elif case=='custom-role':self.server.actor['role_name']='custom-can-bypass'
                elif case=='hidden-bypass':self.server.ruleset_details[4].pop('bypass_actors')
                elif case.startswith('bypass-'):
                    kinds={'bypass-user':'User','bypass-team':'Team','bypass-app':'Integration','bypass-role':'RepositoryRole'}
                    self.server.ruleset_details[4]['bypass_actors']=[{'actor_type':kinds[case],'actor_id':23,'bypass_mode':'always'}]
                elif case=='unknown-rule':self.server.ruleset_details[4]['enforcement']='unknown'
                elif case=='duplicate-rule':self.server.ruleset_rows.append({'id':4})
                elif case=='wrong-detail':self.server.ruleset_details[4]['id']=5
                else:
                    def denied(method,suffix):
                        if suffix.startswith('rulesets'):raise remote.RemoteError('unavailable bypass evidence',status=403)
                    self.server.mutate=denied
                result=self.report()
                self.assertEqual(result['status'],'blocked',result)
                self.assertFalse(any(c[0]=='POST' for c in self.server.calls))
        self.report_state=self.f.root/'non-bypass-positive'
        self.server=Replay(self);self.server.ruleset_rows=[{'id':4}];self.server.ruleset_details={4:copy.deepcopy(detail)}
        result=self.report();self.assertEqual(result['status'],'ready',result)
        self.server.ruleset_details[4]['rules']=[{'type':'required_signatures'}]
        drifted=self.report()
        self.assertEqual(drifted['status'],'blocked',drifted)
        self.assertTrue(drifted['fresh_validation_required'])
        self.assertEqual(len([c for c in self.server.calls if c[0]=='POST']),1)


if __name__=='__main__':unittest.main()
