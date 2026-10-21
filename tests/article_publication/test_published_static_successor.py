"""D01-D04 at native CLI / real Git seams; fixed contracts stay unchanged."""
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
RECORD = 'blog/public/.well-known/discord'
BODY = b'dh=4acc59d1f525794606c4c966b3b879591973fd02'
PUBLICATION = '0e690064985d9d734849e1ec44a8c0f8d84fb2a3'


class PublishedStaticSuccessorTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='discord-source-contract-')
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.output = self.directory / 'projection'
        result = subprocess.run(
            [sys.executable, str(SOURCE / 'scripts/publication-baseline.py'),
             'prepare', '--output', str(self.output)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def git(self, root, *args):
        return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()

    def published(self, role='main'):
        root = self.output / role
        pin = self.git(SOURCE, 'rev-parse', 'refs/heads/' + role)
        self.git(root, 'update-ref', 'HEAD', pin)
        path = root / RECORD
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(BODY)
        path.chmod(0o644)
        return root

    def verify(self, root, *, control=None, env=None):
        return subprocess.run(
            [sys.executable, str((control or root) / 'scripts/verify-harness-adoption.py'),
             '--root', str(root)], capture_output=True, text=True, env=env)

    def assert_refused(self, result, reason=None):
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertEqual(result.stdout, '')
        if reason:
            self.assertIn(reason, result.stderr)

    def test_exact_published_record_passes_on_both_current_targets(self):
        for role in ('main', 'staging'):
            with self.subTest(role=role):
                result = self.verify(self.published(role))
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                report = json.loads(result.stdout)
                self.assertEqual(report['target_role'], role)
                self.assertFalse(report['publishable'])

    def test_every_executable_bit_on_published_record_is_refused(self):
        root = self.published()
        path = root / RECORD
        for mode in (0o744, 0o654, 0o645):
            with self.subTest(mode=oct(mode)):
                path.chmod(mode)
                self.assert_refused(self.verify(root))
        path.chmod(0o644)

    def test_missing_changed_and_linked_record_is_refused(self):
        root = self.published()
        path = root / RECORD
        for raw in (b'unapproved record', BODY + b'\n'):
            with self.subTest(body=raw):
                path.write_bytes(raw)
                self.assert_refused(self.verify(root), RECORD)
        path.unlink()
        self.assert_refused(self.verify(root), RECORD)
        outside = self.directory / 'exact-record'
        outside.write_bytes(BODY)
        path.symlink_to(outside)
        self.assert_refused(self.verify(root), RECORD)
        path.unlink()
        path.write_bytes(BODY)
        moved = self.directory / 'record-parent'
        path.parent.rename(moved)
        path.parent.symlink_to(moved, target_is_directory=True)
        self.assert_refused(self.verify(root), '.well-known')
        path.parent.unlink()
        moved.rename(path.parent)

    def test_unknown_well_known_public_and_management_sources_are_refused(self):
        root = self.published()
        for name in ('blog/public/.well-known/other', 'blog/public/extra.txt',
                     '.proj.specs/0013-discord-source-alignment/unapproved.json'):
            with self.subTest(path=name):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'unapproved')
                self.assert_refused(self.verify(root), name)
                path.unlink()

    def test_candidate_policy_cannot_approve_changed_or_additional_public_records(self):
        control = self.published()
        root = self.directory / 'candidate'
        shutil.copytree(control, root, symlinks=True)
        policy_path = root / 'maintenance/publication-workflow/engineering-v1.json'
        original = policy_path.read_bytes()
        for name in (RECORD, 'blog/public/.well-known/other'):
            with self.subTest(path=name):
                path = root / name
                path.write_bytes(b'self-approved record')
                policy = json.loads(original)
                policy['common'][name] = {
                    'mode': '100644', 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
                policy_path.write_text(json.dumps(policy))
                self.assert_refused(self.verify(root, control=control))
                # Even a candidate executing its own edited map cannot put public
                # content in the engineering overlay or override the finite record.
                self.assert_refused(self.verify(root))
                policy_path.write_bytes(original)
                if name == RECORD:
                    path.write_bytes(BODY)
                else:
                    path.unlink()

    def test_historical_projections_keep_inventory_and_refuse_record_or_cross_role(self):
        bases = {'main': 'eeda8e48d1cb203e4cec2bd53e26d3dcf5c7d45a',
                 'staging': 'c6efa7ded4731cbe251bdbc6fea5615e7e7b11b7'}
        for role, base in bases.items():
            with self.subTest(role=role):
                root = self.output / role
                self.assertEqual(self.git(root, 'rev-parse', 'HEAD'), base)
                self.assertFalse((root / RECORD).exists())
                result = self.verify(root)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(json.loads(result.stdout)['target_role'], role)
        self.assert_refused(self.verify(self.output / 'staging', control=self.output / 'main'))
        root = self.output / 'main'
        path = root / RECORD
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(BODY)
        self.assert_refused(self.verify(root), RECORD)

    def test_unavailable_publication_commit_is_not_treated_as_old_history(self):
        control = self.output / 'main'
        root = self.directory / 'old-candidate'
        shutil.copytree(control, root, symlinks=True)
        history = self.directory / 'old-history'
        subprocess.run(['git', 'init', '--quiet', str(history)], check=True)
        subprocess.run(['git', '-c', 'protocol.file.allow=always', '-C', str(history),
                        'fetch', '--quiet', '--no-tags', str(SOURCE),
                        'eeda8e48d1cb203e4cec2bd53e26d3dcf5c7d45a'], check=True)
        self.git(history, 'update-ref', 'HEAD',
                 'eeda8e48d1cb203e4cec2bd53e26d3dcf5c7d45a')
        missing = subprocess.run(['git', '-C', str(history), 'cat-file', '-e',
                                  PUBLICATION + '^{commit}'], capture_output=True)
        self.assertNotEqual(missing.returncode, 0, 'fixture unexpectedly has future history')
        (root / '.git').rename(self.directory / 'complete-metadata')
        shutil.copytree(history / '.git', root / '.git')
        self.assert_refused(self.verify(root, control=control),
                            'published Discord source ancestry is unavailable')

    def test_ancestry_query_error_is_not_treated_as_normal_non_ancestor(self):
        root = self.published()
        real_git = shutil.which('git')
        self.assertIsNotNone(real_git)
        binaries = self.directory / 'bin'
        binaries.mkdir()
        marker = self.directory / 'ancestry-query-observed'
        wrapper = binaries / 'git'
        wrapper.write_text(
            '#!' + sys.executable + '\n'
            'import os, sys\nfrom pathlib import Path\n'
            'if sys.argv[-4:] == ' + repr(['merge-base', '--is-ancestor', PUBLICATION, 'HEAD']) + ':\n'
            '    Path(' + repr(str(marker)) + ').write_text("observed")\n'
            '    raise SystemExit(42)\n'
            'os.execv(' + repr(real_git) + ', [' + repr(real_git) + ', *sys.argv[1:]])\n')
        wrapper.chmod(0o755)
        env = dict(os.environ, PATH=str(binaries) + os.pathsep + os.environ['PATH'])
        self.assert_refused(self.verify(root, env=env),
                            'published Discord source ancestry is unavailable')
        self.assertTrue(marker.is_file(), 'native Git boundary was not reached')


if __name__ == '__main__':
    unittest.main()
