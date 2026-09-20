from pathlib import Path
import json, subprocess, sys, os
HERE=Path(__file__).resolve().parents[1]
def test_cli_writes_reports(tmp_path):
 home=tmp_path/'h'; codex=home/'.codex'; codex.mkdir(parents=True); (codex/'AGENTS.md').write_text('keep')
 j=tmp_path/'r.json'; m=tmp_path/'r.md'; env={**os.environ,'PYTHONPATH':str(HERE)}
 cp=subprocess.run([sys.executable,'-m','factory_governor.cli','--codex-home',str(codex),'--user-home',str(home),'--json-out',str(j),'--md-out',str(m),'--format','json'],capture_output=True,text=True,env=env,timeout=10)
 assert cp.returncode==0,cp.stderr; assert j.exists() and m.exists(); assert 'resources' in json.loads(j.read_text()); assert 'scan-only' in m.read_text().lower()
