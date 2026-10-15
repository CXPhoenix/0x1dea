"""Owner-authorized dual-target closeout at the native CLI seam (P23/C2)."""
from pathlib import Path
import json
import hashlib
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
MAIN = '5e6c889c808e7ef4cb83493bf06f8a70dd055b41'
STAGING = '612924848ca13663bb2af64e32638fbabedb1685'


class LandedCloseoutTests(unittest.TestCase):
    def test_new_receipts_reject_another_valid_ancestor_even_with_repinning(self):
        with tempfile.TemporaryDirectory(prefix='landed-closeout-negative-') as tmp:
            out=Path(tmp)/'projection'
            result=subprocess.run([sys.executable,str(ROOT/'scripts/publication-baseline.py'),
                                   'prepare','--output',str(out)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            target=out/'main'
            subprocess.run(['git','-C',str(target),'update-ref','refs/heads/staging',STAGING],check=True)
            subprocess.run(['git','-C',str(target),'update-ref','refs/heads/main',MAIN],check=True)
            policy_path=target/'maintenance/publication-workflow/engineering-v1.json'
            original_policy=policy_path.read_bytes()
            for ticket in ('T-0012','T-0014','T-0015'):
                name='.proj.specs/0012-publication-workflow/implementation/dual-landing-20261016/'+ticket+'-landing.json'
                path=target/name;original=path.read_bytes()
                receipt=json.loads(original);receipt['commit']='035783590895a426ee395045829ebc9d50e2b9cf'
                path.write_text(json.dumps(receipt))
                policy=json.loads(original_policy)
                policy['common'][name]['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
                policy_path.write_text(json.dumps(policy))
                result=subprocess.run([sys.executable,str(target/'scripts/verify-harness-adoption.py')],
                                      capture_output=True,text=True)
                self.assertNotEqual(result.returncode,0)
                self.assertIn('unapproved exact closeout identity',result.stderr)
                self.assertEqual(result.stdout,'')
                path.write_bytes(original);policy_path.write_bytes(original_policy)

    def test_trusted_main_validates_staging_without_executing_candidate_code(self):
        with tempfile.TemporaryDirectory(prefix='trusted-sync-native-') as tmp:
            out=Path(tmp)/'projection'
            result=subprocess.run([sys.executable,str(ROOT/'scripts/publication-baseline.py'),
                                   'prepare','--output',str(out)],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            target=out/'staging'
            subprocess.run(['git','-C',str(target),'update-ref','refs/heads/staging',STAGING],check=True)
            subprocess.run(['git','-C',str(target),'update-ref','refs/heads/main',MAIN],check=True)
            program=('import sys,json;from pathlib import Path;sys.path.insert(0,sys.argv[1]+"/scripts");'
                     'from publication_current import verify_staging_sync;'
                     'print(json.dumps(verify_staging_sync(Path(sys.argv[1]),Path(sys.argv[2]))))')
            command=[sys.executable,'-c',program,str(ROOT),str(target)]
            result=subprocess.run(command,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            self.assertEqual(json.loads(result.stdout)['target_role'],'staging')
            sentinel=Path(tmp)/'must-not-execute'
            (target/'scripts/verify-harness-adoption.py').write_text(
                'from pathlib import Path;Path('+repr(str(sentinel))+').touch()')
            result=subprocess.run(command,capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertFalse(sentinel.exists())

    def test_actual_dual_target_closeout_is_accepted(self):
        with tempfile.TemporaryDirectory(prefix='landed-closeout-') as tmp:
            out = Path(tmp)/'projection'
            result = subprocess.run([sys.executable, str(ROOT/'scripts/publication-baseline.py'),
                                     'prepare', '--output', str(out)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
            for role in ('main', 'staging'):
                target = out/role
                for name, sha in [('main', MAIN), ('staging', STAGING)]:
                    subprocess.run(['git', '-C', str(target), 'update-ref', 'refs/heads/'+name, sha], check=True)
                result = subprocess.run([sys.executable, str(target/'scripts/verify-harness-adoption.py')],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
                report = json.loads(result.stdout)
                self.assertEqual(report['target_role'], role)
                for ticket in ('T-0012', 'T-0014', 'T-0015'):
                    self.assertEqual(report['tracker']['tickets'][ticket]['status'], 'done')
                self.assertFalse(report['publishable'])


if __name__ == '__main__':
    unittest.main()
