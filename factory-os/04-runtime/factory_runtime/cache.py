from __future__ import annotations
import json,time
from pathlib import Path
from .models import ModelCapability,RuntimeSnapshot,QuotaSnapshot

def save_snapshot(path:Path,s:RuntimeSnapshot):
 path.parent.mkdir(parents=True,exist_ok=True); data=s.to_dict(); data['saved_at']=time.time(); path.write_text(json.dumps(data),encoding='utf-8')
def load_snapshot(path:Path)->RuntimeSnapshot|None:
 if not path.exists(): return None
 try:
  d=json.loads(path.read_text()); q=QuotaSnapshot.from_appserver(d['quota']) if isinstance(d.get('quota'),dict) else None
  return RuntimeSnapshot(tuple(ModelCapability(x['id'],tuple(x.get('reasoning_efforts',[])),x.get('display_name'),x.get('hidden',False)) for x in d.get('models',[])),q,d.get('codex_version'),bool(d.get('probe_ok')),tuple(d.get('warnings',[])))
 except Exception: return None
def snapshot_age_seconds(path:Path)->float|None:
 try: return max(0.0,time.time()-path.stat().st_mtime)
 except OSError: return None
