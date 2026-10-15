#!/usr/bin/env python3
"""Run live Python suites plus the explicit immutable #22 T13 fixture contract."""
import argparse
from pathlib import Path
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
T13_MAIN_LANDING = '001b26f8e931e0cf1e62373c5aa088a1b5ed09eb'
HISTORICAL_MODULE = 'article_publication.test_current_baseline'


def live_only(suite):
    """Exclude exactly one versioned historical module, never current/new modules."""
    result = unittest.TestSuite()
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            result.addTest(live_only(item))
        elif item.__class__.__module__ != HISTORICAL_MODULE:
            result.addTest(item)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tests-root', type=Path, default=ROOT / 'tests')
    args = parser.parse_args()
    sys.dont_write_bytecode = True
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    historical = args.tests_root.resolve() / 'article_publication/test_current_baseline.py'
    frozen = subprocess.run(['git', '--no-replace-objects', '-C', str(ROOT), 'show',
                             T13_MAIN_LANDING + ':tests/article_publication/test_current_baseline.py'],
                            capture_output=True)
    if frozen.returncode or historical.is_symlink() or not historical.is_file() or historical.read_bytes() != frozen.stdout:
        print('changed historical T13 test contract; #22 fixture cannot hide current test edits', file=sys.stderr)
        return 1
    success = True
    for name in ('harness_adoption', 'article_publication'):
        loader = unittest.TestLoader()
        try:
            suite = loader.discover(str(args.tests_root.resolve()/name), top_level_dir=str(args.tests_root.resolve()))
            if name == 'article_publication':
                suite = live_only(suite)
        except (ImportError, OSError) as error:
            print(f'{name}: testsRun=0 failures=0 errors=1 discovery_error={error}', flush=True)
            success = False
            continue
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        print(f'{name} (live): testsRun={result.testsRun} failures={len(result.failures)} errors={len(result.errors)}', flush=True)
        success = result.testsRun > 0 and result.wasSuccessful() and success
    # Explicitly choose the historical context before execution. There is no
    # failure-dependent retry/fallback and no copying live tests into this fixture.
    with tempfile.TemporaryDirectory(prefix='t13-pr22-contract-') as tmp:
        fixture = Path(tmp)/'fixture'
        for command in (['git', 'clone', '--shared', '--no-checkout', str(ROOT), str(fixture)],
                        ['git', '-C', str(fixture), 'checkout', '--detach', T13_MAIN_LANDING]):
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode:
                print('T13 #22 frozen fixture unavailable: ' + result.stderr, file=sys.stderr)
                return 1
        result = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s',
                                 str(fixture/'tests/article_publication'), '-p', 'test_current_baseline.py', '-v'],
                                cwd=fixture)
        print('T13 #22 frozen fixture: commit=' + T13_MAIN_LANDING + ' exit=' + str(result.returncode), flush=True)
        success = result.returncode == 0 and success
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
