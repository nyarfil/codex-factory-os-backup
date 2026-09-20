from __future__ import annotations
from dataclasses import dataclass,field,asdict
from typing import Any
@dataclass
class Resource:
 id:str; kind:str; name:str; path:str; scope:str; ownership:str='unknown'; enabled:bool|None=None; sha256:str|None=None; metadata:dict[str,Any]=field(default_factory=dict)
 def to_dict(self): return asdict(self)
@dataclass
class Finding:
 code:str; severity:str; summary:str; resource_ids:list[str]=field(default_factory=list); rationale:str=''; disposition:str='review'; action:str=''
 def to_dict(self): return asdict(self)
@dataclass
class GovernanceReport:
 codex_home:str; repo_root:str|None; resources:list[Resource]; findings:list[Finding]
 @property
 def summary(self):
  counts={}
  for f in self.findings: counts[f.severity]=counts.get(f.severity,0)+1
  return {'resource_count':len(self.resources),'finding_count':len(self.findings),'severity_counts':counts}
 def to_dict(self): return {'codex_home':self.codex_home,'repo_root':self.repo_root,'summary':self.summary,'resources':[x.to_dict() for x in self.resources],'findings':[x.to_dict() for x in self.findings]}
