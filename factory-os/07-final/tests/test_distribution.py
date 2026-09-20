from pathlib import Path
import json,re,subprocess,sys,os,tomllib
ROOT=Path(__file__).resolve().parents[2]

def test_distribution_has_complete_runtime_surfaces():
    assert len(list((ROOT/'02-agents/agents').glob('*.toml')))==31
    assert len([p for p in (ROOT/'03-skills/skills').iterdir() if p.is_dir() and (p/'SKILL.md').exists()])==6
    for f in ('session_start.py','user_prompt_submit.py','pre_tool_use_agent.py','subagent_start.py','subagent_stop.py'):
        assert (ROOT/'04-runtime/hooks'/f).is_file()
    for f in ('install.ps1','update.ps1','doctor.ps1','uninstall.ps1','govern.ps1','INSTALL_WINDOWS.md'):
        assert (ROOT/f).exists()

def test_all_json_and_agent_toml_parse():
    for p in ROOT.rglob('*.json'): json.loads(p.read_text(encoding='utf-8'))
    for p in (ROOT/'02-agents/agents').glob('*.toml'): tomllib.loads(p.read_text(encoding='utf-8'))

def test_skill_local_reference_links_resolve():
    for p in (ROOT/'03-skills/skills').glob('*/SKILL.md'):
        text=p.read_text(encoding='utf-8')
        for rel in re.findall(r'`(references/[^`]+)`',text): assert (p.parent/rel).exists(),(p,rel)

def test_lifecycle_cli_install_doctor_uninstall(tmp_path):
    home=tmp_path/'home'; codex=home/'.codex'; codex.mkdir(parents=True)
    (codex/'AGENTS.md').write_text('existing\n'); (codex/'config.toml').write_text('[mcp_servers.x]\ncommand="x"\n')
    env={**os.environ,'PYTHONPATH':os.pathsep.join([str(ROOT/'06-lifecycle'),str(ROOT/'05-governor')])}
    base=[sys.executable,'-m','factory_lifecycle.cli']
    def run(args):
        cp=subprocess.run(base+args,capture_output=True,text=True,env=env,timeout=30); return cp,json.loads(cp.stdout)
    cp,r=run(['install','--source-root',str(ROOT),'--codex-home',str(codex),'--user-home',str(home)]); assert cp.returncode==0,(cp.stderr,r)
    cp,r=run(['doctor','--source-root',str(ROOT),'--codex-home',str(codex),'--user-home',str(home)]); assert cp.returncode==0,(cp.stderr,r)
    cp,r=run(['uninstall','--codex-home',str(codex),'--user-home',str(home)]); assert cp.returncode==0,(cp.stderr,r)
    assert 'existing' in (codex/'AGENTS.md').read_text(); assert 'mcp_servers.x' in (codex/'config.toml').read_text()
