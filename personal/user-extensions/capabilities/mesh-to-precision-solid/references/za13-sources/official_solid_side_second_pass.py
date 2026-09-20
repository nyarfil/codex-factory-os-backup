import json
from official_solid_full_diagnose import shapes,OUT
from official_solid_compare_geometry import read
from official_solid_exact_boundary_trial import rebuild
from official_solid_regularize import regularize
from OCP.TopAbs import TopAbs_SHELL
from OCP.BRepTools import BRepTools

source=read(OUT/'regularized_101603.brep')
assert len(shapes(source,TopAbs_SHELL))==1
rebuilt,report=rebuild(shapes(source,TopAbs_SHELL)[0])
BRepTools.Write_s(rebuilt,str(OUT/'side_second_rebuilt.brep'))
result,reg=regularize(rebuilt)
BRepTools.Write_s(result,str(OUT/'regularized_side_second.brep'))
(OUT/'regularized_side_second.json').write_text(json.dumps({'rebuild':report,'regularization':reg},indent=2))
