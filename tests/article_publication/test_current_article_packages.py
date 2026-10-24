"""Current fifth-package contract; original Phoenix tests remain immutable."""
import json
import subprocess
import sys
from article_publication import test_phoenix_alignment as original

class CurrentArticlePackagesTests(original.PhoenixAlignmentTests):
    def test_exact_v23_is_accepted_in_both_engineering_projections(self):
        main = self.projection()
        mutable = {'maintenance/harness-adoption/runtime-source-policy.json',
                   'maintenance/harness-adoption/generated-writing-manifest.json'}
        expected_skills = ['phoenix-writing', 'maintaining-writing-skills',
                           'creating-vitepress-post', 'managing-article-publication',
                           'article-discovery']
        for role in ('main', 'staging'):
            root = main.parent / role
            with self.subTest(role=role):
                for name in original.FILES:
                    if name not in mutable:
                        expected = subprocess.check_output(['git', '-C', str(original.SOURCE), 'show', original.PIN + ':' + name])
                        self.assertEqual((root/name).read_bytes(), expected, name)
                    self.assertEqual((root/name).stat().st_mode & 0o777, 0o644, name)
                for name in mutable:
                    self.assertEqual(json.loads((root/name).read_text())['skills'], expected_skills)
                checked = self.verify(root)
                self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
                self.assertEqual(json.loads(checked.stdout)['target_role'], role)
                built = subprocess.run([sys.executable, '-B', str(root/'scripts/materialize-writing-skills.py'), '--check'], cwd=root, capture_output=True, text=True)
                self.assertEqual(built.returncode, 0, built.stdout + built.stderr)
