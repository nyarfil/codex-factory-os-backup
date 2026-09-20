from __future__ import annotations
import shutil
from pathlib import Path
from .backup import create_backup
from .hooks import remove_factory_hooks
from .managed_block import remove_block
from .manifest import load_manifest
from .models import LifecycleReport
from .fsutil import sha256_file

def _expected_hashes(manifest): return {str(x.get('path')):x.get('sha256') for x in (manifest or {}).get('managed_files',[]) if x.get('path') and x.get('sha256')}
def _safe_remove_file(path:Path, hashes:dict[str,str], report:LifecycleReport, kind:str):
 expected=hashes.get(str(path))
 if expected and path.is_file() and sha256_file(path)!=expected:
  report.add(kind,'warning',str(path),'Locally modified Factory OS resource preserved during uninstall.'); return False
 if path.exists(): path.unlink(); report.add(kind,'ok',str(path),'Removed unmodified Factory OS-managed resource.'); return True
 return False

def uninstall(codex_home: Path, user_home: Path, version: str = "1.1.0", *, backup_base: Path | None = None, keep_runtime: bool = False) -> LifecycleReport:
 codex_home=codex_home.expanduser().resolve(); user_home=user_home.expanduser().resolve(); install_root=codex_home/'factory-os'/version
 report=LifecycleReport('uninstall',str(codex_home),str(user_home),str(install_root)); manifest=load_manifest(install_root); hashes=_expected_hashes(manifest)
 backup=create_backup(codex_home,user_home,backup_base); report.backup_path=str(backup); report.add('backup','ok',str(backup),'Created pre-uninstall backup.')
 guidance_candidates=[Path(manifest.get('guidance_path'))] if manifest and manifest.get('guidance_path') else [codex_home/'AGENTS.override.md',codex_home/'AGENTS.md']
 for path in guidance_candidates:
  if remove_block(path): report.add('global_guidance','ok',str(path),'Removed only the Factory OS managed block.')
 hooks_path=Path(manifest.get('hooks_path')) if manifest and manifest.get('hooks_path') else codex_home/'hooks.json'
 try:
  changed,count=remove_factory_hooks(hooks_path); report.add('hooks','ok' if changed else 'skipped',str(hooks_path),f'Removed {count} Factory OS hook group(s).')
 except Exception as exc: report.add('hooks','failed',str(hooks_path),f'Could not remove Factory OS hooks: {exc}')
 agent_source=install_root/'02-agents'/'agents'
 if agent_source.exists():
  for src in agent_source.glob('*.toml'): _safe_remove_file(codex_home/'agents'/src.name,hashes,report,'agent')
 skill_source=install_root/'03-skills'/'skills'
 if skill_source.exists():
  for src_dir in skill_source.iterdir():
   if not src_dir.is_dir(): continue
   dst=user_home/'.agents'/'skills'/src_dir.name
   if not dst.exists(): continue
   files=[x for x in dst.rglob('*') if x.is_file()]; modified=[]
   for f in files:
    exp=hashes.get(str(f))
    if exp is None or sha256_file(f)!=exp: modified.append(str(f))
   if modified: report.add('skill','warning',str(dst),'Locally modified/extra Factory skill files preserved during uninstall.',modified=modified)
   else: shutil.rmtree(dst); report.add('skill','ok',str(dst),'Removed unmodified Factory OS-managed entry skill.')
 if install_root.exists() and not keep_runtime:
  shutil.rmtree(install_root); report.add('runtime','ok',str(install_root),'Removed versioned Factory OS runtime.')
 elif keep_runtime: report.add('runtime','skipped',str(install_root),'Runtime retained by request.')
 return report
