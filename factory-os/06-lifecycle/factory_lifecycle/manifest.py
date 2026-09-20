from __future__ import annotations
import json
from pathlib import Path
from .fsutil import atomic_write_json,sha256_file
def build_manifest(version,install_root,managed_paths,codex_home,user_home,guidance_path,hooks_path):
 rows=[]
 for p in managed_paths:
  if p.is_file(): rows.append({'path':str(p),'sha256':sha256_file(p)})
 return {'version':version,'install_root':str(install_root),'codex_home':str(codex_home),'user_home':str(user_home),'guidance_path':str(guidance_path),'hooks_path':str(hooks_path),'managed_files':rows}
def write_manifest(install_root:Path,m): p=install_root/'install-manifest.json'; atomic_write_json(p,m); return p
def load_manifest(install_root:Path):
 p=install_root/'install-manifest.json'
 try: return json.loads(p.read_text()) if p.exists() else None
 except Exception: return None
