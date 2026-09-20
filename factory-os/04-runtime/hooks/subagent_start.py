from __future__ import annotations
import os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from factory_runtime.audit import append_event
from factory_runtime.catalog import expected_agent_model
from factory_runtime.hook_common import emit,read_event
e=read_event(); name=e.get('agent_type') or e.get('agentType') or e.get('agentName') or e.get('name'); actual=e.get('model'); expected=expected_agent_model(str(name)) if name else None
aliases=lambda x: {'gpt-5.6','gpt-5.6-sol'} if x in {'gpt-5.6','gpt-5.6-sol'} else {x}
mismatch=bool(expected and actual and actual not in aliases(expected))
append_event(Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))/'factory-os'/'audit.jsonl',{'event':'subagent_start','agent':name,'expected_model':expected,'actual_model':actual,'mismatch':mismatch})
ctx='MODEL MISMATCH: do not report this worker as the intended tier; integrate cautiously and consider retry/fallback.' if mismatch else None
emit('SubagentStart',additional_context=ctx)
