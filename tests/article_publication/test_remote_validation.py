"""P12 native trusted controller/build surface, separate from live CI/P13."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
MAIN = '5e6c889c808e7ef4cb83493bf06f8a70dd055b41'
STAGING = '612924848ca13663bb2af64e32638fbabedb1685'
CLI = ROOT/'scripts/staging-sync-remote.py'


class TrustedRemoteValidationTests(unittest.TestCase):
    def test_validation_refuses_writer_credentials_before_candidate_execution(self):
        with tempfile.TemporaryDirectory(prefix='sync-no-writer-') as tmp:
            directory = Path(tmp)
            registry = directory/'registry.json'; registry.write_text('{}')
            runtime = directory/'runtime.json'; runtime.write_text('{}')
            operation = directory/'operation.json'; operation.write_text('{}')
            env = dict(os.environ, PUBLICATION_WRITER_TOKEN='synthetic-must-not-reach-build')
            result = subprocess.run([sys.executable,str(CLI),'validate',
                '--registry',str(registry),'--registry-sha256',hashlib.sha256(registry.read_bytes()).hexdigest(),
                '--runtime',str(runtime),'--runtime-sha256',hashlib.sha256(runtime.read_bytes()).hexdigest(),
                '--policy-sha256',hashlib.sha256((ROOT/'maintenance/publication-workflow/engineering-v1.json').read_bytes()).hexdigest(),
                '--operation-record',str(operation),'--head','0'*40,'--build-output',str(directory/'build')],
                capture_output=True,text=True,env=env)
            self.assertEqual(result.returncode,2,result.stdout+result.stderr)
            self.assertIn('credentials',json.loads(result.stdout)['reason'])
            self.assertNotIn('synthetic-must-not-reach-build',result.stdout+result.stderr)
            self.assertFalse((directory/'build').exists())

    def test_dispatch_payload_is_data_and_cannot_execute_shell(self):
        with tempfile.TemporaryDirectory(prefix='sync-untrusted-input-') as tmp:
            sentinel=Path(tmp)/'must-not-execute'
            payload={'operation':'$(touch '+str(sentinel)+')', 'main':'1'*40,'staging':'2'*40,
                     'head':'3'*40,'tree':'4'*40,'policy':'a'*64}
            env=dict(os.environ,UNTRUSTED_INPUTS=json.dumps(payload))
            result=subprocess.run([sys.executable,str(CLI),'validate','--dispatch-inputs-env',
                'UNTRUSTED_INPUTS','--repository','owner/example'],capture_output=True,text=True,env=env)
            self.assertEqual(result.returncode,2,result.stdout+result.stderr)
            self.assertIn('digest mismatch',json.loads(result.stdout)['reason'])
            self.assertFalse(sentinel.exists())

    def test_real_trusted_main_validation_and_isolated_staging_build(self):
        # This is an explicitly synthetic future-main graph, not a remote CI run.
        dependencies=Path(os.environ.get('PUBLICATION_TEST_DEPENDENCIES','/unavailable'))
        self.assertTrue(dependencies.is_dir(),'reviewed installed dependencies required; no skip')
        node=shutil.which('node')
        self.assertIsNotNone(node,'reviewed installed Node required; no skip')
        with tempfile.TemporaryDirectory(prefix='sync-trusted-build-') as tmp:
            directory=Path(tmp).resolve(); projections=directory/'projections'
            prepared=subprocess.run([sys.executable,str(ROOT/'scripts/publication-baseline.py'),
                'prepare','--output',str(projections)],capture_output=True,text=True)
            self.assertEqual(prepared.returncode,0,prepared.stdout+prepared.stderr)
            control=projections/'main'; staging=projections/'staging'
            def git(repo,*args,data=None):
                return subprocess.check_output(['git','-C',str(repo),*args],input=data).decode().strip()
            def commit(repo,parent):
                git(repo,'add','--all')
                sha=git(repo,'-c','user.name=Synthetic fixture','-c','user.email=fixture@example.invalid',
                        'commit-tree',git(repo,'write-tree'),'-p',parent,'-m','Synthetic future controller')
                git(repo,'update-ref','HEAD',sha)
                return sha
            main=commit(control,MAIN);stage=commit(staging,STAGING)
            git(control,'-c','protocol.file.allow=always','fetch','--no-tags',str(staging),stage)
            git(control,'update-ref','refs/heads/main',main)
            git(control,'update-ref','refs/heads/staging',stage)
            for role,sha in [('main',main),('staging',stage)]:
                git(control,'update-ref','refs/remotes/origin/'+role,sha)
            sys.path.insert(0,str(ROOT/'scripts'))
            import publication_remote_git as trusted
            sync=trusted.load('staging-sync.py')
            trees={role:sync.identities(control,sha) for role,sha in [('main',main),('staging',stage)]}
            m0=json.loads((ROOT/'.proj.specs/0012-publication-workflow/implementation/T-0013/M0-inventory.proposed.json').read_bytes())
            candidates=[{'id':c['id'],'source':{'ref':'staging','sha':stage},
                         'paths':{p:trees['staging'][p] for p in c['paths']}} for c in m0['candidates']]
            owned={p for c in candidates for p in c['paths']}
            delta={p for p in set(trees['main'])|set(trees['staging']) if trees['main'].get(p)!=trees['staging'].get(p)}
            registry={'version':1,'target':'staging','repository':str(control),
                'main':{'ref':'main','sha':main},'staging':{'ref':'staging','sha':stage},
                'trees':trees,'candidates':candidates,'engineering':sorted(delta-owned),
                'checks':{p:e for p,e in trees['staging'].items()
                          if p.startswith('maintenance/harness-adoption/') or p in sync.PROTECTED_HISTORY}}
            policy=hashlib.sha256((control/'maintenance/publication-workflow/engineering-v1.json').read_bytes()).hexdigest()
            result=trusted.LocalPreparation(registry,repository='owner/example',policy=policy,
                                             directory=directory/'prepared')({'main':main,'staging':stage,'branch':None})
            self.assertEqual(result['status'],'ready',result)
            git(control,'-c','protocol.file.allow=always','fetch','--no-tags',result['store'],result['head'])
            operation=trusted.operation_for('owner/example',policy,{'main':main,'staging':stage},result['tree'])
            operation_file=directory/'operation.json';operation_file.write_text(json.dumps(operation))
            registry_file=directory/'registry.json';registry_file.write_text(json.dumps(registry))
            runtime_file=directory/'runtime.json';runtime_file.write_text(json.dumps({'version':1,
                'node':node,'node_version':'v24.13.0','dependencies':str(dependencies)}))
            env={k:v for k,v in os.environ.items() if k not in ('PUBLICATION_WRITER_TOKEN','GH_TOKEN','GITHUB_TOKEN')}
            checked=subprocess.run([sys.executable,str(control/'scripts/staging-sync-remote.py'),'validate',
                '--policy-sha256',policy,'--operation-record',str(operation_file),'--head',result['head'],
                '--registry',str(registry_file),'--registry-sha256',hashlib.sha256(registry_file.read_bytes()).hexdigest(),
                '--runtime',str(runtime_file),'--runtime-sha256',hashlib.sha256(runtime_file.read_bytes()).hexdigest(),
                '--build-output',str(directory/'build')],capture_output=True,text=True,env=env)
            self.assertEqual(checked.returncode,0,checked.stdout+checked.stderr)
            report=json.loads(checked.stdout)
            self.assertEqual(report['status'],'pass')
            self.assertEqual(report['native']['target_role'],'staging')
            self.assertEqual(report['build']['isolation'],{'inside':True,'outside_read':'denied',
                'outside_write':'denied','network':'denied'})
            self.assertFalse(report['publishable'])
            evidence=os.environ.get('PUBLICATION_TEST_EVIDENCE')
            if evidence:
                output=Path(evidence)/('T16-'+ROOT.name+'.json');output.parent.mkdir(parents=True,exist_ok=True)
                output.write_text(json.dumps(report,indent=2)+'\n')


if __name__ == '__main__':
    unittest.main()
