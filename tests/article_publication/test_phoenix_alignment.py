"""P02/P03/P22 exact writing successor at existing public CLI seams."""
import json
import hashlib
from contextlib import contextmanager
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[2]
PIN = 'bf6f872db9aa4a2d3e4a765ef4f171186349f432'
FILES = (
    'skills/phoenix-writing/SKILL.md',
    'skills/phoenix-writing/references/context-form.md',
    '.agents/skills/phoenix-writing/SKILL.md',
    '.agents/skills/phoenix-writing/references/context-form.md',
    '.claude/skills/phoenix-writing/SKILL.md',
    '.claude/skills/phoenix-writing/references/context-form.md',
    'maintenance/harness-adoption/runtime-source-policy.json',
    'maintenance/harness-adoption/generated-writing-manifest.json',
    'maintenance/writing-skills/SOURCES.md',
    'maintenance/writing-skills/VALIDATION.md',
)


class PhoenixAlignmentTests(unittest.TestCase):
    def projection(self):
        temp = tempfile.TemporaryDirectory(prefix='phoenix-negative-')
        self.addCleanup(temp.cleanup)
        output = Path(temp.name).resolve()/'projection'
        result = subprocess.run([sys.executable, '-B', str(SOURCE/'scripts/publication-baseline.py'),
                                 'prepare', '--output', str(output)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return output/'main'

    def verify(self, root):
        return subprocess.run([sys.executable, '-B', str(root/'scripts/verify-harness-adoption.py')],
                              cwd=root, capture_output=True, text=True)

    @contextmanager
    def changed(self, root, name):
        path = root/name
        raw, mode = path.read_bytes(), path.stat().st_mode
        policy = root/'maintenance/publication-workflow/engineering-v1.json'
        policy_raw = policy.read_bytes()
        try:
            yield path, policy
        finally:
            if path.is_symlink():
                path.unlink()
            path.write_bytes(raw)
            path.chmod(mode)
            policy.write_bytes(policy_raw)

    def refused(self, root, name):
        result = self.verify(root)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(name, result.stdout + result.stderr)

    def test_exact_v23_is_accepted_in_both_engineering_projections(self):
        with tempfile.TemporaryDirectory(prefix='phoenix-alignment-') as tmp:
            output = Path(tmp).resolve() / 'projection'
            result = subprocess.run([sys.executable, '-B', str(SOURCE/'scripts/publication-baseline.py'),
                                     'prepare', '--output', str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for role in ('main', 'staging'):
                root = output/role
                with self.subTest(role=role):
                    for name in FILES:
                        expected = subprocess.check_output(['git', '-C', str(SOURCE), 'show', PIN+':'+name])
                        self.assertEqual((root/name).read_bytes(), expected, name)
                        self.assertEqual((root/name).stat().st_mode & 0o777, 0o644, name)
                    checked = subprocess.run([sys.executable, '-B', str(root/'scripts/verify-harness-adoption.py')],
                                             cwd=root, capture_output=True, text=True)
                    self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
                    self.assertEqual(json.loads(checked.stdout)['target_role'], role)
                    built = subprocess.run([sys.executable, '-B', str(root/'scripts/materialize-writing-skills.py'), '--check'],
                                           cwd=root, capture_output=True, text=True)
                    self.assertEqual(built.returncode, 0, built.stdout + built.stderr)


    def test_each_exact_identity_rejects_changed_bytes_even_with_repinning(self):
        root = self.projection()
        for name in FILES:
            with self.subTest(name=name), self.changed(root, name) as (path, policy):
                path.write_bytes(path.read_bytes()+b' ')
                data = json.loads(policy.read_bytes())
                data['common'][name]['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
                policy.write_text(json.dumps(data))
                self.refused(root, name)
        self.assertEqual(self.verify(root).returncode, 0)

    def test_missing_entries_files_links_and_all_executable_bits_are_refused(self):
        root = self.projection()
        name = 'skills/phoenix-writing/SKILL.md'
        for change in ('entry', 'file', 'link', 0o100, 0o010, 0o001):
            with self.subTest(change=change), self.changed(root, name) as (path, policy):
                if change == 'entry':
                    data = json.loads(policy.read_bytes())
                    del data['common'][name]
                    policy.write_text(json.dumps(data))
                elif change in ('file', 'link'):
                    path.unlink()
                    if change == 'link':
                        path.symlink_to(root/'skills/phoenix-writing/references/style-examples.md')
                else:
                    path.chmod(path.stat().st_mode | change)
                self.refused(root, name)
        self.assertEqual(self.verify(root).returncode, 0)

    def test_unlisted_writing_changes_remain_protected(self):
        root = self.projection()
        name = 'skills/phoenix-writing/references/style-examples.md'
        with self.changed(root, name) as (path, policy):
            path.write_bytes(path.read_bytes()+b' ')
            data = json.loads(policy.read_bytes())
            data['common'][name] = {'mode': '100644', 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
            policy.write_text(json.dumps(data))
            self.refused(root, name)
        self.assertEqual(self.verify(root).returncode, 0)


if __name__ == '__main__':
    unittest.main()
