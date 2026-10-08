"""Bounded read-only skills/list probe; no thread/session/model requests."""
import json
from pathlib import Path
import selectors
import subprocess
import time

root=Path(__file__).resolve().parents[3]
p=subprocess.Popen(['codex','app-server','--stdio'],cwd=root,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True,bufsize=1)
selector=selectors.DefaultSelector();selector.register(p.stdout,selectors.EVENT_READ)
def request(i,method,params):
    p.stdin.write(json.dumps({'id':i,'method':method,'params':params})+'\n');p.stdin.flush()
    deadline=time.monotonic()+20
    while time.monotonic()<deadline:
        if not selector.select(timeout=1):
            if p.poll() is not None:raise RuntimeError('app-server exited before response')
            continue
        line=p.stdout.readline()
        if not line:raise RuntimeError('app-server exited before response')
        response=json.loads(line)
        if response.get('id')==i:return response
    raise RuntimeError('native discovery timeout at '+method)
try:
    init=request(1,'initialize',{'clientInfo':{'name':'article-publication-discovery','version':'1'},'capabilities':{'explicitGatewayOauth':True}})
    if 'error' in init:raise RuntimeError('initialize failed')
    p.stdin.write(json.dumps({'method':'initialized'})+'\n');p.stdin.flush()
    response=request(2,'skills/list',{'cwds':[str(root)],'forceReload':True})
    matches=[]
    for item in response.get('result',{}).get('data',[]):
        for skill in item.get('skills',[]):
            if skill.get('name')=='managing-article-publication':
                matches.append({k:v for k,v in skill.items() if k in ('name','description','path','scope','enabled','invocationPolicy')})
    report={'runtime':'Codex app-server','method':'skills/list','fresh_reload':True,'status':'pass' if matches else 'blocked','matching_skills':matches,'thread_or_session_requests':False,'trust_settings_credentials_changed':False}
except Exception as exc:
    report={'runtime':'Codex app-server','status':'blocked','reason':str(exc),'thread_or_session_requests':False}
finally:
    p.terminate()
    try:p.wait(timeout=3)
    except subprocess.TimeoutExpired:p.kill();p.wait()
print(json.dumps(report))
Path(__file__).with_name('codex-discovery-escalated.json').write_text(json.dumps(report,indent=2)+'\n')
