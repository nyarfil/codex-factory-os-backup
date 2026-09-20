"""Rebuild faceted faces through shared seam vertices; eliminate loose BRep tolerances."""
import json,time,sys
from pathlib import Path
import numpy as np
from official_solid_full_diagnose import shapes,bounds
from official_solid_compare_geometry import read
from official_solid_patch_loops import triangles,faces_from_triangles,patch_shell
from OCP.TopAbs import TopAbs_SHELL,TopAbs_FACE,TopAbs_EDGE,TopAbs_SOLID
from OCP.TopoDS import TopoDS
from OCP.BRep import BRep_Tool
from OCP.BRepTools import BRepTools,BRepTools_WireExplorer
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.BRepBuilderAPI import BRepBuilderAPI_Sewing,BRepBuilderAPI_MakeSolid
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepAlgoAPI import BRepAlgoAPI_Check
from OCP.BOPAlgo import BOPAlgo_CheckStatus
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps

OUT=Path('V:/mouse/outputs/ZA13_OFFICIAL_PRECISION_REPAIR_02')

def rebuild(shell):
    sew=BRepBuilderAPI_Sewing(1e-7);deviations=[];counts={};added=0;duplicate_points_removed=0
    for face_index,face_shape in enumerate(shapes(shell,TopAbs_FACE)):
        face=TopoDS.Face_s(face_shape);explore=BRepTools_WireExplorer(BRepTools.OuterWire_s(face),face);pts=[]
        while explore.More():
            pts.append(BRep_Tool.Pnt_s(explore.CurrentVertex()).Coord());explore.Next()
        clean=[]
        for p in pts:
            if clean and np.linalg.norm(np.array(p)-clean[-1])<1e-9:duplicate_points_removed+=1;continue
            clean.append(p)
        if len(clean)>1 and np.linalg.norm(np.array(clean[0])-clean[-1])<1e-9:clean.pop();duplicate_points_removed+=1
        pts=clean
        points=np.array(pts);counts[len(points)]=counts.get(len(points),0)+1
        assert len(points)>=3
        plane=BRepAdaptor_Surface(face).Plane()
        deviations.extend(plane.Distance(__import__('OCP.gp',fromlist=['gp_Pnt']).gp_Pnt(*p)) for p in pts)
        try:indices=triangles(points)
        except ValueError:
            (OUT/'failed_exact_face.json').write_text(json.dumps({'face_index':face_index,'points':pts,'singular_values':np.linalg.svd(points-points.mean(axis=0),compute_uv=False).tolist()},indent=2))
            raise
        for new_face in faces_from_triangles(points,indices):sew.Add(new_face);added+=1
    print(json.dumps({'stage':'faces rebuilt','counts':counts,'new_faces':added,'max_vertex_distance_to_old_face_plane_mm':max(deviations)}),flush=True)
    sew.Perform();shells=shapes(sew.SewedShape(),TopAbs_SHELL)
    report={'free_edges':sew.NbFreeEdges(),'multiple_edges':sew.NbMultipleEdges(),'deleted_faces':sew.NbDeletedFaces(),'shells':len(shells),'max_vertex_distance_to_old_face_plane_mm':max(deviations),'original_face_edge_counts':counts,'rebuilt_faces':added,'duplicate_points_removed':duplicate_points_removed}
    assert len(shells)==1 and sew.NbFreeEdges()==0 and sew.NbMultipleEdges()==0,report
    result=BRepBuilderAPI_MakeSolid(TopoDS.Shell_s(shells[0])).Solid()
    prop=GProp_GProps();BRepGProp.VolumeProperties_s(result,prop)
    if prop.Mass()<0:result.Reverse()
    report.update({'valid':BRepCheck_Analyzer(result).IsValid(),'volume_mm3':abs(prop.Mass()),'bounds_mm':bounds(result)})
    return result,report

def main():
    count=int(sys.argv[1]) if len(sys.argv)>1 else 66853
    shape=read(OUT/'sewing_trial_cache.brep')
    shell=next(s for s in shapes(shape,TopAbs_SHELL) if len(shapes(s,TopAbs_FACE))==count)
    if not BRep_Tool.IsClosed_s(shell):
        sew=BRepBuilderAPI_Sewing(.006);sew.Add(shell);sew.Perform()
        additions,info=patch_shell(count,[sew.FreeEdge(i) for i in range(1,sew.NbFreeEdges()+1)])
        for f in additions:sew.Add(f)
        sew.Perform();shell=shapes(sew.SewedShape(),TopAbs_SHELL)[0]
        assert BRep_Tool.IsClosed_s(shell)
    result,report=rebuild(shell)
    BRepTools.Write_s(result,str(OUT/f'exact_boundary_{count}.brep'))
    (OUT/f'exact_boundary_{count}.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report),flush=True)
    checker=BRepAlgoAPI_Check();checker.SetData(result,True,True);checker.SetRunParallel(True);checker.Perform()
    report['self_intersections']=sum(r.GetCheckStatus()==BOPAlgo_CheckStatus.BOPAlgo_SelfIntersect for r in checker.Result())
    (OUT/f'exact_boundary_{count}.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)

if __name__=='__main__':main()
