from __future__ import annotations
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any

class Domain(str, Enum):
    GENERAL="general"; SOFTWARE="software"; CAD_3DP="cad_3dp"; RESEARCH="research"; DATA="data"; DOCUMENT="document"
class TaskType(str, Enum):
    CHAT="chat"; EXTRACTION="extraction"; EXPLORATION="exploration"; PLANNING="planning"; SYNTHESIS="synthesis"; REVIEW="review"; RESEARCH="research"
    IMPLEMENTATION="implementation"; REFACTOR="refactor"; DEBUG="debug"; TESTING="testing"; INTEGRATION="integration"; ARCHITECTURE="architecture"
    GEOMETRY_INSPECTION="geometry_inspection"; CAD_EDIT="cad_edit"; CAD_RECIPE="cad_recipe"; MECHANISM_DESIGN="mechanism_design"; DFM_3DP="dfm_3dp"; SIMULATION="simulation"; OPTIMIZATION="optimization"
class ModelTier(str, Enum): LUNA="luna"; TERRA="terra"; SOL="sol"; ASTRA="astra"
class ReasoningEffort(str, Enum): LOW="low"; MEDIUM="medium"; HIGH="high"; XHIGH="xhigh"; MAX="max"; ULTRA="ultra"
class BudgetMode(str, Enum): ECO="eco"; BALANCED="balanced"; QUALITY="quality"; MAX="max"

@dataclass(frozen=True)
class TaskContract:
    domain: Domain
    task_type: TaskType
    complexity:int=2; uncertainty:int=2; novelty:int=1; blast_radius:int=2; failure_count:int=0
    verification_strength:int=2; parallelizability:int=1; write_overlap_risk:int=2; context_size:int=2; safety_criticality:int=0
    deterministic_tools_available:bool=False; user_requires_max_quality:bool=False; budget_mode:BudgetMode=BudgetMode.BALANCED
    @classmethod
    def from_dict(cls,d:dict[str,Any])->"TaskContract":
        kw=dict(d); kw['domain']=Domain(kw.get('domain','general')); kw['task_type']=TaskType(kw.get('task_type','chat')); kw['budget_mode']=BudgetMode(kw.get('budget_mode','balanced'))
        for k in ('complexity','uncertainty','novelty','blast_radius','failure_count','verification_strength','parallelizability','write_overlap_risk','context_size','safety_criticality'):
            if k in kw: kw[k]=int(kw[k])
        return cls(**kw)
    def to_dict(self):
        d=asdict(self); d['domain']=self.domain.value; d['task_type']=self.task_type.value; d['budget_mode']=self.budget_mode.value; return d

@dataclass(frozen=True)
class ModelAssignment:
    tier:ModelTier; model_id:str; reasoning_effort:ReasoningEffort; role:str; write_allowed:bool=True
    def to_dict(self): return {'tier':self.tier.value,'model_id':self.model_id,'reasoning_effort':self.reasoning_effort.value,'role':self.role,'write_allowed':self.write_allowed}
@dataclass(frozen=True)
class ParallelismPlan:
    max_workers:int; read_workers:int; write_workers:int; strategy:str
@dataclass(frozen=True)
class VerificationPlan:
    level:str; independent_review:bool; deterministic:bool
@dataclass(frozen=True)
class RouteDecision:
    factory:Domain; primary:ModelAssignment; specialist:ModelAssignment|None; implementation_handoff:ModelAssignment|None
    parallelism:ParallelismPlan; verification:VerificationPlan; escalation_chain:tuple[str,...]; score:int; reasons:tuple[str,...]
    def to_dict(self):
        return {'factory':self.factory.value,'primary':self.primary.to_dict(),'specialist':self.specialist.to_dict() if self.specialist else None,
        'implementation_handoff':self.implementation_handoff.to_dict() if self.implementation_handoff else None,
        'parallelism':asdict(self.parallelism),'verification':asdict(self.verification),'escalation_chain':list(self.escalation_chain),'score':self.score,'reasons':list(self.reasons)}
