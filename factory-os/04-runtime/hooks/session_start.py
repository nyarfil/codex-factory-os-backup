from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from factory_runtime.hook_common import emit,read_event
read_event(); emit('SessionStart',additional_context='Factory OS active: specialize by domain; cheap bounded workers first; one integration owner; verify real results; reserve Astra for hard bottlenecks.')
