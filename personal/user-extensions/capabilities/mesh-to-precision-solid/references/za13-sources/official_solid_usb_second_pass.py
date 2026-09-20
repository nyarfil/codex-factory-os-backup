import json
from pathlib import Path
from official_solid_full_diagnose import shapes
from official_solid_compare_geometry import read
from official_solid_exact_boundary_trial import rebuild
from official_solid_regularize import regularize
from OCP.TopAbs import TopAbs_SHELL
from OCP.BRepTools import BRepTools

OUT=Path('V:/mouse/outputs/ZA13_OFFICIAL_PRECISION_REPAIR_02')
source=read(OUT/'unified_13058.brep')
assert len(shapes(source,TopAbs_SHELL))==1
rebuilt,report=rebuild(shapes(source,TopAbs_SHELL)[0])
result,reg=regularize(rebuilt)
BRepTools.Write_s(result,str(OUT/'regularized_usb_second.brep'))
(OUT/'regularized_usb_second.json').write_text(json.dumps({'rebuild':report,'regularization':reg},indent=2))
