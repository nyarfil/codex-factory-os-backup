from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
def fm(text):
 lines=text.splitlines(); out={}
 if not lines or lines[0].strip()!='---': return out
 for line in lines[1:]:
  if line.strip()=='---': break
  if ':' in line:
   k,v=line.split(':',1); out[k.strip()]=v.strip()
 return out

def test_six_entry_skills_exist():
 dirs=sorted(p for p in (ROOT/'skills').iterdir() if p.is_dir())
 assert len(dirs)==6
 assert {p.name for p in dirs}=={'factory-general','factory-software','factory-cad-3dp','factory-research','factory-data','factory-document'}

def test_frontmatter_and_descriptions_are_bounded():
 for p in (ROOT/'skills').glob('*/SKILL.md'):
  text=p.read_text(); meta=fm(text); assert meta.get('name')==p.parent.name; assert meta.get('description'); assert len(meta['description'])<320

def test_referenced_local_files_exist():
 for p in (ROOT/'skills').glob('*/SKILL.md'):
  text=p.read_text()
  for rel in re.findall(r'`(references/[^`]+)`',text): assert (p.parent/rel).exists(), (p,rel)

def test_catalog_matches_skills():
 d=json.loads((ROOT/'catalog/factory_skill_map.json').read_text()); names={p.parent.name for p in (ROOT/'skills').glob('*/SKILL.md')}
 assert {v['skill'] for v in d['domains'].values()}==names

def test_general_is_not_implicit():
 d=json.loads((ROOT/'catalog/factory_skill_map.json').read_text()); assert d['domains']['general']['implicit'] is False
