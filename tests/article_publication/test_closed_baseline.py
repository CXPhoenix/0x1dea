"""P23 current closed tracker is checked independently of the frozen #22 fixtures."""
import json
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[2]
MAIN = '001b26f8e931e0cf1e62373c5aa088a1b5ed09eb'
STAGING = '035783590895a426ee395045829ebc9d50e2b9cf'


class ClosedBaselineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='closed-baseline-')
        self.addCleanup(self.tmp.cleanup)
        self.output = Path(self.tmp.name) / 'projection'
        result = subprocess.run([sys.executable, str(SOURCE/'scripts/publication-baseline.py'),
                                 'prepare', '--output', str(self.output)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for role in ('main', 'staging'):
            controller = self.output / role
            for name, pin in (('main', MAIN), ('staging', STAGING)):
                subprocess.run(['git', '-C', str(controller), 'update-ref', 'refs/heads/' + name, pin], check=True)
            subprocess.run(['git', '-C', str(controller), 'update-ref', 'HEAD', MAIN if role == 'main' else STAGING], check=True)

    def test_real_closed_t13_landing_does_not_require_future_ticket_scripts(self):
        for role in ('main', 'staging'):
            controller = self.output / role
            result = subprocess.run([sys.executable, str(controller/'scripts/verify-harness-adoption.py')],
                                     capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report['tracker']['tickets']['T-0013']['status'], 'done')
            self.assertEqual(report['target_role'], role)
            self.assertFalse(report['publishable'])
    def test_current_guard_still_rejects_m0_as_implementation_landing(self):
        controller = self.output / 'main'
        receipt_path = controller / '.proj.specs/0012-publication-workflow/implementation/T-0013-landing/landing.json'
        receipt = json.loads(receipt_path.read_bytes())
        receipt['main_commit'] = 'eeda8e48d1cb203e4cec2bd53e26d3dcf5c7d45a'
        receipt['commit'] = 'c6efa7ded4731cbe251bdbc6fea5615e7e7b11b7'
        receipt_path.write_text(json.dumps(receipt))
        policy_path = controller / 'maintenance/publication-workflow/engineering-v1.json'
        policy = json.loads(policy_path.read_bytes())
        policy['common'][receipt_path.relative_to(controller).as_posix()]['sha256'] = hashlib.sha256(receipt_path.read_bytes()).hexdigest()
        policy_path.write_text(json.dumps(policy))
        result = subprocess.run([sys.executable, str(controller/'scripts/verify-harness-adoption.py')],
                                 capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('T-0013 landing', result.stderr)
        self.assertEqual(result.stdout, '')

    def test_current_guard_rejects_partial_promisor_candidate_without_fetch(self):
        controller = self.output / 'main'
        subprocess.run(['git', '-C', str(controller), 'config', 'remote.fixture.promisor', 'true'], check=True)
        result = subprocess.run([sys.executable, str(controller/'scripts/verify-harness-adoption.py')],
                                 capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn('partial/promisor', result.stderr)
        self.assertEqual(result.stdout, '')



if __name__ == '__main__':
    unittest.main()
