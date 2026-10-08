"""Compare trusted local pre-cleanup and final build artifacts without publishing paths."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--before', type=Path, required=True)
parser.add_argument('--after', type=Path, default=Path('blog/.vitepress/dist'))
args = parser.parse_args()
base = '8890d5250e22ec4ee0e0493c1e72bab89d16489b'
before_css = next(args.before.glob('assets/style.*.css')).read_text()
after_css = next(args.after.glob('assets/style.*.css')).read_text()
scope_map = {}
for selector in ('.post-card', '.post-block', '.post-list-container'):
    pattern = re.escape(selector) + r'\[data-v-([a-f0-9]{8})\]'
    old_id = re.search(pattern, before_css)[1]
    new_id = re.search(pattern, after_css)[1]
    scope_map['data-v-' + new_id] = 'data-v-' + old_id

def normalize(text, final=False):
    if final:
        for new_id, old_id in scope_map.items():
            text = text.replace(new_id, old_id)
    text = re.sub(r'(/assets/(?:chunks/)?[^"<> /]+?)\.[A-Za-z0-9_-]{8}(?=\.(?:lean\.)?(?:js|css))', r'\1.HASH', text)
    text = re.sub(r'(window\.__VP_HASH_MAP__=JSON\.parse\().*?(\);)', r'\1"HASH_MAP"\2', text)
    return re.sub(r'class="([^"]*)"', lambda match: 'class="' + ' '.join(sorted(match[1].split())) + '"', text)

old_routes = {path.relative_to(args.before).as_posix() for path in args.before.rglob('*.html')}
new_routes = {path.relative_to(args.after).as_posix() for path in args.after.rglob('*.html')}
assert old_routes == new_routes, 'built route set changed'
for name in sorted(old_routes):
    assert normalize((args.before / name).read_text()) == normalize((args.after / name).read_text(), True), 'built HTML changed: ' + name
assert Counter(before_css.split('}')) == Counter(normalize(after_css, True).split('}')), 'CSS content blocks changed'
readonly = []
for name in filter(None, subprocess.check_output(['git', 'ls-files', '-z', 'blog'], text=True).split('\0')):
    if name.endswith(('.md', '.css')) or name.startswith('blog/public/'):
        pinned = subprocess.check_output(['git', 'show', base + ':' + name])
        current = Path(name).read_bytes()
        assert current == pinned, 'read-only site source changed: ' + name
        readonly.append({'path': name, 'sha256': hashlib.sha256(current).hexdigest()})
print(json.dumps({'status': 'pass', 'base': base, 'route_count': len(old_routes), 'normalized_html_equal': True, 'mapped_css_content_blocks_equal': True, 'scope_map': scope_map, 'readonly_site_files': readonly, 'limits': 'Normalizes generated asset/route hashes, corresponding component scope IDs and class order. CSS block order is reviewed separately; not pixel or browser-interaction equivalence.'}, indent=2))
