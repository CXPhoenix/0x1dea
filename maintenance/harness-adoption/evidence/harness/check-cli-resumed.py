#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, re, subprocess, sys, tempfile

repo = Path(sys.argv[1]).resolve()
site = sys.argv[2]
node = '{EXISTING_NODE_BIN}/node'
tsx = repo / 'node_modules/tsx/dist/cli.mjs'
records = []
cases = [
    ('default', ['Hello World'], f'{site}/post/Hello_World.md', 'post_Hello_World'),
    ('category', ['Course Intro', '-c', 'course/intro'], f'{site}/post/course/intro/Course_Intro.md', 'post_course_intro_Course_Intro'),
    ('custom', ['Custom Note', '-d', f'{site}/post/special'], f'{site}/post/special/Custom_Note.md', 'post_special_Custom_Note'),
    ('root', ['Root Note', '-d', site], f'{site}/Root_Note.md', 'root_Root_Note'),
    ('unicode-space', ['繁中 Hello 測試'], f'{site}/post/繁中_Hello_測試.md', 'post_繁中_Hello_測試'),
    ('explicit-legacy-d', ['Legacy Note', '-d', 'docs/post/special'], 'docs/post/special/Legacy_Note.md', 'post_special_Legacy_Note'),
]
for name, args, article, asset in cases:
    with tempfile.TemporaryDirectory(prefix='harness-cli-') as temp:
        cwd = Path(temp)
        argv = [node, str(tsx), str(repo / 'scripts/vpHelper.ts'), 'new', 'post', *args]
        p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True)
        assert p.returncode == 0, (name, p.stdout, p.stderr)
        content = (cwd / article).read_text()
        assert re.search(r'createdTime: \d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\+08:00', content)
        expected_title = re.sub(r'\b\w', lambda m: m[0].upper(), args[0], flags=re.ASCII)
        assert content.startswith(f'---\ntitle: {expected_title}\ndescription:\ncreatedTime: ')
        assert content.endswith(f'thumbnail:\n---\n\n# {expected_title}\n')
        assert (cwd / site / 'public/assets' / asset).is_dir()
        assert str(cwd / article) in p.stdout and str(cwd / site / 'public/assets' / asset) in p.stdout
        before = {str(x.relative_to(cwd)): hashlib.sha256(x.read_bytes()).hexdigest() for x in cwd.rglob('*') if x.is_file()}
        duplicate = subprocess.run(argv, cwd=cwd, capture_output=True, text=True)
        after = {str(x.relative_to(cwd)): hashlib.sha256(x.read_bytes()).hexdigest() for x in cwd.rglob('*') if x.is_file()}
        assert duplicate.returncode == 1 and before == after and '已經存在' in duplicate.stderr
        if site == 'blog' and name == 'explicit-legacy-d':
            assert not (cwd / 'blog/post/special/Legacy_Note.md').exists()
        records.append({'case': name, 'argv': argv, 'cwd': temp, 'exit': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr, 'article': article, 'assets': f'{site}/public/assets/{asset}', 'duplicate_exit': duplicate.returncode, 'duplicate_preserved': before == after, 'sha256': before})
for name, args, expected in [('conflict', ['new','post','X','-c','course','-d',f'{site}/post/other'], '參數 -c 與 -d 不能同時使用。'), ('missing-title', ['new','post'], '請輸入文章名稱')]:
    with tempfile.TemporaryDirectory(prefix='harness-cli-negative-') as temp:
        argv = [node,str(tsx),str(repo/'scripts/vpHelper.ts'),*args]
        p = subprocess.run(argv,cwd=temp,capture_output=True,text=True)
        assert p.returncode == 1 and expected in p.stderr and not list(Path(temp).iterdir()), (name,p.stdout,p.stderr)
        records.append({'case':name,'argv':argv,'cwd':temp,'exit':p.returncode,'stderr':p.stderr,'no_writes':True})
print(json.dumps({'status':'pass','site_root':site,'repo':str(repo),'actual_cli_cases':len(records),'records':records},ensure_ascii=False,indent=2))
