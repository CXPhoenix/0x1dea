"""Original #32 assertions against current code; fixed-history originals run separately."""
import importlib.util
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

SOURCE = Path(__file__).resolve().parents[2]


def materialize_published_record(root, parent='HEAD'):
    """Prepare fixture data for the actual history it claims, before assertions."""
    result = subprocess.run(
        ['git', '-C', str(root), 'merge-base', '--is-ancestor',
         '0e690064985d9d734849e1ec44a8c0f8d84fb2a3', parent], capture_output=True)
    if result.returncode == 1:
        return
    result.check_returncode()
    path = root / 'blog/public/.well-known/discord'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b'dh=4acc59d1f525794606c4c966b3b879591973fd02')
    path.chmod(0o644)


def actual_refs():
    return {role: subprocess.check_output(
        ['git', '--no-replace-objects', '-C', str(SOURCE), 'rev-parse',
         'refs/heads/' + role], text=True).strip() for role in ('main', 'staging')}


def fixture(name):
    # A separate namespace configures test fixtures only. Product modules and
    # original test source/assertions are never patched or replaced.
    spec = importlib.util.spec_from_file_location(
        'current_fixture_' + name, SOURCE/'tests/article_publication'/(name+'.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    refs = actual_refs()
    module.MAIN, module.STAGING = refs['main'], refs['staging']
    if name == 'test_remote_validation':
        def prepare_current_remote(command, *args, **kwargs):
            result = subprocess.run(command, *args, **kwargs)
            prepare = [sys.executable, str(SOURCE / 'scripts/publication-baseline.py'),
                       'prepare', '--output']
            if result.returncode == 0 and command[:4] == prepare:
                # This fixture next commits each prepared tree on its current
                # named parent. Supply data before its unchanged git add/tree.
                for role, parent in refs.items():
                    materialize_published_record(Path(command[4]) / role, parent)
            return result

        # Only this live fixture namespace changes. The real process executes and
        # its result is returned unchanged; stdlib and frozen modules stay intact.
        module.subprocess = SimpleNamespace(**(vars(subprocess) | {'run': prepare_current_remote}))
    return module


def rebind_projections(output):
    for role in ('main', 'staging'):
        for name, pin in actual_refs().items():
            subprocess.run(['git', '-C', str(output/role), 'update-ref',
                            'refs/heads/'+name, pin], check=True)
        materialize_published_record(output / role)


_closed = fixture('test_closed_baseline')
_successor = fixture('test_closeout_successor')
_landed = fixture('test_landed_closeout')
_remote = fixture('test_remote_validation')


class CurrentClosedBaselineTests(_closed.ClosedBaselineTests):
    def setUp(self):
        super().setUp()
        rebind_projections(self.output)


class CurrentCloseoutSuccessorTests(_successor.CloseoutSuccessorTests):
    def setUp(self):
        super().setUp()
        rebind_projections(self.output)


class CurrentLandedCloseoutTests(_landed.LandedCloseoutTests):
    pass


class CurrentTrustedRemoteValidationTests(_remote.TrustedRemoteValidationTests):
    pass
