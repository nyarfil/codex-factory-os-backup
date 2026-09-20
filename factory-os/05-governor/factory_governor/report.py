from __future__ import annotations
import json
from pathlib import Path
from .models import GovernanceReport
def render_markdown(r:GovernanceReport)->str:
 lines=['# Codex Environment Governance Report','', 'Mode: **scan-only**. This report does not delete or mutate resources. Factory OS is the user-managed control plane.', '', f"Resources: {len(r.resources)}  Findings: {len(r.findings)}",'','## Findings']
 for f in r.findings: lines.append(f"- **{f.severity.upper()} {f.code}** — {f.summary}. {f.action}".rstrip())
 if not r.findings: lines.append('- No findings.')
 lines+=['','## Inventory']
 for x in r.resources: lines.append(f"- `{x.kind}` **{x.name}** — {x.scope}/{x.ownership} — `{x.path}`")
 return '\n'.join(lines)+'\n'
def write_json(path:Path,r:GovernanceReport): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(r.to_dict(),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def write_markdown(path:Path,r:GovernanceReport): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(render_markdown(r),encoding='utf-8')
