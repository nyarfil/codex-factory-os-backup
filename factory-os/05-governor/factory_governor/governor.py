from __future__ import annotations
from pathlib import Path
from .models import GovernanceReport
from .policy import analyze
from .scanner import scan_environment
def govern(codex_home:Path, repo_root:Path|None=None, user_home:Path|None=None, source_root:Path|None=None)->GovernanceReport:
 resources=scan_environment(codex_home=codex_home,repo_root=repo_root,user_home=user_home); findings=analyze(resources)
 return GovernanceReport(str(codex_home.expanduser().resolve()),str(repo_root.expanduser().resolve()) if repo_root else None,resources,findings)
