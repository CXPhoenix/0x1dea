from collections import Counter
from pathlib import Path
import hashlib,json,re,subprocess
root=Path(__file__).resolve().parent/'implementation-resumed';results=[]
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
for en in sorted((root/'.proj.specs/_baseline/ee7fecf').glob('*/spec.en.md')):
 zh=en.with_name('spec.zh-TW.md');a=en.read_text();b=zh.read_text();source='openspec/specs/'+en.parent.name+'/spec.md'
 assert en.read_bytes()==subprocess.check_output(['git','show','ee7fecfff72f47abc735d26ac7e9a943de04ebbf:'+source],cwd=root)
 assert f'synced_from_sha: {blob(en.read_bytes())}' in b and 'synced_from: spec.en.md' in b
 count=lambda s,label:len(re.findall('^'+label,s,re.M))
 req=count(a,'### Requirement:');scen=count(a,'#### Scenario:')
 assert (req,scen)==(count(b,'### Requirement:'),count(b,'#### Scenario:'))
 conditions=lambda s:re.findall(r'\*\*(WHEN|THEN|AND|GIVEN)\*\*',s)
 assert conditions(a)==conditions(b)
 trace=lambda s:re.findall(r'<!-- @trace.*?-->',s,re.S)
 assert trace(a)==trace(b)
 codes=lambda s:Counter(re.findall(r'(?<!`)`(?!`)([^`\n]+)`(?!`)',s))
 assert not(codes(a)-codes(b)), f'missing inline code {en.parent.name}: {codes(a)-codes(b)}'
 assert 'historical review not recreated' in b and 'not recorded under harness' in b
 results.append({'capability':en.parent.name,'requirements':req,'scenarios':scen,'condition_clauses':len(conditions(a)),'trace_blocks':len(trace(a)),'source_git_blob':blob(en.read_bytes()),'english_sha256':hashlib.sha256(en.read_bytes()).hexdigest(),'zh_TW_sha256':hashlib.sha256(zh.read_bytes()).hexdigest(),'source_byte_identical':True,'scope':'full structural/clause/inline-code/trace audit; translation semantics were supplied by the full authoring pass, not independently human-certified'})
en=root/'.proj.specs/0001-harness-adoption/spec.en.md';zh=en.with_name('spec.zh-TW.md')
assert f'synced_from_sha: {blob(en.read_bytes())}' in zh.read_text()
assert len(re.findall(r'^## ',en.read_text(),re.M))==len(re.findall(r'^## ',zh.read_text(),re.M))==14
assert sum(r['requirements'] for r in results)==32 and sum(r['scenarios'] for r in results)==81 and sum(r['condition_clauses'] for r in results)==230 and sum(r['trace_blocks'] for r in results)==9
print(json.dumps({'status':'pass','translated_specs':7,'baseline_requirements':32,'baseline_scenarios':81,'preserved_conditions':230,'trace_blocks':9,'baseline_pairs':results,'adoption_english_git_blob':blob(en.read_bytes()),'adoption_zh_SHA256':hashlib.sha256(zh.read_bytes()).hexdigest()},indent=2))
