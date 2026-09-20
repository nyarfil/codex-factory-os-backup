from __future__ import annotations
from dataclasses import dataclass,field,asdict
from typing import Any
@dataclass
class LifecycleItem:
 action:str; status:str; path:str|None=None; detail:str=''; extra:dict[str,Any]=field(default_factory=dict)
@dataclass
class LifecycleReport:
 operation:str; codex_home:str; user_home:str; install_root:str; backup_path:str|None=None; items:list[LifecycleItem]=field(default_factory=list)
 def add(self,action,status,path=None,detail='',**extra): self.items.append(LifecycleItem(action,status,path,detail,extra))
 @property
 def ok(self): return not any(x.status in {'failed','blocked'} for x in self.items)
 def to_dict(self): return {'operation':self.operation,'codex_home':self.codex_home,'user_home':self.user_home,'install_root':self.install_root,'backup_path':self.backup_path,'ok':self.ok,'items':[asdict(x) for x in self.items]}
