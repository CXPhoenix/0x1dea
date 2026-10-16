#!/usr/bin/env python3
"""Route immutable historical contracts and the reviewed current M0 successor."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import types

sys.dont_write_bytecode = True
CONTROL = Path(__file__).resolve().parents[1]
BASES = {'main': 'eeda8e48d1cb203e4cec2bd53e26d3dcf5c7d45a',
         'staging': 'c6efa7ded4731cbe251bdbc6fea5615e7e7b11b7'}
LEGACY_DIGESTS = {'main': 'cf0019f96aa56a60ae4fff325f1487a239df5df4eeb4fb1f905cdc6063de5c46',
                  'staging': '86b6f7ea72a3b0bc17d303db471a94c104860a810c73014ef16e152872cad3d2'}


def legacy_module(role):
    """Only hash-pinned historical Git code is loaded; candidate files are never imported."""
    try:
        raw = subprocess.check_output(['git', '--no-replace-objects', '-C', str(CONTROL),
                                       'show', BASES[role] + ':scripts/verify-harness-adoption.py'],
                                      stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as error:
        raise ValueError('historical verifier ancestor is unavailable') from error
    if hashlib.sha256(raw).hexdigest() != LEGACY_DIGESTS[role]:
        raise ValueError('changed immutable historical verifier')
    module = types.ModuleType('historical_' + role)
    module.__file__ = __file__
    exec(compile(raw, __file__, 'exec'), module.__dict__)
    return module


# Keep the original public test/tracker helpers and assertions available without edits.
_CONTROL_STAGE = subprocess.run(['git', '--no-replace-objects', '-C', str(CONTROL), 'merge-base',
                                 '--is-ancestor', BASES['staging'], 'HEAD'], capture_output=True)
_HISTORICAL_API = legacy_module('staging' if _CONTROL_STAGE.returncode == 0 else 'main')
for _name, _value in vars(_HISTORICAL_API).items():
    if not _name.startswith('_') and _name != 'main':
        globals()[_name] = _value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=CONTROL)
    from publication_workflows import add_arguments, from_args
    add_arguments(parser)
    args = parser.parse_args()
    root = args.root.resolve()
    current = root / 'maintenance/publication-workflow/engineering-v1.json'
    ancestry = subprocess.run(['git', '--no-replace-objects', '-C', str(root), 'merge-base',
                               '--is-ancestor', BASES['main'], 'HEAD'], capture_output=True)
    if current.exists() or current.is_symlink() or ancestry.returncode == 0:
        from publication_current import verify
        print(json.dumps(verify(CONTROL, root, workflow_admission=from_args(args, CONTROL, root)), indent=2))
        return
    # Historical fixture routing is retained; failure never selects another contract.
    records = root / 'maintenance/harness-reconciliation'
    role = 'staging' if any(records.glob('*.json')) else 'main'
    legacy_module(role).main()


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        raise SystemExit(f'FAIL: {error}')
