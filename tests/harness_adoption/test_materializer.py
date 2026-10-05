"""Real filesystem and CLI regression tests for the three-package materializer."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts/materialize-writing-skills.py"
NAMES = ("phoenix-writing", "maintaining-writing-skills", "creating-vitepress-post")
ALIASES = (
    ("skills/phoenix-writing/reference", "../../maintenance/writing-skills/legacy/phoenix-writing/reference", "maintenance/writing-skills/legacy/phoenix-writing/reference", "phoenix-writing/reference"),
    ("skills/phoenix-writing/scripts", "../maintaining-writing-skills/legacy-validator", "skills/maintaining-writing-skills/legacy-validator", "phoenix-writing/scripts"),
)

def sha(data):
    return hashlib.sha256(data).hexdigest()

class MaterializerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()  # macOS /var is a host alias; fixture uses its real directory
        self.put("scripts/vpHelper.ts", "// source helper\n")
        self.put("maintenance/writing-skills/SOURCES.md", "# Source\n")
        for name in NAMES:
            self.put(f"skills/{name}/SKILL.md", f"---\nname: {name}\ndescription: local fixture\nmetadata:\n  scope: project\n---\n\n# Test\n")
        self.put("skills/creating-vitepress-post/SKILL.md", "---\nname: creating-vitepress-post\ndescription: local fixture\n---\n[helper](../../scripts/vpHelper.ts#helper)\n[sibling](../phoenix-writing/SKILL.md)\n`[literal](../../missing.md)`\n```md\n[x](../../missing.md)\n```\n")
        self.put("skills/maintaining-writing-skills/references/context.md", "[source](../../../maintenance/writing-skills/SOURCES.md)\n")
        self.put("skills/maintaining-writing-skills/legacy-validator/validate.py", "print('historical validator')\n")
        self.put("maintenance/writing-skills/legacy/phoenix-writing/reference/old.md", "# Legacy\n")
        for path,target,backing,dest in ALIASES:
            (self.root/path).symlink_to(target)
        for runtime in (".agents", ".claude"):
            self.put(f"{runtime}/skills/framework/SKILL.md", "# Foreign framework preserved\n")
        self.pin()

    def put(self, path, content):
        p = self.root / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        return p

    def pin(self):
        inputs = []
        roots = [f"skills/{n}" for n in NAMES] + [ALIASES[0][2]]
        for root in roots:
            for p in sorted((self.root/root).rglob("*")):
                if p.is_file() and not p.is_symlink():
                    inputs.append({"path": p.relative_to(self.root).as_posix(), "sha256": sha(p.read_bytes())})
        policy = {"schema_version": 1, "skills": list(NAMES), "implicit": {NAMES[0]: True, NAMES[1]: True, NAMES[2]: True}, "inputs": inputs, "aliases": [{"path": p,"literal_target": t,"backing_root": b,"runtime_subpath": d,"literal_sha256": sha(t.encode())} for p,t,b,d in ALIASES]}
        self.put("maintenance/harness-adoption/runtime-source-policy.json", json.dumps(policy, sort_keys=True, indent=2)+"\n")

    def run_cli(self, mode="--write", *extra):
        return subprocess.run([sys.executable, str(SCRIPT), "--root", str(self.root), mode, *extra], capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE":"1"})

    def assert_ok(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def assert_rejected(self, result):
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("MATERIALIZER:", result.stderr)

    def snapshot(self):
        return {p.relative_to(self.root).as_posix():sha(p.read_bytes()) for root in (".agents", ".claude", "maintenance/harness-adoption") for p in (self.root/root).rglob("*") if p.is_file() and not p.is_symlink()}

    def test_builds_physical_complete_packages_and_projects_links(self):
        self.assert_ok(self.run_cli())
        for runtime in (".agents", ".claude"):
            self.assertFalse(any(p.is_symlink() for p in (self.root/runtime).rglob("*")))
            self.assertEqual((self.root/f"{runtime}/skills/phoenix-writing/reference/old.md").read_text(), "# Legacy\n")
            self.assertEqual((self.root/f"{runtime}/skills/phoenix-writing/scripts/validate.py").read_text(), "print('historical validator')\n")
            text=(self.root/f"{runtime}/skills/creating-vitepress-post/SKILL.md").read_text()
            self.assertIn("(../../../scripts/vpHelper.ts#helper)", text)
            self.assertIn("(../phoenix-writing/SKILL.md)",text)
            self.assertIn("`[literal](../../missing.md)`", text)
            self.assertIn("[x](../../missing.md)",text)
            self.assertIn("(../../../../maintenance/writing-skills/SOURCES.md)", (self.root/f"{runtime}/skills/maintaining-writing-skills/references/context.md").read_text())
        codex=(self.root/".agents/skills/phoenix-writing/agents/openai.yaml").read_text()
        self.assertIn("allow_implicit_invocation: true",codex)
        self.assertIn("allow_implicit_invocation: true",(self.root/".agents/skills/creating-vitepress-post/agents/openai.yaml").read_text())
        self.assertNotIn("disable-model-invocation", (self.root/".agents/skills/creating-vitepress-post/SKILL.md").read_text())
        self.assertNotIn("disable-model-invocation", (self.root/".claude/skills/creating-vitepress-post/SKILL.md").read_text())
        self.assertFalse((self.root/".claude/skills/phoenix-writing/agents").exists())
        self.assertEqual((self.root/".agents/skills/framework/SKILL.md").read_text(), "# Foreign framework preserved\n")

    def test_second_generation_and_check_are_deterministic_and_read_only(self):
        self.assert_ok(self.run_cli())
        before=self.snapshot()
        self.assert_ok(self.run_cli())
        self.assertEqual(before,self.snapshot())
        self.assert_ok(self.run_cli("--check"))
        self.assertEqual(before,self.snapshot())

    def test_check_detects_output_manifest_and_policy_drift(self):
        self.assert_ok(self.run_cli())
        for path in (".agents/skills/phoenix-writing/SKILL.md", "maintenance/harness-adoption/generated-writing-manifest.json", "maintenance/harness-adoption/runtime-source-policy.json"):
            with self.subTest(path=path):
                p=self.root/path; old=p.read_bytes(); p.write_bytes(old+b" ")
                result=self.run_cli("--check")
                self.assert_rejected(result)
                p.write_bytes(old)

    def test_rejects_unknown_missing_extra_and_changed_inputs_before_write(self):
        for action in ("extra", "missing", "hash", "unknown-link", "foreign-metadata"):
            with self.subTest(action=action):
                p=self.root/"skills/phoenix-writing/SKILL.md"; old=p.read_bytes()
                extra=self.root/"skills/phoenix-writing/unexpected.md"
                if action=="extra":extra.write_text("new")
                elif action=="missing":p.unlink()
                elif action=="hash":p.write_bytes(old+b"tamper")
                elif action=="unknown-link":extra.symlink_to("../maintaining-writing-skills")
                else:self.put("skills/phoenix-writing/agents/openai.yaml", "foreign: true\n");self.pin()
                before=self.snapshot();result=self.run_cli()
                after=self.snapshot()
                if extra.is_symlink() or extra.exists():extra.unlink()
                if action=="foreign-metadata":(self.root/"skills/phoenix-writing/agents/openai.yaml").unlink();(self.root/"skills/phoenix-writing/agents").rmdir()
                p.write_bytes(old); self.pin()
                self.assert_rejected(result)
                self.assertEqual(before,after)

    def test_rejects_alias_target_escape_and_nested_backing_symlink(self):
        alias=self.root/ALIASES[0][0]
        for target in ("/tmp", "../../../../outside", "../../maintenance/writing-skills/legacy/phoenix-writing/reference/../reference"):
            alias.unlink();alias.symlink_to(target)
            result=self.run_cli();self.assert_rejected(result)
        alias.unlink();alias.symlink_to(ALIASES[0][1])
        backing=self.root/ALIASES[0][2]/"old.md";backing.unlink();backing.symlink_to(self.root/"scripts/vpHelper.ts")
        result=self.run_cli();self.assert_rejected(result)

    def test_rejects_extra_and_missing_backing_files(self):
        extra=self.put(ALIASES[0][2]+"/extra.md", "unexpected")
        self.assert_rejected(self.run_cli())
        extra.unlink();(self.root/ALIASES[0][2]/"old.md").unlink()
        self.assert_rejected(self.run_cli())

    def test_rejects_source_parent_symlink_even_with_matching_hash(self):
        old=self.root/"skills/maintaining-writing-skills/references"; old.rename(self.root/"external")
        old.symlink_to(self.root/"external",target_is_directory=True)
        self.assert_rejected(self.run_cli())

    def test_rejects_unknown_active_markdown_link_syntax_and_missing_link(self):
        p=self.root/"skills/phoenix-writing/SKILL.md";old=p.read_text()
        for bad in ("[bad][ref]\n[ref]: ../../scripts/vpHelper.ts\n", "<a href=\"../../scripts/vpHelper.ts\">x</a>\n", "[bad](../../does-not-exist.md)\n"):
            p.write_text(old+bad);self.pin();result=self.run_cli()
            self.assert_rejected(result)

    def test_rolls_back_partial_install_and_preserves_foreign_framework(self):
        self.assert_ok(self.run_cli());before=self.snapshot()
        p=self.root/"skills/phoenix-writing/SKILL.md";p.write_bytes(p.read_bytes()+b"\nUpdate\n");self.pin()
        pinned=self.snapshot()
        result=self.run_cli("--write", "--test-fail-after", "2")
        self.assert_rejected(result)
        self.assertEqual(pinned,self.snapshot())
        self.assertEqual(before["maintenance/harness-adoption/generated-writing-manifest.json"],self.snapshot()["maintenance/harness-adoption/generated-writing-manifest.json"])

    def test_rejects_runtime_parent_and_foreign_framework_symlinks(self):
        self.assert_ok(self.run_cli())
        p=self.root/".agents/skills/framework/SKILL.md";p.unlink();p.symlink_to(self.root/"scripts/vpHelper.ts")
        self.assert_rejected(self.run_cli())
        p.unlink();p.write_text("framework")
        parent=self.root/".claude/skills";parent.rename(self.root/"elsewhere");parent.symlink_to(self.root/"elsewhere",target_is_directory=True)
        self.assert_rejected(self.run_cli())

    def test_rollback_restores_original_entry_symlinks_after_first_install_failure(self):
        for runtime in (".agents", ".claude"):
            for name in NAMES:
                (self.root/f"{runtime}/skills/{name}").symlink_to(f"../../skills/{name}")
        result=self.run_cli("--write", "--test-fail-after", "4")
        self.assert_rejected(result)
        self.assertIn("injected partial-install failure",result.stderr)
        for runtime in (".agents", ".claude"):
            for name in NAMES:
                p=self.root/f"{runtime}/skills/{name}"
                self.assertTrue(p.is_symlink())
                self.assertEqual(os.readlink(p),f"../../skills/{name}")
        self.assertFalse((self.root/"maintenance/harness-adoption/generated-writing-manifest.json").exists())

    def test_rejects_pinned_backing_hash_drift_and_regular_alias_replacement(self):
        p=self.root/ALIASES[0][2]/"old.md";p.write_text("tampered historical backing")
        result=self.run_cli();self.assert_rejected(result);self.assertIn("source SHA drift",result.stderr)
        p.write_text("# Legacy\n")
        alias=self.root/ALIASES[0][0];alias.unlink();alias.mkdir()
        result=self.run_cli();self.assert_rejected(result);self.assertIn("alias literal",result.stderr)

    def test_rejects_policy_parent_symlink_before_read(self):
        p=self.root/"maintenance/harness-adoption";p.rename(self.root/"external-policy")
        p.symlink_to(self.root/"external-policy",target_is_directory=True)
        result=self.run_cli();self.assert_rejected(result);self.assertIn("symlink component",result.stderr)

    def test_rejects_runtime_extra_and_claude_codex_metadata_on_check(self):
        self.assert_ok(self.run_cli())
        for path in (".agents/skills/phoenix-writing/foreign.md", ".claude/skills/phoenix-writing/agents/openai.yaml"):
            p=self.put(path,"foreign")
            result=self.run_cli("--check");self.assert_rejected(result);self.assertIn("generated output drift",result.stderr)
            p.unlink()

    def test_rejects_source_claude_frontmatter_before_generation(self):
        p=self.root/"skills/phoenix-writing/SKILL.md"
        p.write_text(p.read_text().replace("name:","disable-model-invocation: true\nname:",1));self.pin()
        result=self.run_cli();self.assert_rejected(result);self.assertIn("foreign runtime frontmatter",result.stderr)

    def test_rejects_unknown_or_duplicate_canonical_frontmatter_keys(self):
        p=self.root/"skills/phoenix-writing/SKILL.md";original=p.read_text()
        for added in ("tools: shell\n", "policy: unsafe\n", "name: arbitrary-other-skill\n"):
            with self.subTest(added=added):
                p.write_text(original.replace("description:",added+"description:",1));self.pin()
                result=self.run_cli();self.assert_rejected(result);self.assertIn("foreign runtime frontmatter",result.stderr)

    def test_rejects_quoted_top_level_runtime_keys_and_duplicate_names(self):
        p=self.root/"skills/phoenix-writing/SKILL.md";original=p.read_text()
        for added in ('"disable-model-invocation": true\n', '"name": arbitrary-other-skill\n'):
            with self.subTest(added=added):
                p.write_text(original.replace("description:",added+"description:",1));self.pin()
                result=self.run_cli();self.assert_rejected(result);self.assertIn("foreign runtime frontmatter",result.stderr)

    def test_rejects_manifest_directory_without_removing_its_data(self):
        sentinel=self.put("maintenance/harness-adoption/generated-writing-manifest.json/foreign.txt","preserve unrelated data")
        result=self.run_cli();self.assert_rejected(result);self.assertIn("manifest must be a regular file",result.stderr)
        self.assertTrue(sentinel.is_file());self.assertEqual(sentinel.read_text(),"preserve unrelated data")

    def test_preserves_encoded_spaces_in_projected_markdown_links(self):
        self.put("scripts/helper one.ts","// spaced helper")
        p=self.root/"skills/phoenix-writing/SKILL.md";p.write_text(p.read_text()+"[space](../../scripts/helper%20one.ts)\n");self.pin()
        self.assert_ok(self.run_cli())
        for runtime in (".agents", ".claude"):
            text=(self.root/f"{runtime}/skills/phoenix-writing/SKILL.md").read_text()
            self.assertIn("(../../../scripts/helper%20one.ts)",text)
            self.assertNotIn("(../../../scripts/helper one.ts)",text)
        self.assert_ok(self.run_cli("--check"))

    def test_rejects_wrong_top_level_name_even_when_nested_name_matches(self):
        p=self.root/"skills/phoenix-writing/SKILL.md";text=p.read_text().replace("name: phoenix-writing","name: arbitrary-other-skill",1).replace("  scope: project","  scope: project\n  name: phoenix-writing")
        p.write_text(text);self.pin()
        result=self.run_cli();self.assert_rejected(result);self.assertIn("frontmatter/name",result.stderr)

    def test_rejects_forged_policy_alias_mapping_and_duplicate_input(self):
        path=self.root/"maintenance/harness-adoption/runtime-source-policy.json"; original=path.read_text()
        for mutation in ("alias", "duplicate", "escape"):
            data=json.loads(original)
            if mutation=="alias":data["aliases"][0]["runtime_subpath"]="phoenix-writing/other"
            elif mutation=="duplicate":data["inputs"].append(data["inputs"][0])
            else:data["inputs"][0]["path"]="../outside"
            path.write_text(json.dumps(data))
            self.assert_rejected(self.run_cli())
        path.write_text(original)

if __name__ == "__main__":
    unittest.main()
