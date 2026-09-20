from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class ModelCapability:
 id:str; reasoning_efforts:tuple[str,...]=(); display_name:str|None=None; hidden:bool=False
 @property
 def supported_reasoning_efforts(self): return self.reasoning_efforts
 @classmethod
 def from_appserver(cls,d:dict[str,Any]):
  mid=str(d.get('id') or d.get('model')); raw=d.get('supportedReasoningEfforts') or d.get('reasoningEfforts') or d.get('reasoning_efforts') or []
  vals=[]
  for x in raw:
   if isinstance(x,str): vals.append(x)
   elif isinstance(x,dict): vals.append(str(x.get('effort') or x.get('name') or x.get('id') or ''))
  return cls(mid,tuple(x for x in vals if x),d.get('displayName') or d.get('name'),bool(d.get('hidden',False)))
@dataclass(frozen=True)
class RateWindow:
 used_percent:float|None=None; reset_at:str|None=None
@dataclass(frozen=True)
class RateGroup:
 primary:RateWindow|None=None; secondary:RateWindow|None=None
@dataclass(frozen=True)
class QuotaSnapshot:
 general:RateGroup|None=None; ordinary_usage_allowed:bool|None=None; rate_limit_reached_type:str|None=None; plan_type:str|None=None; raw:dict[str,Any]|None=None
 @classmethod
 def from_appserver(cls,d:dict[str,Any]):
  def win(x):
   if not isinstance(x,dict): return None
   v=x.get('usedPercent',x.get('used_percent'))
   return RateWindow(float(v) if v is not None else None,str(x.get('resetAt') or x.get('reset_at') or '') or None)
  src=d.get('rateLimits') if isinstance(d.get('rateLimits'),dict) else d
  # Codex responses have appeared both as rateLimits.primary/secondary and rateLimits.general.primary/secondary.
  g=src.get('general') if isinstance(src,dict) and isinstance(src.get('general'),dict) else src
  group=RateGroup(win(g.get('primary')),win(g.get('secondary'))) if isinstance(g,dict) else None
  return cls(group,src.get('ordinaryUsageAllowed') if isinstance(src,dict) else None,src.get('rateLimitReachedType') if isinstance(src,dict) else None,str(d.get('planType') or src.get('planType') or '') or None,d)
@dataclass(frozen=True)
class RuntimeSnapshot:
 models:tuple[ModelCapability,...]=(); quota:QuotaSnapshot|None=None; codex_version:str|None=None; probe_ok:bool=False; warnings:tuple[str,...]=()
 @property
 def model_ids(self): return tuple(m.id for m in self.models)
 def model(self,model_id:str): return next((m for m in self.models if m.id==model_id),None)
 def to_dict(self):
  return {'models':[{'id':m.id,'reasoning_efforts':list(m.reasoning_efforts),'display_name':m.display_name,'hidden':m.hidden} for m in self.models], 'quota':self.quota.raw if self.quota else None,'codex_version':self.codex_version,'probe_ok':self.probe_ok,'warnings':list(self.warnings)}
