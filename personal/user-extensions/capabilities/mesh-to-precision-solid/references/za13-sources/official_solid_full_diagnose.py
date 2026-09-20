"""Offline topology repair trial on immutable Fusion export. No CAD output yet."""
import json
import time
import hashlib
from pathlib import Path
from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone
from OCP.TopExp import TopExp
from OCP.TopAbs import TopAbs_FACE, TopAbs_SHELL, TopAbs_SOLID, TopAbs_EDGE, TopAbs_VERTEX
from OCP.TopTools import TopTools_IndexedMapOfShape
from OCP.TopoDS import TopoDS
from OCP.BRep import BRep_Tool
from OCP.BRepBuilderAPI import BRepBuilderAPI_Sewing, BRepBuilderAPI_MakeSolid
from OCP.BRepBndLib import BRepBndLib
from OCP.Bnd import Bnd_Box
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
from OCP.BRepTools import BRepTools
from OCP.BRep import BRep_Builder
from OCP.TopoDS import TopoDS_Shape

OUT = Path('V:/mouse/outputs/ZA13_OFFICIAL_PRECISION_REPAIR_02')
INPUT = OUT / 'original_all_bodies.step'
TOLERANCE_MM = 0.006


def shapes(shape, kind):
    index = TopTools_IndexedMapOfShape()
    TopExp.MapShapes_s(shape, kind, index)
    return [index.FindKey(i) for i in range(1, index.Extent()+1)]


def bounds(shape):
    box = Bnd_Box()
    BRepBndLib.AddOptimal_s(shape, box, False, False)
    return list(box.Get())


def load_input():
    cache=OUT/'original_import_cache.brep'
    stamp=OUT/'original_import_cache.json'
    digest=hashlib.file_digest(open(INPUT,'rb'),'sha256').hexdigest()
    if cache.is_file() and stamp.is_file():
        saved=json.loads(stamp.read_text())
        if saved['step_sha256']==digest and saved['brep_sha256']==hashlib.file_digest(open(cache,'rb'),'sha256').hexdigest():
            shape=TopoDS_Shape()
            assert BRepTools.Read_s(shape,str(cache),BRep_Builder())
            return shape
    reader=STEPControl_Reader()
    assert reader.ReadFile(str(INPUT))==IFSelect_RetDone
    reader.TransferRoots()
    shape=reader.OneShape()
    assert BRepTools.Write_s(shape,str(cache))
    stamp.write_text(json.dumps({'step_sha256':digest,'brep_sha256':hashlib.file_digest(open(cache,'rb'),'sha256').hexdigest()}),encoding='utf-8')
    return shape


def main():
    started = time.monotonic()
    original = load_input()
    face_count = len(shapes(original, TopAbs_FACE))
    solids = shapes(original, TopAbs_SOLID)
    shells = shapes(original, TopAbs_SHELL)
    solid_shells=TopTools_IndexedMapOfShape()
    for solid in solids:
        TopExp.MapShapes_s(solid,TopAbs_SHELL,solid_shells)
    opened = [s for s in shells if not solid_shells.Contains(s)]
    # STEP text audit resolves all 189 named bodies. Export split four faces
    # across bodies 140, 143, 181 and expanded multi-lump bodies into solids.
    if face_count != 359903:
        details=[{'faces':len(shapes(s,TopAbs_FACE)),'closed':BRep_Tool.IsClosed_s(s),'bounds_mm':bounds(s)} for s in shells]
        (OUT/'import_face_discrepancy.json').write_text(json.dumps({'faces':face_count,'solids':len(solids),'shells':details},indent=2),encoding='utf-8')
        raise ValueError('Input face discrepancy recorded for investigation')
    print(json.dumps({'stage':'loaded','faces':face_count,'solids':len(solids),'shells':len(shells),'open_shells':len(opened),'seconds':time.monotonic()-started}),flush=True)
    assert sum(len(shapes(s,TopAbs_FACE)) for s in solids+opened)==face_count, 'Input faces lost or double-counted'
    sewing = BRepBuilderAPI_Sewing(TOLERANCE_MM)
    for shell in opened:
        sewing.Add(shell)
    sewing.Perform()
    result = sewing.SewedShape()
    assert BRepTools.Write_s(result,str(OUT/'sewing_trial_cache.brep'))
    shell_items=shapes(result,TopAbs_SHELL)
    edge_maps=[]
    for shell in shell_items:
        em=TopTools_IndexedMapOfShape()
        TopExp.MapShapes_s(shell,TopAbs_EDGE,em)
        edge_maps.append(em)
    free=[]
    for i in range(1,sewing.NbFreeEdges()+1):
        edge=sewing.FreeEdge(i)
        owners=[len(shapes(shell_items[k],TopAbs_FACE)) for k,em in enumerate(edge_maps) if em.Contains(edge)]
        points=[list(BRep_Tool.Pnt_s(TopoDS.Vertex_s(v)).Coord()) for v in shapes(edge,TopAbs_VERTEX)]
        free.append({'index':i,'shell_faces':owners,'endpoints_mm':points})
    (OUT/'remaining_free_edges.json').write_text(json.dumps(free,indent=2),encoding='utf-8')
    rows = []
    for shell in shapes(result, TopAbs_SHELL):
        closed = BRep_Tool.IsClosed_s(shell)
        info = {'faces':len(shapes(shell,TopAbs_FACE)), 'closed':closed, 'bounds_mm':bounds(shell)}
        if closed:
            solid = BRepBuilderAPI_MakeSolid(TopoDS.Shell_s(shell)).Solid()
            props = GProp_GProps()
            BRepGProp.VolumeProperties_s(solid,props)
            info['volume_mm3'] = props.Mass()
            info['valid'] = BRepCheck_Analyzer(solid).IsValid()
        rows.append(info)
    result_info = {
        'input':str(INPUT), 'tolerance_mm':TOLERANCE_MM,
        'original_solids_untouched':len(solids),
        'original_open_faces':sum(len(shapes(s,TopAbs_FACE)) for s in opened),
        'result_faces':len(shapes(result,TopAbs_FACE)),
        'free_edges':sewing.NbFreeEdges(), 'multiple_edges':sewing.NbMultipleEdges(),
        'deleted_faces':sewing.NbDeletedFaces(),
        'result_shells':sorted(rows,key=lambda r:r['faces'],reverse=True),
        'seconds':time.monotonic()-started,
    }
    (OUT/'full_sewing_diagnosis.json').write_text(json.dumps(result_info,indent=2),encoding='utf-8')
    print(json.dumps(result_info),flush=True)


if __name__ == '__main__':
    main()
