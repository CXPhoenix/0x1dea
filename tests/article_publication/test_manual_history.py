"""PD-01–04 public controller/API-adapter contracts with real disposable Git ancestry."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import subprocess
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from article_publication import test_staging_sync as git_fixtures
from article_publication import test_remote_sync as remote_fixtures
import publication_remote as remote


class ManualHistoryTests(unittest.TestCase):
    def setUp(self):
        self.fixture=git_fixtures.StagingSyncTests();self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        f=self.fixture;self.root=f.root
        self.api=remote_fixtures.FakeGitHub()
        self.api.state.update(main=f.main,staging=f.stage)
        self.api.is_ancestor=lambda old,new: subprocess.run(['git','-C',str(f.repo),'merge-base','--is-ancestor',old,new],capture_output=True).returncode==0
        tree=f.git('rev-parse',f.stage+'^{tree}').strip()
        self.pull={'number':28,'state':'closed','base':'staging','base_sha':f.base,
            'head':f.stage,'merge':f.stage,'tree':tree,'branch':remote.BRANCH,
            'repository':'owner/example','owner':None,'operation':None,'merged':True,
            'actor':{'login':'maintainer','id':123,'type':'User'}}
        self.api.prs=[copy.deepcopy(self.pull)]
        self.api.pull_details=lambda number: copy.deepcopy(next(p for p in self.api.prs if p['number']==number))
        self.api.commits[f.stage]={'tree':tree,'parents':[f.base],'owner':None,'operation':None}
        self.receipt=self.root/'owner-receipt.json'
        self.grant=self.root/'manual-history.json'
        self.identity={key:copy.deepcopy(self.pull[key]) for key in
            ('number','base','base_sha','head','merge','tree','branch','repository','actor')}
        self.receipt.write_text(json.dumps({'version':1,'approval':'owner-approved-local-fixture',
            'manual':self.identity})+'\n')
        self.data={'version':1,'repository':'owner/example','branch':remote.BRANCH,
            'manual':self.identity,'approval':{'path':str(self.receipt),'sha256':self.sha(self.receipt)}}

    @staticmethod
    def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

    def admission(self):
        import publication_manual
        self.grant.write_text(json.dumps(self.data)+'\n')
        return publication_manual.ManualHistory(self.grant,self.sha(self.grant),'owner/example',source=self.fixture.repo)

    def run_sync(self, admission=None, prepare=remote_fixtures.prepare):
        return remote.run_sync(self.api,prepare,repository='owner/example',policy='b'*64,
            state_dir=self.root/'journal',activation=remote_fixtures.activation(),authorized=True,
            **({'manual_history':admission} if admission else {}))

    def test_noop_precedes_manual_ownership_but_ready_defaults_to_refusal(self):
        """PD-01: synchronized refs never need a historical ownership exemption."""
        noop=self.run_sync(prepare=lambda refs:{'status':'no-op','reason':'already synchronized'})
        self.assertEqual(noop['status'],'no-op');self.assertEqual(self.api.calls,[])
        refused=self.run_sync()
        self.assertEqual(refused['status'],'blocked');self.assertEqual(self.api.calls,[])

    def test_exact_external_manual_history_continues_without_reassigning_ownership(self):
        """PD-02: exact historical admission excludes one manual pull, never owns it."""
        original=copy.deepcopy(self.api.prs[0]);admission=self.admission()
        for _ in range(2):
            result=self.run_sync(admission)
            self.assertEqual(result['status'],'ready',result)
            self.assertEqual(result['manual_history'][0]['classification'],'manual')
        self.assertEqual(self.api.calls.count('create_pull'),1)
        self.assertEqual(len(self.api.prs),2)
        self.assertEqual(self.api.prs[0],original)
        journal=json.loads(next((self.root/'journal').glob('*.json')).read_bytes())
        self.assertEqual(journal['manual_history'][0]['number'],28)
        self.assertIsNone(self.api.prs[0]['owner'])

    def test_each_manual_binding_drift_and_ambiguous_or_unmerged_pull_refuses(self):
        """PD-03: one exact historical identity, not a broad closed-pull exemption."""
        base=copy.deepcopy(self.pull)
        for field,value in [('repository','other/repo'),('branch','other-branch'),('number',29),
                ('base','main'),('base_sha','9'*40),('head','8'*40),('merge','7'*40),('tree','6'*40),
                ('actor',{'login':'other','id':123,'type':'User'}),
                ('actor',{'login':'maintainer','id':124,'type':'User'}),
                ('actor',{'login':'maintainer','id':123,'type':'Bot'}),
                ('state','open'),('merged',False),('owner',remote.OWNER),('operation','forged')]:
            with self.subTest(field=field,value=value):
                self.api.prs=[copy.deepcopy(base)];self.api.prs[0][field]=value
                refused=self.run_sync(self.admission())
                self.assertEqual(refused['status'],'blocked',refused)
                self.assertEqual(self.api.calls,[])
        self.api.prs=[copy.deepcopy(base),copy.deepcopy(base)]
        self.assertEqual(self.run_sync(self.admission())['status'],'blocked')
        self.api.prs=[copy.deepcopy(base)]
        admission=self.admission();self.receipt.write_text('{}')
        self.assertEqual(self.run_sync(admission)['status'],'blocked')
        self.receipt.write_text(json.dumps({'version':1,'approval':'owner-approved-local-fixture','manual':self.identity})+'\n')
        admission=self.admission();self.grant.write_text('{}')
        self.assertEqual(self.run_sync(admission)['status'],'blocked')
        self.api.pull_details=lambda number:dict(copy.deepcopy(base),tree='0'*40)
        self.assertEqual(self.run_sync(self.admission())['status'],'blocked')
        self.api.pull_details=lambda number:copy.deepcopy(base)
        for authority in ('grant','receipt'):
            with self.subTest(candidate_contained=authority):
                original_grant,original_receipt=self.grant,self.receipt
                self.api.pull_details=lambda number:copy.deepcopy(base)
                if authority=='grant':
                    self.grant=self.fixture.repo/'candidate-grant.json'
                else:
                    self.receipt=self.fixture.repo/'candidate-receipt.json'
                    self.receipt.write_bytes(original_receipt.read_bytes())
                    self.data['approval']['path']=str(self.receipt)
                rejected=self.run_sync(self.admission())
                self.assertEqual(rejected['status'],'blocked',rejected)
                self.assertEqual(self.api.calls,[])
                self.grant,self.receipt=original_grant,original_receipt
                self.data['approval']['path']=str(self.receipt)
        self.api.is_ancestor=lambda *args:False
        self.assertEqual(self.run_sync(self.admission())['status'],'blocked')
        self.assertEqual(self.api.calls,[])

    def test_unrelated_pulls_and_unowned_branch_never_gain_history_ownership(self):
        """PD-04: grant leaves unrelated pulls, owned closed state and branch guards intact."""
        original=copy.deepcopy(self.pull)
        for state in ('open','closed'):
            with self.subTest(unrelated_state=state):
                unrelated=dict(original,number=99,state=state,merged=False)
                self.api.prs=[copy.deepcopy(original),unrelated]
                self.assertEqual(self.run_sync(self.admission())['status'],'blocked')
                self.assertEqual(self.api.calls,[])
        self.api.prs=[copy.deepcopy(original)]
        self.api.state['branch']=self.fixture.stage
        self.assertEqual(self.run_sync(self.admission())['status'],'blocked')
        self.assertEqual(self.api.calls,[])
        # Existing independently proven owned branch recovery stays non-force.
        self.api.state['branch']=None
        self.assertEqual(self.run_sync(self.admission())['status'],'ready')
        self.api.state['branch']=None
        self.api.calls.clear()
        self.assertEqual(self.run_sync(self.admission())['status'],'ready')
        self.assertEqual(self.api.calls.count('create_pull'),0)
        self.assertEqual(self.api.calls.count('advance'),1)
        self.assertEqual(self.api.prs[0],original)
        self.api.prs[1]['state']='closed'
        self.api.calls.clear()
        self.assertEqual(self.run_sync(self.admission())['status'],'blocked')
        self.assertEqual(self.api.calls,[])
