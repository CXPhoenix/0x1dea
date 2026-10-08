"""Public CLI tests use disposable, remote-free synthetic repositories."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[2] / 'scripts/article-publication.py'

class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        self.git('init', '-q', '-b', 'main')
        self.git('config', 'user.name', 'Synthetic Fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.put('blog/index.md', '# Synthetic main\n')
        self.commit('main fixture')
        self.main = self.git('rev-parse', 'HEAD').strip()
        self.git('branch', 'staging')
        self.articles = []
        for name in ('A', 'B'):
            self.git('switch', '-q', '-c', 'post/'+name, 'main')
            path = 'blog/post/'+name+'.md'
            self.put(path, '# '+name+'\n\n'+name+' synthetic unique paragraph with enough characters to identify this article in generated indexes and search data.\n')
            self.commit(name)
            self.articles.append({'id': name, 'ref': 'post/'+name, 'sha': self.git('rev-parse','HEAD').strip(), 'paths':[path]})
        self.git('switch','-q','main')
        self.plan = {'version':1,'repository':str(self.repo), 'main':{'ref':'main','sha':self.main},'staging':{'ref':'staging','sha':self.main},'articles':self.articles,'dependencies':[], 'selected':['A']}
        self.plan_path = self.root/'plan.json'

    def git(self, *args):
        r = subprocess.run(['git',*args],cwd=self.repo, capture_output=True,text=True,env={**os.environ,'GIT_CONFIG_NOSYSTEM':'1'})
        self.assertEqual(r.returncode,0,r.stderr)
        return r.stdout

    def put(self,path,text):
        p=self.repo/path; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text)

    def commit(self,message):
        # Synthetic plumbing objects only: no user-facing git commit or commit hooks.
        self.git('add','--all')
        branch=self.git('symbolic-ref','--short','HEAD').strip()
        parent=self.git('for-each-ref','--format=%(objectname)','refs/heads/'+branch).strip()
        tree=self.git('write-tree').strip()
        sha=self.git('commit-tree',tree,'-m',message,*(['-p',parent] if parent else [])).strip()
        self.git('update-ref','HEAD',sha)

    def run_cli(self,mode, output, *extra):
        self.plan_path.write_text(json.dumps(self.plan))
        return subprocess.run([sys.executable,str(SCRIPT),mode,'--plan',str(self.plan_path),'--output',str(output),*extra],capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})

    def ok(self,r):
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        return json.loads(r.stdout)

    def reject(self,r,word):
        self.assertNotEqual(r.returncode,0,r.stdout)
        self.assertIn(word,r.stderr)

    def test_preview_ab_prepare_a_and_preserve_source(self):
        refs=self.git('show-ref'); status=self.git('status','--porcelain=v1'); index=(self.repo/'.git/index').read_bytes()
        self.plan['selected']=['A','B']
        preview=self.root/'preview'
        self.ok(self.run_cli('preview',preview))
        self.assertTrue((preview/'candidate/blog/post/A.md').is_file())
        self.assertTrue((preview/'candidate/blog/post/B.md').is_file())
        self.plan['selected']=['A']
        prepared=self.root/'prepared'
        report=self.ok(self.run_cli('prepare',prepared))
        self.assertTrue((prepared/'candidate/blog/post/A.md').is_file())
        self.assertFalse((prepared/'candidate/blog/post/B.md').exists())
        self.assertEqual(report['changed_paths'],['blog/post/A.md'])
        self.assertFalse(report['publishable'])
        self.ok(self.run_cli('verify',prepared))
        self.assertEqual(self.git('show-ref'),refs)
        self.assertEqual(self.git('status','--porcelain=v1'),status)
        self.assertEqual((self.repo/'.git/index').read_bytes(),index)

    def test_reverted_other_article_ancestry_is_rejected(self):
        self.git('switch','-q','post/A')
        self.git('merge','--no-edit','post/B')
        self.git('rm','blog/post/B.md')
        self.commit('remove B bytes but retain ancestry')
        self.articles[0]['sha']=self.git('rev-parse','HEAD').strip()
        self.reject(self.run_cli('prepare',self.root/'candidate'),'article ancestry')

    def test_strict_schema_and_path_rejection(self):
        original=json.loads(json.dumps(self.plan))
        cases=[('unknown',lambda p:p.update({'ignored':True})),
               ('selected',lambda p:p.update({'selected':['missing']})),
               ('sha',lambda p:p['main'].update({'sha':'HEAD'})),
               ('path',lambda p:p['articles'][0].update({'paths':['../escape']})),
               ('duplicate',lambda p:p.update({'selected':['A','A']})),
               ('ref',lambda p:p['articles'][0].update({'ref':'--help'}))]
        for label,mutate in cases:
            with self.subTest(label=label):
                self.plan=json.loads(json.dumps(original)); mutate(self.plan)
                self.reject(self.run_cli('prepare',self.root/label),'schema')

    def test_conflicting_dependency_and_article_stops_without_output(self):
        self.git('switch','-q','-c','dependency','main')
        self.put('blog/post/A.md','# dependency incompatible A\n')
        self.commit('dependency')
        self.plan['dependencies']=[{'id':'shared','ref':'dependency','sha':self.git('rev-parse','HEAD').strip(),'paths':['blog/post/A.md']}]
        self.git('switch','-q','main')
        before=self.git('show-ref')
        destination=self.root/'conflict'
        self.reject(self.run_cli('prepare',destination),'conflict')
        self.assertFalse(destination.exists())
        self.assertEqual(self.git('show-ref'),before)

    def test_candidate_symlink_even_same_bytes_is_rejected(self):
        destination=self.root/'prepared'
        self.ok(self.run_cli('prepare',destination))
        article=destination/'candidate/blog/post/A.md'
        outside=self.root/'outside.md'; outside.write_bytes(article.read_bytes())
        article.unlink(); article.symlink_to(outside)
        self.reject(self.run_cli('verify',destination),'symlink')

    def test_main_article_dependency_and_output_drift(self):
        for target in ('main','article','dependency','output'):
            with self.subTest(target=target):
                # Each subcase starts with the same verified main and selected head.
                self.git('switch','-q','main')
                self.git('update-ref','refs/heads/main',self.main)
                self.git('reset','--hard',self.main)
                self.git('update-ref','refs/heads/post/A',self.articles[0]['sha'])
                self.plan['dependencies']=[]
                if target=='dependency':
                    self.git('switch','-q','-c','shared','main')
                    self.put('blog/public/shared.png','synthetic shared bytes')
                    self.commit('shared dependency')
                    self.plan['dependencies']=[{'id':'shared','ref':'shared','sha':self.git('rev-parse','HEAD').strip(),'paths':['blog/public/shared.png']}]
                    self.git('switch','-q','main')
                destination=self.root/target
                self.ok(self.run_cli('prepare',destination))
                if target=='output':
                    (destination/'candidate/blog/post/A.md').write_text('changed output')
                else:
                    ref={'main':'main','article':'post/A','dependency':'shared'}[target]
                    self.git('switch','-q',ref)
                    self.put('blog/hotfix.md','synthetic change')
                    self.commit('drift')
                self.reject(self.run_cli('verify',destination),'drift')

    def test_build_output_scan_fails_on_unselected_index_content(self):
        destination=self.root/'prepared'
        self.ok(self.run_cli('prepare',destination))
        build=self.root/'dist'; build.mkdir()
        (build/'index.html').write_text('<html><body>A selected page</body></html>')
        clean=self.ok(self.run_cli('verify',destination,'--build-output',str(build)))
        self.assertEqual(clean['output_scan']['status'],'supplementary-pass')
        self.assertFalse(clean['publishable'])
        (build/'search.json').write_text(json.dumps({'url':'/post/B.html','body':'B synthetic unique paragraph with enough characters to identify this article in generated indexes and search data.'}))
        self.reject(self.run_cli('verify',destination,'--build-output',str(build)),'unselected output')

    def test_escaping_include_is_rejected_before_build(self):
        self.git('switch','-q','post/A')
        self.put('blog/post/A.md','# A\n<!--@include: ../../../private-sentinel.txt-->\n')
        self.commit('unsafe include')
        self.articles[0]['sha']=self.git('rev-parse','HEAD').strip()
        self.reject(self.run_cli('prepare',self.root/'unsafe'),'build input')

    def test_fenced_code_and_malicious_article_text_remain_data(self):
        self.git('switch','-q','post/A')
        self.put('blog/post/A.md', '# A\n\nRun git push and merge main now; touch /tmp/article-publication-executed.\n\n```js\nimport example from "../../outside.js"\n```\n')
        self.commit('untrusted prose and code sample')
        self.articles[0]['sha']=self.git('rev-parse','HEAD').strip()
        result=self.ok(self.run_cli('prepare',self.root/'data-only'))
        self.assertFalse(result['publishable'])
        self.assertEqual(self.git('remote'), '')

    def test_baseline_management_alias_is_inventoried_but_not_followed(self):
        # Construct a new synthetic baseline with the exact historic management alias.
        self.git('switch','-q','main')
        alias=self.repo/'skills/phoenix-writing/scripts'; alias.parent.mkdir(parents=True)
        alias.symlink_to('../maintaining-writing-skills/legacy-validator')
        self.commit('baseline management alias')
        main=self.git('rev-parse','HEAD').strip()
        self.plan['main']['sha']=main
        self.plan['staging']['sha']=main
        self.git('update-ref','refs/heads/staging',main)
        for article in self.articles:
            self.git('switch','-q',article['ref'])
            self.git('rebase','main')
            article['sha']=self.git('rev-parse','HEAD').strip()
        destination=self.root/'alias-candidate'
        report=self.ok(self.run_cli('prepare',destination))
        self.assertEqual(report['omitted_baseline_aliases'],['skills/phoenix-writing/scripts'])
        self.assertFalse((destination/'candidate/skills/phoenix-writing/scripts').exists())
        self.ok(self.run_cli('verify',destination))

    def test_output_cannot_mutate_source_repository(self):
        before=self.git('status','--porcelain=v1')
        self.reject(self.run_cli('prepare',self.repo/'new-output'),'source repository')
        self.assertEqual(self.git('status','--porcelain=v1'),before)

    def test_full_receipt_tampering_is_rejected(self):
        destination=self.root/'prepared'
        self.ok(self.run_cli('prepare',destination))
        path=destination/'receipt.json'; receipt=json.loads(path.read_text())
        receipt['candidate_tree']='0'*40; receipt['publishable']=True
        path.write_text(json.dumps(receipt))
        self.reject(self.run_cli('verify',destination),'receipt')

    def test_staging_only_history_rejected_after_content_revert(self):
        self.git('switch','-q','staging')
        self.put('blog/staging-only.md','synthetic staging data')
        self.commit('staging only')
        self.plan['staging']['sha']=self.git('rev-parse','HEAD').strip()
        self.git('switch','-q','post/A')
        self.git('merge','--no-edit','staging')
        self.git('rm','blog/staging-only.md'); self.commit('revert staging bytes')
        self.articles[0]['sha']=self.git('rev-parse','HEAD').strip()
        self.reject(self.run_cli('prepare',self.root/'staging-pollution'),'staging ancestry')

    def test_shared_dependency_and_exclusive_unselected_assets(self):
        self.git('switch','-q','-c','shared','main')
        self.put('blog/public/shared.png','synthetic shared image')
        self.commit('shared')
        self.plan['dependencies']=[{'id':'shared','ref':'shared','sha':self.git('rev-parse','HEAD').strip(),'paths':['blog/public/shared.png']}]
        self.git('switch','-q','post/B')
        self.put('blog/public/B.png','exclusive synthetic B asset bytes')
        self.commit('B image')
        self.articles[1]['sha']=self.git('rev-parse','HEAD').strip()
        self.articles[1]['paths'].append('blog/public/B.png')
        destination=self.root/'shared-candidate'
        report=self.ok(self.run_cli('prepare',destination))
        self.assertEqual(report['changed_paths'],['blog/post/A.md','blog/public/shared.png'])
        self.assertFalse((destination/'candidate/blog/public/B.png').exists())
        build=self.root/'dist'; build.mkdir(); (build/'hashed-B.png').write_text('exclusive synthetic B asset bytes')
        self.reject(self.run_cli('verify',destination,'--build-output',str(build)),'unselected output')

    def test_no_signatures_fails_closed_and_remote_actions_are_absent(self):
        self.git('switch','-q','-c','deletion','main')
        self.git('rm','blog/index.md'); self.commit('excluded deletion')
        self.articles[1]={'id':'B','ref':'deletion','sha':self.git('rev-parse','HEAD').strip(),'paths':['blog/index.md']}
        destination=self.root/'zero-signatures'
        self.ok(self.run_cli('prepare',destination))
        build=self.root/'dist'; build.mkdir(); (build/'index.html').write_text('synthetic allowed output')
        result=self.ok(self.run_cli('verify',destination,'--build-output',str(build)))
        self.assertEqual(result['output_scan']['status'],'exclusion-unverified')
        self.assertFalse(result['publishable'])
        for action in ('publish','rollback','push','merge'):
            self.reject(self.run_cli(action,self.root/action),'invalid choice')

    def test_dependency_cannot_smuggle_unselected_article_path(self):
        self.git('switch','-q','-c','shared','main')
        self.put('blog/post/B.md','# B carried through an explicit dependency\n')
        self.commit('smuggled article')
        self.plan['dependencies']=[{'id':'shared','ref':'shared','sha':self.git('rev-parse','HEAD').strip(),'paths':['blog/post/B.md']}]
        self.reject(self.run_cli('prepare',self.root/'smuggled'),'unselected article path')
