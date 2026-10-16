"""Exact independently approved manual history; never establishes automation ownership."""
import hashlib
import json
from pathlib import Path
import re

import publication_remote as remote


def unique(pairs):
    result={}
    for key,value in pairs:
        if key in result:raise ValueError('duplicate manual-history key')
        result[key]=value
    return result


def external(path, digest, source):
    path=Path(path).absolute()
    if any(p.is_symlink() for p in (path,*path.parents)
           if str(p) not in ('/tmp','/var')):
        raise ValueError('linked manual-history authority')
    root=Path(__file__).resolve().parents[1]
    path=path.resolve()
    if any(path.is_relative_to(p) for p in (root, Path(source).resolve())) or not path.is_file():
        raise ValueError('manual-history authority must be regular and external')
    raw=path.read_bytes()
    if not isinstance(digest,str) or not re.fullmatch('[0-9a-f]{64}',digest) or hashlib.sha256(raw).hexdigest()!=digest:
        raise ValueError('independent manual-history digest mismatch')
    return json.loads(raw,object_pairs_hook=unique)


class ManualHistory:
    def __init__(self,path,digest,repository,*,source):
        self.path,self.digest,self.repository,self.source=path,digest,repository,Path(source).resolve()

    def observe(self,api,refs,prs):
        grant=external(self.path,self.digest,self.source)
        if (not isinstance(grant,dict) or set(grant)!={'version','repository','branch','manual','approval'}
                or type(grant['version']) is not int or grant['version']!=1
                or grant['repository']!=self.repository or grant['branch']!=remote.BRANCH):
            raise ValueError('manual-history scope mismatch')
        approval=grant['approval']
        if not isinstance(approval,dict) or set(approval)!={'path','sha256'}:
            raise ValueError('manual-history independent receipt required')
        receipt=external(approval['path'],approval['sha256'],self.source)
        expected=grant['manual']
        fields={'number','repository','branch','base','base_sha','head','merge','tree','actor'}
        if (not isinstance(expected,dict) or set(expected)!=fields
                or type(expected['number']) is not int or expected['number']<=0
                or expected['repository']!=self.repository or expected['branch']!=remote.BRANCH
                or expected['base']!='staging'
                or any(not isinstance(expected[key],str) or not re.fullmatch('[0-9a-f]{40}',expected[key])
                       for key in ('base_sha','head','merge','tree'))
                or not isinstance(expected['actor'],dict) or set(expected['actor'])!={'id','login','type'}
                or type(expected['actor']['id']) is not int or expected['actor']['id']<=0
                or expected['actor']['type'] not in ('User','Bot')
                or not isinstance(expected['actor']['login'],str) or not expected['actor']['login']):
            raise ValueError('manual-history identity mismatch')
        if (not isinstance(receipt,dict) or set(receipt)!={'version','approval','manual'}
                or type(receipt['version']) is not int or receipt['version']!=1
                or not isinstance(receipt['approval'],str) or not receipt['approval'].strip()
                or receipt['manual']!=expected):
            raise ValueError('manual-history approval binding mismatch')
        found=[p for p in prs if p.get('number')==expected['number']]
        if len(found)!=1:raise ValueError('manual-history pull missing or ambiguous')
        observed=api.pull_details(expected['number'])
        for value, checked_fields in ((found[0], fields-{'base_sha','merge','tree','actor'}), (observed, fields)):
            if (any(value.get(key)!=expected[key] for key in checked_fields)
                    or value.get('state')!='closed' or value.get('merged') is not True
                    or value.get('owner') is not None or value.get('operation') is not None):
                raise ValueError('manual-history observed pull changed or claims ownership')
        commit=api.commit(expected['merge'])
        if (commit.get('tree')!=expected['tree']
                or not api.is_ancestor(expected['base_sha'],expected['head'])
                or not api.is_ancestor(expected['head'],expected['merge'])
                or not api.is_ancestor(expected['merge'],refs['staging'])):
            raise ValueError('manual-history tree/ancestry mismatch')
        return dict(expected,classification='manual',approval_sha256=approval['sha256'])
