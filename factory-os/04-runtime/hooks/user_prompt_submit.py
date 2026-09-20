from __future__ import annotations
import os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from factory_runtime.classifier import classify_prompt
from factory_runtime.hook_common import emit,read_event
from factory_runtime.audit import append_event
e=read_event(); prompt=str(e.get('prompt') or e.get('userPrompt') or e.get('message') or ''); hint=classify_prompt(prompt)
# Keep per-turn injection tiny. Detailed process stays in lazily-loaded Factory skills.
ctx=f'Factory OS: route={hint.factory}. For non-trivial work use that Factory skill; delegate only when independence/latency/context benefit exceeds subagent token cost; verify before claiming success.'
append_event(Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))/'factory-os'/'audit.jsonl',{'event':'prompt_route','domain':hint.factory,'why':hint.reason})
emit('UserPromptSubmit',additional_context=ctx)
