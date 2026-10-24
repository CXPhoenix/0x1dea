#!/usr/bin/env python3
"""Current writing suites plus preselected immutable historical test contexts.

The original current runner and assertions are preserved. The original Phoenix
alignment module requires the four-package v2.3 policy byte-for-byte and runs at
its last main context. A current counterpart retains its negative assertions and
verifies unchanged voice bytes plus the explicitly reviewed fifth package.
"""
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('original_current_runner', ROOT/'scripts/run-current-python-tests.py')
original = importlib.util.module_from_spec(spec)
spec.loader.exec_module(original)
PHOENIX_BASE = '8b2cffab8ed1a8a2c50ece18b6fe5b578f186668'
PHOENIX_MODULE = 'article_publication.test_phoenix_alignment'
CONTEXTS = ((original.T13_MAIN_LANDING, (original.HISTORICAL_MODULE,)),
            (original.PR32, original.PR32_MODULES),
            (PHOENIX_BASE, (PHOENIX_MODULE,)))
FROZEN = {name for _, names in CONTEXTS for name in names}


def current_only(suite):
    result = unittest.TestSuite()
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            result.addTest(current_only(item))
        elif item.__class__.__module__ not in FROZEN:
            result.addTest(item)
    return result


def main():
    sys.dont_write_bytecode = True
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    # Bind unchanged contracts before selecting a context; never retry a failed
    # current assertion at an older source or rewrite an input to obtain success.
    for commit, modules in CONTEXTS:
        for module in modules:
            name = 'tests/' + module.replace('.', '/') + '.py'
            raw = subprocess.check_output(['git', '--no-replace-objects', '-C', str(ROOT), 'show', commit+':'+name])
            path = ROOT/name
            if path.is_symlink() or path.read_bytes() != raw:
                print('changed frozen historical test: '+name, file=sys.stderr)
                return 1
    success = True
    for name in ('harness_adoption', 'article_publication'):
        suite = unittest.TestLoader().discover(str(ROOT/'tests'/name), top_level_dir=str(ROOT/'tests'))
        result = unittest.TextTestRunner(verbosity=2).run(current_only(suite))
        print(f'{name} (writing current): testsRun={result.testsRun} failures={len(result.failures)} errors={len(result.errors)}', flush=True)
        success = result.testsRun > 0 and result.wasSuccessful() and success
    for commit, modules in CONTEXTS:
        with tempfile.TemporaryDirectory(prefix='writing-frozen-') as tmp:
            fixture = Path(tmp)/'fixture'
            for command in (['git','clone','--shared','--no-checkout',str(ROOT),str(fixture)],
                            ['git','-C',str(fixture),'checkout','--detach',commit]):
                result = subprocess.run(command,capture_output=True,text=True)
                if result.returncode:
                    print('frozen context unavailable: '+result.stderr,file=sys.stderr)
                    return 1
            if commit == PHOENIX_BASE:
                for role, pin in (('main', PHOENIX_BASE),
                                  ('staging', '6fcb277a9841dfad21d91f79005d39924acd92d2')):
                    subprocess.run(['git','-C',str(fixture),'update-ref','refs/heads/'+role,pin],check=True)
            result = subprocess.run([sys.executable,'-B','-m','unittest','-v',*modules],cwd=fixture,
                                    env=dict(os.environ,PYTHONPATH=str(fixture/'tests')))
            print('writing frozen context: commit='+commit+' modules='+','.join(modules)+' exit='+str(result.returncode),flush=True)
            success = result.returncode==0 and success
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
