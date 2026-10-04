import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path.cwd()
names = {"phoenix-writing", "maintaining-writing-skills", "creating-vitepress-post"}
def snapshot(base):
    rows = {}
    for directory, dirs, files in os.walk(base, followlinks=False):
        for child in dirs + files:
            p = Path(directory) / child
            assert not p.is_symlink(), str(p)
        for filename in files:
            p = Path(directory) / filename
            rows[p.relative_to(base).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return rows

before = {runtime: snapshot(root / runtime / "skills") for runtime in (".agents", ".claude")}
manifest_path = root / "maintenance/harness-adoption/generated-writing-manifest.json"
manifest_before = manifest_path.read_bytes()
subprocess.run([sys.executable, "scripts/materialize-writing-skills.py", "--write"], check=True)
after = {runtime: snapshot(root / runtime / "skills") for runtime in (".agents", ".claude")}
assert before == after, "generation was not deterministic"
assert manifest_before == manifest_path.read_bytes(), "manifest bytes changed"
for runtime in (".agents", ".claude"):
    packages = {p.split("/", 1)[0] for p in after[runtime]}
    assert len(packages) == 35 and names <= packages, packages
    initialized = snapshot(root.parent / "scratch-resumed" / runtime / "skills")
    framework = {p: h for p, h in after[runtime].items() if p.split("/", 1)[0] not in names}
    assert framework == initialized, "pinned initialized framework bytes changed"
subprocess.run([sys.executable, "scripts/materialize-writing-skills.py", "--check"], check=True)
print(json.dumps({"status":"pass", "runtime_packages":{".agents":35,".claude":35},
    "all_depth_no_symlinks": True, "two_project_generations_identical": True,
    "framework_bytes_equal_pinned_initialized_template":True,
    "generated_manifest_sha256":hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
    "runtime_tree_sha256":{r:hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest() for r,rows in after.items()},
    "source_policy_sha256":hashlib.sha256((root/"maintenance/harness-adoption/runtime-source-policy.json").read_bytes()).hexdigest()},sort_keys=True))
