from __future__ import annotations
import json,sys
from pathlib import Path
import pytest
HERE=Path(__file__).resolve().parents[1]; PROJECT=HERE.parent
sys.path[:0]=[str(HERE),str(PROJECT/'05-governor')]
from factory_lifecycle.installer import install,update
from factory_lifecycle.uninstaller import uninstall
from factory_lifecycle.doctor import doctor
from factory_lifecycle.cleanup import execute_cleanup
from factory_lifecycle.managed_block import BEGIN,END

def seed(tmp_path):
 home=tmp_path/'user'; codex=home/'.codex'; codex.mkdir(parents=True)
 (codex/'AGENTS.md').write_text('# Existing\nKeep this guidance.\n')
 (codex/'config.toml').write_text('[mcp_servers.keepme]\ncommand = "keep"\n')
 (codex/'hooks.json').write_text(json.dumps({'hooks':{'Stop':[{'hooks':[{'type':'command','command':'echo keep'}]}]}}))
 skill=home/'.agents/skills/existing'; skill.mkdir(parents=True); (skill/'SKILL.md').write_text('---\nname: existing\ndescription: keep\n---\n')
 agent=codex/'agents'; agent.mkdir(); (agent/'existing.toml').write_text('name="existing"\ndescription="keep"\ndeveloper_instructions="keep"\n')
 return home,codex

def test_install_preserves_existing_and_doctor(tmp_path):
 home,codex=seed(tmp_path); r=install(PROJECT,codex,home); assert r.ok, r.to_dict()
 assert 'Keep this guidance.' in (codex/'AGENTS.md').read_text(); assert BEGIN in (codex/'AGENTS.md').read_text()
 assert 'keepme' in (codex/'config.toml').read_text(); assert (home/'.agents/skills/existing/SKILL.md').exists(); assert (codex/'agents/existing.toml').exists()
 hooks=json.loads((codex/'hooks.json').read_text()); assert 'Stop' in hooks['hooks']; assert 'UserPromptSubmit' in hooks['hooks']
 d=doctor(codex,home,source_root=PROJECT); assert d.ok, d.to_dict()
 assert len(list((codex/'agents').glob('*.toml')))>=32
 assert len(list((home/'.agents/skills').glob('factory-*/SKILL.md')))==6

def test_preflight_collision_is_non_destructive(tmp_path):
 home,codex=seed(tmp_path); bad=codex/'agents/software_builder.toml'; bad.write_text('name="software_builder"\ndescription="mine"\ndeveloper_instructions="mine"\n')
 before={p:p.read_bytes() for p in [codex/'AGENTS.md',codex/'config.toml',codex/'hooks.json',bad]}
 r=install(PROJECT,codex,home); assert not r.ok
 for p,b in before.items(): assert p.read_bytes()==b
 assert not (codex/'factory-os/1.1.0').exists()

def test_uninstall_removes_only_factory_owned(tmp_path):
 home,codex=seed(tmp_path); assert install(PROJECT,codex,home).ok
 r=uninstall(codex,home); assert r.ok
 assert 'Keep this guidance.' in (codex/'AGENTS.md').read_text(); assert BEGIN not in (codex/'AGENTS.md').read_text()
 assert (codex/'agents/existing.toml').exists(); assert (home/'.agents/skills/existing/SKILL.md').exists(); assert 'keepme' in (codex/'config.toml').read_text()
 hooks=json.loads((codex/'hooks.json').read_text()); assert list(hooks['hooks'])==['Stop']

def test_cleanup_quarantine_and_restore(tmp_path):
 home,codex=seed(tmp_path); target=home/'.agents/skills/old'; target.mkdir(parents=True); (target/'SKILL.md').write_text('old')
 plan=tmp_path/'plan.json'; plan.write_text(json.dumps({'operations':[{'op':'quarantine_path','path':str(target)}]}))
 dry=execute_cleanup(plan,codex,home,apply=False); assert dry.ok and target.exists()
 applied=execute_cleanup(plan,codex,home,apply=True); assert applied.ok and not target.exists()
 q=next(Path(x.extra['quarantine_path']) for x in applied.items if x.action=='quarantine_path' and x.extra.get('quarantine_path'))
 restore=tmp_path/'restore.json'; restore.write_text(json.dumps({'operations':[{'op':'restore_path','path':str(q),'destination':str(target)}]}))
 rr=execute_cleanup(restore,codex,home,apply=True); assert rr.ok and target.exists()

def test_update_detects_modified_managed_agent(tmp_path):
 home,codex=seed(tmp_path); assert install(PROJECT,codex,home).ok
 target=codex/'agents/software_builder.toml'; target.write_text(target.read_text()+'\n# local edit\n')
 r=update(PROJECT,codex,home); assert not r.ok; assert any(i.action=='integrity' and i.status=='blocked' for i in r.items)

def test_incomplete_source_bundle_blocks_before_mutation(tmp_path):
    home,codex=seed(tmp_path); broken=tmp_path/'broken'; broken.mkdir()
    before=(codex/'AGENTS.md').read_bytes()
    r=install(broken,codex,home); assert not r.ok; assert any(i.action=='source_bundle' and i.status=='blocked' for i in r.items)
    assert (codex/'AGENTS.md').read_bytes()==before; assert not (codex/'factory-os/1.1.0').exists()

def test_uninstall_preserves_locally_modified_factory_agent(tmp_path):
    home,codex=seed(tmp_path); assert install(PROJECT,codex,home).ok
    a=codex/'agents/software_builder.toml'; a.write_text(a.read_text()+'\n# user customization\n')
    r=uninstall(codex,home); assert r.ok; assert a.exists(); assert any(i.action=='agent' and i.status=='warning' for i in r.items)

def test_uninstall_preserves_locally_modified_factory_skill(tmp_path):
    home,codex=seed(tmp_path); assert install(PROJECT,codex,home).ok
    s=home/'.agents/skills/factory-software/LOCAL.md'; s.write_text('user addition')
    r=uninstall(codex,home); assert r.ok; assert s.exists(); assert any(i.action=='skill' and i.status=='warning' for i in r.items)
