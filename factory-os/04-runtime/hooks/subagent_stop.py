from __future__ import annotations
import os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from factory_runtime.hook_common import read_event,emit
from factory_runtime.audit import append_event
e=read_event(); append_event(Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))/'factory-os'/'audit.jsonl',{'event':'subagent_stop','agent':e.get('agent_type') or e.get('agentType'),'last_message_present':bool(e.get('last_assistant_message'))}); emit('SubagentStop')
