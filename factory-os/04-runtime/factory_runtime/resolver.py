from __future__ import annotations
from dataclasses import dataclass
from .models import RuntimeSnapshot
from .quota_policy import astra_allowed
ALIASES={
 'gpt-5.6-luna':('gpt-5.6-luna','gpt-5.6-terra','gpt-5.6','gpt-5.6-sol','gpt-6-astra'),
 'gpt-5.6-terra':('gpt-5.6-terra','gpt-5.6','gpt-5.6-sol','gpt-5.6-luna','gpt-6-astra'),
 'gpt-5.6':('gpt-5.6','gpt-5.6-sol','gpt-5.6-terra','gpt-6-astra','gpt-5.6-luna'),
 'gpt-5.6-sol':('gpt-5.6-sol','gpt-5.6','gpt-5.6-terra','gpt-6-astra','gpt-5.6-luna'),
 'gpt-6-astra':('gpt-6-astra','gpt-5.6','gpt-5.6-sol','gpt-5.6-terra','gpt-5.6-luna')}
EFFORT_ORDER=('low','medium','high','xhigh','max','ultra')
@dataclass(frozen=True)
class Assignment:
 model:str; effort:str; degraded:bool=False; reason:str=''
@dataclass(frozen=True)
class ResolvedRoute:
 primary:Assignment; specialist:Assignment|None; specialist_suppressed:bool=False; reasons:tuple[str,...]=()
class RuntimeResolver:
 def __init__(self,snapshot:RuntimeSnapshot): self.snapshot=snapshot
 def assignment(self,model:str,effort:str='medium')->Assignment:
  caps={m.id:m for m in self.snapshot.models}
  if not caps: return Assignment(model,effort,False,'model/list unavailable; preserve configured value')
  actual=next((x for x in ALIASES.get(model,(model,)) if x in caps),None) or next(iter(caps))
  supported=caps[actual].reasoning_efforts; ae=effort
  if supported and effort not in supported:
   target=EFFORT_ORDER.index(effort) if effort in EFFORT_ORDER else 1
   ae=min(supported,key=lambda x:abs((EFFORT_ORDER.index(x) if x in EFFORT_ORDER else 1)-target))
  return Assignment(actual,ae,actual!=model or ae!=effort,'resolved against model/list')
 def resolve(self,route_or_model,task_meta=None):
  if isinstance(route_or_model,str): return self.assignment(route_or_model,str(task_meta or 'medium'))
  route=route_or_model; meta=task_meta or {}; reasons=[]
  p=route.get('primary') or {}; primary=self.assignment(p.get('model_id','gpt-5.6'),p.get('reasoning_effort','medium'))
  specialist=None; suppressed=False; s=route.get('specialist')
  if s:
   allowed,why=astra_allowed(self.snapshot.quota,score=int(route.get('score',0)),failure_count=int(meta.get('failure_count',0)),budget_mode=str(meta.get('budget_mode','balanced')),explicit_max_quality=bool(meta.get('user_requires_max_quality',False)))
   reasons.append(why)
   if allowed: specialist=self.assignment(s.get('model_id','gpt-6-astra'),s.get('reasoning_effort','medium'))
   else: suppressed=True
  return ResolvedRoute(primary,specialist,suppressed,tuple(reasons))
