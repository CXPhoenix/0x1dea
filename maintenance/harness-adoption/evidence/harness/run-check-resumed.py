#!/usr/bin/env python3
"""Capture one real check, without installations or shell interpolation."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

job = json.loads(sys.stdin.read())
out = Path(__file__).parent / "evidence" / "resumed"
out.mkdir(exist_ok=True)
name = job["name"]
if not name.replace("-", "").replace("_", "").isalnum():
    raise SystemExit("unsafe check name")
log, meta = out / (name + ".log"), out / (name + ".json")
if log.exists() or meta.exists():
    raise SystemExit("check ID already recorded; choose a new attempt ID")
env = dict(os.environ)
env.update({"PATH": "{EXISTING_NODE_BIN}:" + env.get("PATH", ""), "COREPACK_ENABLE_NETWORK": "0", "PYTHONDONTWRITEBYTECODE": "1"})
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
t = time.monotonic()
with log.open("wb") as f:
    p = subprocess.run(job["argv"], cwd=job["cwd"], env=env, stdout=f, stderr=subprocess.STDOUT)
record = {"name": name, "argv": job["argv"], "cwd": job["cwd"], "started_utc": start, "ended_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "elapsed_seconds": time.monotonic() - t, "exit_code": p.returncode, "status": "pass" if p.returncode == 0 else job.get("failure_status", "failure"), "log_sha256": hashlib.sha256(log.read_bytes()).hexdigest(), "log": str(log), "baseline": "ee7fecfff72f47abc735d26ac7e9a943de04ebbf", "node_selection": "existing NVM v24.13.0; no install", "package_manager_network": "disabled"}
meta.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(record, ensure_ascii=False))
print(log.read_text(errors="replace")[-7000:])
raise SystemExit(p.returncode)
