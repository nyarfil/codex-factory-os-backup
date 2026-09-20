import json,sys
from pathlib import Path
from official_solid_full_diagnose import shapes,bounds
from official_solid_compare_geometry import read
from OCP.TopAbs import TopAbs_SOLID,TopAbs_FACE
from OCP.TopTools import TopTools_ListOfShape
from OCP.BRepAlgoAPI import BRepAlgoAPI_Fuse,BRepAlgoAPI_Check
from OCP.BOPAlgo import BOPAlgo_CheckStatus
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepTools import BRepTools

OUT=Path('V:/mouse/outputs/ZA13_OFFICIAL_PRECISION_REPAIR_02');key=sys.argv[1]
cells=shapes(read(OUT/f'regularized_{key}.brep'),TopAbs_SOLID)
args=TopTools_ListOfShape();args.Append(cells[0]);tools=TopTools_ListOfShape()
for s in cells[1:]:tools.Append(s)
fuse=BRepAlgoAPI_Fuse();fuse.SetArguments(args);fuse.SetTools(tools);fuse.SetNonDestructive(True);fuse.Build()
assert fuse.IsDone();result=fuse.Shape()
report={'solids':len(shapes(result,TopAbs_SOLID)),'faces':len(shapes(result,TopAbs_FACE)),'valid':BRepCheck_Analyzer(result).IsValid(),'bounds':bounds(result)}
BRepTools.Write_s(result,str(OUT/f'unified_{key}.brep'));print(json.dumps(report),flush=True)
check=BRepAlgoAPI_Check(result,True,True);check.Perform()
report['self_intersections']=sum(r.GetCheckStatus()==BOPAlgo_CheckStatus.BOPAlgo_SelfIntersect for r in check.Result())
(OUT/f'unified_{key}.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
