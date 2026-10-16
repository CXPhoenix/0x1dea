#!/usr/bin/env python3
"""Prepare source-bound external inputs using installed tools; never installs or activates."""
import argparse
import json
from pathlib import Path
import sys
import subprocess

from publication_jobs import materialize_job, verify_job


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation',choices=('prepare','verify'))
    parser.add_argument('--manifest',type=Path)
    parser.add_argument('--manifest-sha256')
    parser.add_argument('--snapshot-root',type=Path)
    parser.add_argument('--binding-sha256')
    parser.add_argument('--repository',required=True)
    parser.add_argument('--role',choices=('writer','validator'),required=True)
    args = parser.parse_args()
    try:
        if args.operation == 'prepare':
            if args.manifest is None or args.manifest_sha256 is None:
                raise ValueError('independent job manifest and digest required')
            result = materialize_job(args.manifest,args.manifest_sha256,
                                     repository=args.repository,role=args.role)
        else:
            if args.snapshot_root is None or args.binding_sha256 is None:
                raise ValueError('independent snapshot root and binding digest required')
            result = verify_job(args.snapshot_root,args.binding_sha256,
                                repository=args.repository,role=args.role)
        print(json.dumps(result,indent=2))
        return 0
    except (ValueError,OSError,KeyError,TypeError,RuntimeError,subprocess.SubprocessError) as error:
        print(json.dumps({'status':'blocked','reason':str(error),'publishable':False}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
