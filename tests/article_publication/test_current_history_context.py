"""Original #32 assertions against current code; fixed-history originals run separately."""
import importlib.util
from pathlib import Path
import subprocess

SOURCE = Path(__file__).resolve().parents[2]


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
    return module


def rebind_projections(output):
    for role in ('main', 'staging'):
        for name, pin in actual_refs().items():
            subprocess.run(['git', '-C', str(output/role), 'update-ref',
                            'refs/heads/'+name, pin], check=True)


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
