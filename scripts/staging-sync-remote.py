#!/usr/bin/env python3
"""Trusted synchronization adapter. Inert until separately verified remote activation."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True
CONTROL = Path(__file__).resolve().parents[1]


def checked_json(path, expected, *, external=False):
    if path is None or expected is None or len(expected) != 64:
        raise ValueError('explicit trusted input and digest required')
    path = path.resolve(strict=True)
    if external and path.is_relative_to(CONTROL):
        raise ValueError('activation authority must be external to candidate/control source')
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError('trusted input digest mismatch')
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('duplicate input key')
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('schema', 'run', 'validate'))
    parser.add_argument('--repository')
    parser.add_argument('--policy-sha256')
    parser.add_argument('--registry', type=Path)
    parser.add_argument('--registry-sha256')
    parser.add_argument('--activation', type=Path)
    parser.add_argument('--activation-sha256')
    parser.add_argument('--state-dir', type=Path)
    parser.add_argument('--allow-remote-write', action='store_true')
    parser.add_argument('--operation-record', type=Path)
    parser.add_argument('--head')
    parser.add_argument('--dispatch-inputs-env')
    parser.add_argument('--runtime', type=Path)
    parser.add_argument('--runtime-sha256')
    parser.add_argument('--build-output', type=Path)
    parser.add_argument('--job-snapshot-root', type=Path)
    parser.add_argument('--job-binding-sha256')
    args = parser.parse_args()
    # Consume the explicit writer credential before any trusted Git preparation.
    # Only the JSON transport receives the retained value; no subprocess inherits it.
    writer_token = os.environ.pop('PUBLICATION_WRITER_TOKEN', None) if args.operation == 'run' else None
    if args.operation == 'schema':
        print(json.dumps({'version':1, 'operations':['schema', 'run', 'validate'],
            'branch':'tickets/T-0016/main-to-staging-sync', 'max_retries':3,
            'activation_required':['repository','permissions_verified','latest_base_verified','dispatch_verified',
                'candidate_isolation_verified','exercise_run_id','workflow','workflow_sha256','branch_seed','bootstrap_pr'],
            'operation_binding':['repository','target','branch','owner','main','staging','policy','tree','id'],
            'authority':'External owner-reviewed receipt digest and explicit run flag; no implicit credentials',
            'publishable':False}))
        return 0
    try:
        if args.operation == 'run' and not args.allow_remote_write:
            raise ValueError('remote authority and activation prerequisites missing')
        job = None
        if args.job_snapshot_root is not None or args.job_binding_sha256 is not None:
            if args.job_snapshot_root is None or args.job_binding_sha256 is None:
                raise ValueError('sealed job root and independent binding digest required')
            from publication_jobs import verify_job
            job = verify_job(args.job_snapshot_root, args.job_binding_sha256,
                repository=args.repository, role='writer' if args.operation == 'run' else 'validator',
                include_inputs=True)
            if args.operation == 'run' and (args.state_dir is None
                    or str(args.state_dir) != job['state_directory']):
                raise ValueError('writer durable state must match verified job binding')
        from publication_remote_git import LocalPreparation, validate_operation, operation_for
        import publication_current as current
        policy = hashlib.sha256(current.regular(CONTROL, current.POLICY).read_bytes()).hexdigest()
        dispatch_record = None
        if args.operation == 'validate' and args.dispatch_inputs_env:
            inputs = json.loads(os.environ[args.dispatch_inputs_env])
            if set(inputs) != {'operation', 'main', 'staging', 'head', 'tree', 'policy'}:
                raise ValueError('dispatch input schema mismatch')
            dispatch_record = operation_for(args.repository, inputs['policy'], inputs, inputs['tree'])
            if dispatch_record['id'] != inputs['operation']:
                raise ValueError('dispatch operation digest mismatch')
            args.policy_sha256, args.head = inputs['policy'], inputs['head']
        if policy != args.policy_sha256:
            raise ValueError('trusted main policy digest required')
        registry = job['checked_inputs']['registry'] if job else checked_json(args.registry, args.registry_sha256)
        if args.operation == 'validate':
            if (dispatch_record is None and args.operation_record is None) or args.head is None or args.build_output is None:
                raise ValueError('exact operation, head and new build output required')
            record = dispatch_record if dispatch_record is not None else json.loads(args.operation_record.read_bytes())
            runtime = job['checked_inputs']['runtime'] if job else checked_json(args.runtime, args.runtime_sha256)
            if job:
                args.runtime_sha256 = job['runtime_sha256']
            result = validate_operation(record, args.head, registry, runtime, args.runtime_sha256, args.build_output)
        else:
            from publication_remote import GhTransport, GitHubAdapter, run_sync
            activation = checked_json(args.activation, args.activation_sha256, external=True)
            # Verification code and approved policy must be the actual main checkout.
            head = current.git(CONTROL, 'rev-parse', 'HEAD').decode().strip()
            frozen = current.git(CONTROL, 'show', head+':'+current.POLICY)
            if hashlib.sha256(frozen).hexdigest() != policy:
                raise ValueError('unlanded control/policy cannot operate as trusted main')
            current.verify(CONTROL, CONTROL)
            if args.state_dir is None or args.state_dir.resolve().is_relative_to(CONTROL):
                raise ValueError('external shared writer state directory required')
            with tempfile.TemporaryDirectory(prefix='trusted-sync-prepare-') as tmp:
                prepare = LocalPreparation(registry, repository=args.repository, policy=policy, directory=Path(tmp)/'prepared')
                transport = GhTransport(writer_token, state_dir=args.state_dir)
                api = GitHubAdapter(args.repository, transport)
                result = run_sync(api, prepare, repository=args.repository, policy=policy,
                    state_dir=args.state_dir, activation=activation, authorized=True)
        print(json.dumps(result, indent=2))
        return 0 if result['status'] in ('pass', 'ready', 'no-op') else 2
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(json.dumps({'version':1, 'status':'blocked', 'reason':str(error), 'publishable':False}))
        return 2


if __name__ == '__main__':
    sys.exit(main())
