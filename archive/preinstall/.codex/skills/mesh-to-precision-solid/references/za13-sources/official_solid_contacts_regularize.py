import json
from official_solid_full_diagnose import load_input,shapes,OUT
from official_solid_regularize import regularize
from OCP.TopAbs import TopAbs_SOLID
from OCP.BRepTools import BRepTools

source=load_input();solids=shapes(source,TopAbs_SOLID)
for index in (160,161):
    result,record=regularize(solids[index-1])
    BRepTools.Write_s(result,str(OUT/f'regularized_original_{index}.brep'))
    (OUT/f'regularized_original_{index}.json').write_text(json.dumps(record,indent=2))
