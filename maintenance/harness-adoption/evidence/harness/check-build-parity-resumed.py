from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
base=root/'rollback-resumed/docs/.vitepress/dist'
candidate=root/'implementation-resumed/blog/.vitepress/dist'
def manifest(tree):
    return {str(p.relative_to(tree)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(tree.rglob('*')) if p.is_file()}
b,c=manifest(base),manifest(candidate)
assert b==c, {'removed':list(b.keys()-c.keys()),'added':list(c.keys()-b.keys()),'changed':[k for k in b.keys()&c.keys() if b[k]!=c[k]]}
routes=sorted(k for k in c if k.endswith('.html'))
assert routes==['404.html','about.html','index.html','post/course/cybersec/index.html','post/course/cybersec/what-is-safety.html','post/course/rm/index.html','post/course/rm/why-we-need-rm.html','posts.html']
assets={str(p.relative_to(root/'implementation-resumed/blog/public')):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((root/'implementation-resumed/blog/public').rglob('*')) if p.is_file()}
assert len(assets)==32
for path,sha in assets.items(): assert c[path]==sha
print(json.dumps({'status':'pass','surface':'actual baseline/candidate VitePress build output','built_files':len(c),'byte_identical':True,'routes':routes,'public_assets':assets,'all_built_file_sha256':c,'data_parity':'all emitted JS/chunks and route HTML byte-identical; includes generated post data','management_html':'none; exact route allowlist'},indent=2))
