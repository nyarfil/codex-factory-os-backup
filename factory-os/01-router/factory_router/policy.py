from __future__ import annotations
from dataclasses import dataclass
from .models import Domain, TaskType, ModelTier, ReasoningEffort

# Preferred IDs only. Phase 4 resolves against model/list at runtime.
MODEL_IDS={ModelTier.LUNA:'gpt-5.6-luna',ModelTier.TERRA:'gpt-5.6-terra',ModelTier.SOL:'gpt-5.6',ModelTier.ASTRA:'gpt-6-astra'}
TIER_ORDER=(ModelTier.LUNA,ModelTier.TERRA,ModelTier.SOL,ModelTier.ASTRA)
@dataclass(frozen=True)
class Baseline: tier:ModelTier; effort:ReasoningEffort

DEFAULT=Baseline(ModelTier.TERRA,ReasoningEffort.MEDIUM)
BASELINES={
(Domain.GENERAL,TaskType.CHAT):Baseline(ModelTier.SOL,ReasoningEffort.MEDIUM),
(Domain.GENERAL,TaskType.EXTRACTION):Baseline(ModelTier.LUNA,ReasoningEffort.LOW),
(Domain.GENERAL,TaskType.EXPLORATION):Baseline(ModelTier.TERRA,ReasoningEffort.MEDIUM),
(Domain.GENERAL,TaskType.PLANNING):Baseline(ModelTier.SOL,ReasoningEffort.MEDIUM),
(Domain.GENERAL,TaskType.SYNTHESIS):Baseline(ModelTier.SOL,ReasoningEffort.MEDIUM),
(Domain.GENERAL,TaskType.REVIEW):Baseline(ModelTier.SOL,ReasoningEffort.HIGH),
(Domain.SOFTWARE,TaskType.EXPLORATION):Baseline(ModelTier.TERRA,ReasoningEffort.MEDIUM),
(Domain.SOFTWARE,TaskType.IMPLEMENTATION):Baseline(ModelTier.TERRA,ReasoningEffort.HIGH),
(Domain.SOFTWARE,TaskType.REFACTOR):Baseline(ModelTier.SOL,ReasoningEffort.HIGH),
(Domain.SOFTWARE,TaskType.DEBUG):Baseline(ModelTier.SOL,ReasoningEffort.HIGH),
(Domain.SOFTWARE,TaskType.TESTING):Baseline(ModelTier.TERRA,ReasoningEffort.MEDIUM),
(Domain.SOFTWARE,TaskType.REVIEW):Baseline(ModelTier.SOL,ReasoningEffort.HIGH),
(Domain.SOFTWARE,TaskType.INTEGRATION):Baseline(ModelTier.SOL,ReasoningEffort.HIGH),
(Domain.SOFTWARE,TaskType.ARCHITECTURE):Baseline(ModelTier.SOL,ReasoningEffort.HIGH),
(Domain.CAD_3DP,TaskType.GEOMETRY_INSPECTION):Baseline(ModelTier.TERRA,ReasoningEffort.MEDIUM),
(Domain.CAD_3DP,TaskType.CAD_EDIT):Baseline(ModelTier.TERRA,ReasoningEffort.HIGH),
(Domain.CAD_3DP,TaskType.CAD_RECIPE):Baseline(ModelTier.SOL,ReasoningEffort.MEDIUM),
(Domain.CAD_3DP,TaskType.MECHANISM_DESIGN):Baseline(ModelTier.SOL,ReasoningEffort.HIGH),
(Domain.CAD_3DP,TaskType.DFM_3DP):Baseline(ModelTier.SOL,ReasoningEffort.MEDIUM),
(Domain.CAD_3DP,TaskType.SIMULATION):Baseline(ModelTier.SOL,ReasoningEffort.HIGH),
(Domain.CAD_3DP,TaskType.OPTIMIZATION):Baseline(ModelTier.SOL,ReasoningEffort.HIGH),
(Domain.CAD_3DP,TaskType.REVIEW):Baseline(ModelTier.SOL,ReasoningEffort.HIGH),
(Domain.CAD_3DP,TaskType.INTEGRATION):Baseline(ModelTier.SOL,ReasoningEffort.HIGH),
(Domain.CAD_3DP,TaskType.RESEARCH):Baseline(ModelTier.TERRA,ReasoningEffort.HIGH),
(Domain.RESEARCH,TaskType.RESEARCH):Baseline(ModelTier.TERRA,ReasoningEffort.HIGH),
(Domain.RESEARCH,TaskType.EXTRACTION):Baseline(ModelTier.LUNA,ReasoningEffort.MEDIUM),
(Domain.RESEARCH,TaskType.SYNTHESIS):Baseline(ModelTier.SOL,ReasoningEffort.MEDIUM),
(Domain.RESEARCH,TaskType.REVIEW):Baseline(ModelTier.SOL,ReasoningEffort.HIGH),
(Domain.DATA,TaskType.EXTRACTION):Baseline(ModelTier.TERRA,ReasoningEffort.MEDIUM),
(Domain.DATA,TaskType.SYNTHESIS):Baseline(ModelTier.SOL,ReasoningEffort.MEDIUM),
(Domain.DOCUMENT,TaskType.EXTRACTION):Baseline(ModelTier.TERRA,ReasoningEffort.LOW),
(Domain.DOCUMENT,TaskType.SYNTHESIS):Baseline(ModelTier.TERRA,ReasoningEffort.MEDIUM),
(Domain.DOCUMENT,TaskType.IMPLEMENTATION):Baseline(ModelTier.TERRA,ReasoningEffort.MEDIUM),
}
def baseline_for(domain:Domain,task:TaskType)->Baseline: return BASELINES.get((domain,task),DEFAULT)
