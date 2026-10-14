#!/usr/bin/env python3
"""Run both product Python suites; empty discovery is a failure."""
import argparse
import os
from pathlib import Path
import sys
import unittest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tests-root', type=Path, default=Path(__file__).resolve().parents[1] / 'tests')
    args = parser.parse_args()
    sys.dont_write_bytecode = True
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    root = args.tests_root.resolve()
    success = True
    for name in ('harness_adoption', 'article_publication'):
        loader = unittest.TestLoader()
        try:
            suite = loader.discover(str(root / name), top_level_dir=str(root))
        except (ImportError, OSError) as error:
            print(f'{name}: testsRun=0 failures=0 errors=1 discovery_error={error}', flush=True)
            success = False
            continue
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        print(f'{name}: testsRun={result.testsRun} failures={len(result.failures)} errors={len(result.errors)}', flush=True)
        success = result.testsRun > 0 and result.wasSuccessful() and success
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
