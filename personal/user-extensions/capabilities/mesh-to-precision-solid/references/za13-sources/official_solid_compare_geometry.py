"""Compare imported CAD geometry with actual vertex coordinates and plane equations."""
import json
import hashlib
import sys
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone
from OCP.TopAbs import TopAbs_FACE, TopAbs_VERTEX, TopAbs_SOLID, TopAbs_SHELL
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Plane
from OCP.TopoDS import TopoDS
from OCP.BRep import BRep_Tool
from official_solid_full_diagnose import shapes, bounds


def read(path):
    if path.suffix=='.brep':
        from OCP.BRepTools import BRepTools
        from OCP.BRep import BRep_Builder
        from OCP.TopoDS import TopoDS_Shape
        shape=TopoDS_Shape();assert BRepTools.Read_s(shape,str(path),BRep_Builder())
        return shape
    reader=STEPControl_Reader()
    assert reader.ReadFile(str(path)) == IFSelect_RetDone
    reader.TransferRoots()
    return reader.OneShape()


def without_zero_volume_debris(shape):
    from OCP.BRep import BRep_Builder
    from OCP.TopoDS import TopoDS_Compound
    from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeSolid
    from OCP.BRepGProp import BRepGProp
    from OCP.GProp import GProp_GProps
    from OCP.TopTools import TopTools_IndexedMapOfShape
    from OCP.TopExp import TopExp
    builder=BRep_Builder();out=TopoDS_Compound();builder.MakeCompound(out)
    contained=TopTools_IndexedMapOfShape();removed=[]
    for s in shapes(shape,TopAbs_SOLID):
        TopExp.MapShapes_s(s,TopAbs_SHELL,contained)
        props=GProp_GProps();BRepGProp.VolumeProperties_s(s,props)
        if abs(props.Mass())<=1e-12:removed.append(len(shapes(s,TopAbs_FACE)))
        else:builder.Add(out,s)
    for shell in shapes(shape,TopAbs_SHELL):
        if contained.Contains(shell):continue
        if BRep_Tool.IsClosed_s(shell):
            props=GProp_GProps();BRepGProp.VolumeProperties_s(BRepBuilderAPI_MakeSolid(TopoDS.Shell_s(shell)).Solid(),props)
            if abs(props.Mass())<=1e-12:
                removed.append(len(shapes(shell,TopAbs_FACE)));continue
        builder.Add(out,shell)
    assert len(removed)==7 and sum(removed)==24
    return out,removed


def properties(shape):
    points=np.array([list(BRep_Tool.Pnt_s(TopoDS.Vertex_s(v)).Coord()) for v in shapes(shape,TopAbs_VERTEX)])
    planes=[]
    other=0
    for f in shapes(shape,TopAbs_FACE):
        surface=BRepAdaptor_Surface(TopoDS.Face_s(f))
        if surface.GetType()!=GeomAbs_Plane:
            other+=1
            continue
        plane=surface.Plane()
        n=np.array(plane.Axis().Direction().Coord())
        if n[np.argmax(np.abs(n))]<0: n=-n
        offset=np.dot(n,np.array(plane.Location().Coord()))
        planes.append([*n,offset])
    return points,np.array(planes),other


def main():
    before_path,after_path,out_path=map(Path,sys.argv[1:4])
    before,after=read(before_path),read(after_path)
    if '--cache-after' in sys.argv:
        from OCP.BRepTools import BRepTools
        cache=out_path.parent/'reimported_final.brep'
        assert BRepTools.Write_s(after,str(cache))
        cache.with_suffix('.json').write_text(json.dumps({'step_sha256':hashlib.file_digest(open(after_path,'rb'),'sha256').hexdigest(),'brep_sha256':hashlib.file_digest(open(cache,'rb'),'sha256').hexdigest()}))
    excluded=[]
    if '--exclude-zero-debris' in sys.argv:
        before,excluded=without_zero_volume_debris(before)
    print('CAD files loaded',flush=True)
    bp,bplanes,bother=properties(before)
    ap,aplanes,aother=properties(after)
    print('Vertex and surface data collected',flush=True)
    forward=cKDTree(ap).query(bp)[0]
    reverse=cKDTree(bp).query(ap)[0]
    # Compare plane normals plus offsets as coefficients, not a surface distance.
    plane_forward=cKDTree(aplanes).query(bplanes)[0]
    plane_reverse=cKDTree(bplanes).query(aplanes)[0]
    out={
        'before':str(before_path),'after':str(after_path),
        'excluded_zero_volume_fragment_face_counts':excluded,
        'before_sha256':hashlib.file_digest(open(before_path,'rb'),'sha256').hexdigest(),
        'after_sha256':hashlib.file_digest(open(after_path,'rb'),'sha256').hexdigest(),
        'before_bbox_mm':bounds(before),'after_bbox_mm':bounds(after),
        'bbox_max_difference_mm':float(np.max(np.abs(np.array(bounds(before))-bounds(after)))),
        'before_vertices':len(bp),'after_vertices':len(ap),
        'before_faces':len(bplanes)+bother,'after_faces':len(aplanes)+aother,
        'before_nonplanar_faces':bother,'after_nonplanar_faces':aother,
        'before_solids':len(shapes(before,TopAbs_SOLID)),'after_solids':len(shapes(after,TopAbs_SOLID)),
        'max_original_vertex_to_nearest_result_vertex_mm':float(forward.max()),
        'max_result_vertex_to_nearest_original_vertex_mm':float(reverse.max()),
        'original_vertices_over_0_001mm':int((forward>0.001).sum()),
        'original_vertices_over_0_006mm':int((forward>0.006).sum()),
        'max_plane_coefficient_nearest_difference':float(max(plane_forward.max(),plane_reverse.max())),
        'max_existing_plane_coefficient_to_result':float(plane_forward.max()),
        'existing_planes_over_1e_8_coefficient_difference':int((plane_forward>1e-8).sum()),
        'limitations':'Nearest-vertex distances and plane coefficients are not a continuous Hausdorff surface-distance proof. Bbox excludes model tolerance padding.',
    }
    out_path.write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps(out),flush=True)


if __name__=='__main__': main()
