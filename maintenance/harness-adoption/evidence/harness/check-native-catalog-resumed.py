#!/usr/bin/env python3
"""Query a new native app-server's skills catalog without generating a model response."""
from pathlib import Path
import hashlib, json, selectors, subprocess, time

root = Path(__file__).resolve().parent
out = root / 'evidence/resumed'
argv = ['{EXISTING_CODEX_BIN}/codex', '--no-daemon', 'app-server', '--stdio']
requests = [
 {'id': 1, 'method': 'initialize', 'params': {'clientInfo': {'name': 'harness_adoption_check', 'version': '1.0'}}},
 {'method': 'initialized', 'params': {}},
 {'id': 2, 'method': 'skills/list', 'params': {'cwds': [str(root/'implementation-resumed')], 'forceReload': True}},
]
started = time.time()
with (out/'native-catalog-stderr.log').open('wb') as stderr:
    process = subprocess.Popen(argv,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=stderr,text=True,bufsize=1)
    sel = selectors.DefaultSelector();sel.register(process.stdout,selectors.EVENT_READ)
    responses=[]
    def send(request):
        process.stdin.write(json.dumps(request)+'\n');process.stdin.flush()
    def receive(wanted):
        deadline = time.monotonic()+30
        while time.monotonic()<deadline:
            if sel.select(timeout=1):
                line=process.stdout.readline()
                if not line: raise RuntimeError('app-server exited before response')
                message=json.loads(line);responses.append(message)
                if message.get('id')==wanted: return message
        raise TimeoutError('native app-server response timeout')
    try:
        send(requests[0]);initialized=receive(1)
        if 'error' in initialized: raise RuntimeError(initialized['error'])
        send(requests[1]);send(requests[2]);catalog=receive(2)
        if 'error' in catalog: raise RuntimeError(catalog['error'])
        (out/'native-catalog-response.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
        data=catalog['result']['data'][0]
        location=str(root/'implementation-resumed/.agents/skills/')
        project=[s for s in data['skills'] if s['path'].startswith(location)]
        expected={p.name for p in (root/'implementation-resumed/.agents/skills').iterdir() if (p/'SKILL.md').is_file()}
        actual={s['name'] for s in project}
        assert actual==expected and len(project)==35 and all(s['scope']=='repo' and s['enabled'] for s in project), (len(project),expected-actual,actual-expected)
        assert not data['errors'],data['errors']
        product=[s for s in project if s['name'] in {'phoenix-writing','maintaining-writing-skills','creating-vitepress-post'}]
        proof={'status':'pass','argv':argv,'started_epoch':started,'ended_epoch':time.time(),'native_fresh_process':True,'forceReload':True,'model_response_required':False,'project_count':len(project),'project_skills':project,'product_skill_locations':product,'errors':data['errors'],'response_sha256':hashlib.sha256((out/'native-catalog-response.json').read_bytes()).hexdigest(),'limitation':'Native Codex discovery only; no claim of fresh Claude runtime discovery or CLI model generation.'}
        (out/'native-catalog-proof.json').write_text(json.dumps(proof,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({'status':'pass','project_count':len(project),'product':product,'response_sha256':proof['response_sha256']},ensure_ascii=False,indent=2))
    finally:
        process.terminate()
        try:process.wait(timeout=5)
        except subprocess.TimeoutExpired:process.kill();process.wait()
        (out/'native-catalog-rpc.json').write_text(json.dumps({'requests':requests,'responses':responses},ensure_ascii=False,indent=2)+'\n')
