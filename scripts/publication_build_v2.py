"""Fixed-command macOS build boundary for the explicit publication v2 controller."""
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile


def execute(old, verified, files, runtime, runtime_digest, output, export, physical, scan, signature_values):
    old.exact(runtime, ('version', 'node', 'node_version', 'dependencies'))
    if runtime['version'] != 1 or runtime['node_version'] != 'v24.13.0':
        raise old.Invalid('reviewed Node 24.13.0 runtime required; no installation')
    node = Path(runtime['node']).resolve(); dependencies = Path(runtime['dependencies']).resolve()
    if not node.is_file() or not dependencies.is_dir():
        raise old.Invalid('reviewed runtime unavailable')
    clean = {'PATH': str(node.parent) + ':/usr/bin:/bin', 'LANG': 'en_US.UTF-8'}
    version = subprocess.run([str(node), '--version'], capture_output=True, text=True, env=clean)
    if version.returncode or version.stdout.strip() != runtime['node_version']:
        raise old.Invalid('reviewed runtime identity/version mismatch')
    vitepress = (dependencies / 'vitepress/bin/vitepress.js').resolve()
    if not vitepress.is_file() or not vitepress.is_relative_to(dependencies):
        raise old.Invalid('reviewed VitePress toolchain unavailable')
    if not Path('/usr/bin/sandbox-exec').is_file():
        raise old.Invalid('enforced isolation unavailable; no unrestricted fallback')
    output = old.clean_location(output)
    if output.exists():
        raise old.Invalid('build output must be new')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='v2-isolated-build-', dir=output.parent) as temporary:
        controller = Path(temporary).resolve(); workspace = controller / 'workspace'; export(files, workspace)
        modules = workspace / 'node_modules'; modules.mkdir()
        for entry in dependencies.iterdir():
            if entry.name in ('.bin', '.vite-temp', '.cache'):
                continue
            if entry.name.startswith('@') and entry.is_dir():
                scope = modules / entry.name; scope.mkdir()
                for child in entry.iterdir():
                    (scope / child.name).symlink_to(child.resolve(), target_is_directory=child.is_dir())
            else:
                (modules / entry.name).symlink_to(entry.resolve(), target_is_directory=entry.is_dir())
        (modules / '.vite-temp').mkdir()
        scratch = controller / 'scratch'; scratch.mkdir()
        clean.update({'HOME': str(scratch), 'TMPDIR': str(scratch)})
        inside = workspace / 'isolation-inside.txt'; inside.write_text('INSIDE_READ_ALLOWED')
        outside = controller / 'outside.txt'; outside.write_text('OUTSIDE_READ_DENIED')
        profile = controller / 'build.sb'
        quote = json.dumps
        reads = [workspace, dependencies, node.parent.parent, Path('/System'), Path('/usr/lib'), Path('/usr/share'), Path('/usr/bin'), Path('/bin')]
        writes = [scratch, modules / '.vite-temp', workspace / 'blog/.vitepress/dist', workspace / 'blog/.vitepress/cache', workspace / 'blog/.vitepress/.temp']
        profile.write_text('(version 1)\n(deny default)\n(allow process* sysctl-read file-read-metadata)\n(allow file-read-data (literal "/"))\n' + '\n'.join('(allow file-read-data (subpath ' + quote(str(path)) + '))' for path in reads) + '\n' + '\n'.join('(allow file-write* (subpath ' + quote(str(path)) + '))' for path in writes) + '\n(allow file-read-data file-write-data (literal "/dev/null") (literal "/dev/tty"))\n')
        listener = socket.socket(); listener.bind(('127.0.0.1', 0)); listener.listen()
        port = listener.getsockname()[1]
        probe = controller / 'probe.cjs'
        probe.write_text("const fs=require('node:fs'),net=require('node:net');\n" +
            f"const inside={quote(str(inside))}, outside={quote(str(outside))}, target={quote(str(controller / 'outside-write.txt'))};\n" +
            "const result={inside:fs.readFileSync(inside,'utf8')==='INSIDE_READ_ALLOWED'};\n" +
            "for(const [key,action] of [['outside_read',()=>fs.readFileSync(outside)],['outside_write',()=>fs.writeFileSync(target,'DENIED')]]){try{action();result[key]='allowed'}catch(e){result[key]=['EACCES','EPERM'].includes(e.code)?'denied':e.code}}\n" +
            f"const client=net.connect({port},'127.0.0.1');client.setTimeout(1500);client.on('connect',()=>{{result.network='allowed';client.destroy();console.log(JSON.stringify(result))}});client.on('error',e=>{{result.network=['EACCES','EPERM'].includes(e.code)?'denied':e.code;console.log(JSON.stringify(result))}});client.on('timeout',()=>{{result.network='unverified';client.destroy();console.log(JSON.stringify(result))}});\n")
        # Probe script is reviewed controller input, never candidate-controlled code.
        with profile.open('a') as handle:
            handle.write('(allow file-read-data (literal ' + quote(str(probe)) + '))\n')
        prefix = ['/usr/bin/sandbox-exec', '-f', str(profile), str(node)]
        try:
            tested = subprocess.run(prefix + [str(probe)], cwd=workspace, capture_output=True, text=True, env=clean, timeout=20)
        finally:
            listener.close()
        if tested.returncode:
            raise old.Invalid('enforced isolation probe blocked: ' + tested.stderr.strip())
        isolation = json.loads(tested.stdout.strip().splitlines()[-1])
        if isolation != {'inside': True, 'outside_read': 'denied', 'outside_write': 'denied', 'network': 'denied'} or outside.read_text() != 'OUTSIDE_READ_DENIED' or (controller / 'outside-write.txt').exists():
            raise old.Invalid('enforced isolation sentinel failed')
        inside.unlink()
        command = prefix + [str(vitepress), 'build', 'blog']
        result = subprocess.run(command, cwd=workspace, capture_output=True, text=True, env=clean, timeout=180)
        if result.returncode:
            raise old.Invalid('isolated actual VitePress build failed: ' + result.stdout[-4000:] + result.stderr[-4000:])
        generated = workspace / 'blog/.vitepress/dist'
        actual = old.regular_files(generated)
        if not actual:
            raise old.Invalid('actual build output missing')
        output_scan = scan(actual, signature_values)
        # Source content was read-only in the child; controller checks complete original input too.
        source = physical(workspace, ('node_modules', 'blog/.vitepress/dist', 'blog/.vitepress/cache', 'blog/.vitepress/.temp'))
        expected_source = {p: entry for p, entry in source.items() if not p.startswith(('node_modules/', 'blog/.vitepress/dist/', 'blog/.vitepress/cache/', 'blog/.vitepress/.temp/'))}
        if expected_source != files:
            raise old.Invalid('isolated build changed source inputs')
        receipt = {'version': 2, 'status': 'pass', 'binding': old.digest(old.canonical(verified)), 'runtime_sha256': runtime_digest,
                   'node_version': runtime['node_version'], 'command': [str(node), str(vitepress), 'build', 'blog'],
                   'isolation': isolation, 'profile_sha256': old.digest(profile.read_bytes()), 'scan': output_scan,
                   'files': old.inventory(actual), 'output_manifest_sha256': old.digest(old.canonical(old.inventory(actual))),
                   'pr_ready': False, 'publishable': False, 'surface': 'isolated actual VitePress CLI build; no HTTP/browser/remote claim'}
        output.mkdir()
        shutil.copytree(generated, output / 'output')
        (output / 'build-receipt.json').write_bytes(old.canonical(receipt))
        (output / 'build-stdout.txt').write_text(result.stdout)
        (output / 'build-stderr.txt').write_text(result.stderr)
    return receipt
