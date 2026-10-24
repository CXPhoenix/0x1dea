"""Public materializer contract for approved article-discovery packaging."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]

class ArticleDiscoveryPackageTests(unittest.TestCase):
    def test_B10_fifth_package_is_materialized_for_both_runtimes(self):
        result = subprocess.run([sys.executable, '-B', 'scripts/materialize-writing-skills.py', '--check'], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        manifest = json.loads((ROOT / 'maintenance/harness-adoption/generated-writing-manifest.json').read_text())
        self.assertIn('article-discovery', manifest['skills'])
        for runtime in ('.agents', '.claude'):
            entry = ROOT / runtime / 'skills/article-discovery/SKILL.md'
            self.assertTrue(entry.is_file() and not entry.is_symlink())

if __name__ == '__main__':
    unittest.main()

# Reuse the original public CLI assertions unchanged, with a fifth-package fixture.
from harness_adoption import test_materializer as original_materializer
import hashlib

class FifthPackageFixtureTests(original_materializer.MaterializerTests):
    def setUp(self):
        super().setUp()
        self.put('skills/article-discovery/SKILL.md', '---\nname: article-discovery\ndescription: Explore article direction.\n---\n[voice](../phoenix-writing/SKILL.md)\n')
        self.pin()

    def pin(self):
        super().pin()
        path = self.root / 'skills/article-discovery/SKILL.md'
        if path.exists():
            policy_path = self.root / 'maintenance/harness-adoption/runtime-source-policy.json'
            data = json.loads(policy_path.read_text())
            data['skills'].append('article-discovery')
            data['implicit']['article-discovery'] = True
            data['inputs'].append({'path':'skills/article-discovery/SKILL.md', 'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
            policy_path.write_text(json.dumps(data, sort_keys=True, indent=2)+'\n')

    def test_B10_fifth_package_drift_and_repeat_generation(self):
        self.assert_ok(self.run_cli())
        before = self.snapshot()
        self.assert_ok(self.run_cli())
        self.assertEqual(before, self.snapshot())
        for runtime in ('.agents', '.claude'):
            path = self.root / runtime / 'skills/article-discovery/SKILL.md'
            raw = path.read_bytes()
            path.write_bytes(raw + b'changed')
            self.assert_rejected(self.run_cli('--check'))
            path.write_bytes(raw)
        self.assert_ok(self.run_cli('--check'))
