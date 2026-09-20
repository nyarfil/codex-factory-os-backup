from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class FactoryHint:
 factory:str; reason:str
 def __iter__(self): yield self.factory; yield self.reason

def classify_prompt(text:str)->FactoryHint:
 s=text.lower()
 groups=[
 ('cad_3dp',('cad','step','stl','3d print','3dp','fusion','freecad','mesh','mechanism','filament','orca','qidi','ソリッド','機構','3dモデル')),
 ('software',('code','python','javascript','typescript','rust','repo','bug','debug','api','function','class','test','refactor','software','codex','実装','コード')),
 ('data',('csv','spreadsheet','dataset','sql','metric','kpi','dataframe','データ分析')),
 ('research',('research','調べ','検索','source','論文','reddit','latest','最新','リサーチ')),
 ('document',('document','report','proposal','essay','文書','レポート'))]
 for domain,terms in groups:
  if any(x in s for x in terms): return FactoryHint(domain,f'{domain} cues')
 return FactoryHint('general','no specialist cue')
