"""Rebuild broad upper-shell regions with B-splines, retaining detailed rims.

SOURCE OF TRUTH: TEXT-TO-CAD. Trial only until independent STEP QA passes.
"""
import json,time
from pathlib import Path
import numpy as np
import trimesh
from official_upper_surface_fit_probe import OUT,fit,basis
from official_solid_full_diagnose import shapes,bounds
from OCP.gp import gp_Pnt,gp_Pnt2d
from OCP.Geom import Geom_BSplineSurface
from OCP.Geom2d import Geom2d_BezierCurve
from OCP.TColgp import TColgp_Array2OfPnt,TColgp_Array1OfPnt2d
from OCP.TColStd import TColStd_Array1OfReal,TColStd_Array1OfInteger
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge,BRepBuilderAPI_MakeWire,BRepBuilderAPI_MakeFace,BRepBuilderAPI_MakePolygon,BRepBuilderAPI_Sewing,BRepBuilderAPI_MakeSolid
from OCP.BRepFill import BRepFill_Filling
from OCP.BRepLib import BRepLib
from OCP.BRepTools import BRepTools
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRep import BRep_Tool
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.BRepLProp import BRepLProp_SLProps
from OCP.GeomAbs import GeomAbs_C0
from OCP.TopAbs import TopAbs_SHELL,TopAbs_FACE,TopAbs_REVERSED
from OCP.TopoDS import TopoDS
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps

def parameter(points):return np.degrees(np.arctan2(points[:,:2]-[0,5],points[:,2,None]+5))

def bspline(tx,ty,c):
    poles=TColgp_Array2OfPnt(1,len(tx)-4,1,len(ty)-4)
    c=c.reshape(len(tx)-4,len(ty)-4,3)
    for i in range(c.shape[0]):
        for j in range(c.shape[1]):poles.SetValue(i+1,j+1,gp_Pnt(*c[i,j]))
    def knotarrays(t):
        k,m=np.unique(t,return_counts=True);ka=TColStd_Array1OfReal(1,len(k));ma=TColStd_Array1OfInteger(1,len(k))
        for i,(a,b) in enumerate(zip(k,m),1):ka.SetValue(i,float(a));ma.SetValue(i,int(b))
        return ka,ma
    uk,um=knotarrays(tx);vk,vm=knotarrays(ty)
    return Geom_BSplineSurface(poles,uk,vk,um,vm,3,3)

def border_loops(faces):
    edges=np.vstack([faces[:,[0,1]],faces[:,[1,2]],faces[:,[2,0]]]);keys=np.sort(edges,axis=1)
    _,inverse,count=np.unique(keys,axis=0,return_inverse=True,return_counts=True)
    border=edges[count[inverse]==1];nxt={int(a):int(b) for a,b in border}
    assert len(nxt)==len(border),'Branching region border'
    loops=[]
    while nxt:
        start=next(iter(nxt));loop=[start];p=nxt.pop(start)
        while p!=start:loop.append(p);p=nxt.pop(p)
        loops.append(loop)
    return loops

def main(output_dir=OUT, remove_logo=False):
    output_dir=Path(output_dir);output_dir.mkdir(parents=True,exist_ok=True)
    start=time.monotonic();d=np.load(OUT/'upper_reference_mesh.npz');m=trimesh.Trimesh(vertices=d['vertices'],faces=d['faces'],process=False)
    labels=np.load(OUT/'feature_labels_5.npy');adj=m.face_adjacency
    selected=np.isin(labels,[4,3])&(m.vertices[m.faces][:,:,1].min(axis=1)>-40)
    for _ in range(2):
        cut=selected[adj[:,0]]!=selected[adj[:,1]];selected[np.unique(adj[cut])]=False
    removed=np.zeros(len(m.faces),dtype=bool);logo_report=None
    if remove_logo:
        components=trimesh.graph.connected_components(adj[(~selected[adj]).all(axis=1)],nodes=np.where(~selected)[0])
        matches=[]
        for component in components:
            v=m.vertices[np.unique(m.faces[component])]
            if (v[:,0]>-6).all() and (v[:,0]<6).all() and (v[:,1]>43).all() and (v[:,1]<54).all():matches.append(component)
        assert len(matches)==1,'Expected exactly one isolated logo island'
        removed[matches[0]]=True
        island_loops=border_loops(m.faces[removed]);assert len(island_loops)==1
        logo_edge_keys={tuple(sorted(pair)) for loop in island_loops for pair in zip(loop,loop[1:]+loop[:1])}
        v=m.vertices[np.unique(m.faces[removed])]
        logo_report={'removed_original_triangles':int(removed.sum()),'bounds_mm':[v.min(axis=0).tolist(),v.max(axis=0).tolist()],'boundary_edges':len(logo_edge_keys),'method':'Remove isolated engraved-logo island and extend the SAME fitted outer B-spline through its inner trim loop. Fitting input and all other boundaries unchanged.'}
        np.save(output_dir/'removed_logo_triangle_ids.npy',np.where(removed)[0])
    cache={};points=m.vertices.copy();all_faces=[];reports=[]
    for region in [4,3]:
        ids=np.where(selected&(labels==region))[0];tris=m.faces[ids];vid=np.unique(tris)
        p=np.vstack([m.vertices[vid],m.triangles_center[ids]]);uv=parameter(p);cs=[]
        for axis in range(3):tx,ty,c,info=fit(np.column_stack([uv,p[:,axis]]),3);cs.append(c)
        c=np.array(cs).T;pred=basis(uv,tx,ty)@c;err=np.linalg.norm(pred-p,axis=1)
        surface=bspline(tx,ty,c);loops=border_loops(tris)
        uv_all=parameter(m.vertices)
        def area(loop):
            v=uv_all[loop];return .5*np.sum(v[:,0]*np.roll(v[:,1],-1)-v[:,1]*np.roll(v[:,0],-1))
        loops.sort(key=lambda x:abs(area(x)),reverse=True)
        if remove_logo and region==4:
            assert len(loops)==2
            hole_keys={tuple(sorted(pair)) for pair in zip(loops[1],loops[1][1:]+loops[1][:1])}
            assert hole_keys==logo_edge_keys,'Logo island must exactly share the removed trim boundary'
            loops=loops[:1]
        # Outer loop CCW, holes CW in the surface parameter domain.
        for i,loop in enumerate(loops):
            if (area(loop)>0)!=(i==0):loop.reverse()
        wires=[]
        for loop in loops:
            wire=BRepBuilderAPI_MakeWire()
            for a,b in zip(loop,loop[1:]+loop[:1]):
                key=tuple(sorted((a,b)));lo,hi=key
                if key not in cache:
                    cp=TColgp_Array1OfPnt2d(1,2);cp.SetValue(1,gp_Pnt2d(*uv_all[lo]));cp.SetValue(2,gp_Pnt2d(*uv_all[hi]))
                    curve=Geom2d_BezierCurve(cp);edge=BRepBuilderAPI_MakeEdge(curve,surface,0.,1.).Edge()
                    assert BRepLib.BuildCurve3d_s(edge,1e-7)
                    cache[key]=edge
                    for v in key:points[v]=surface.Value(*uv_all[v]).Coord()
                edge=cache[key] if a==lo else TopoDS.Edge_s(cache[key].Reversed());wire.Add(edge)
            assert wire.IsDone();wires.append(wire.Wire())
        face=BRepBuilderAPI_MakeFace(surface,wires[0],True)
        for wire in wires[1:]:face.Add(wire)
        assert face.IsDone();f=face.Face()
        if region==3:f.Reverse()
        all_faces.append(f)
        report={'region':region,'replaced_faces':len(ids),'border_loops':len(loops),'border_edges':sum(map(len,loops)),'control_points':info['control_points'],'fit_sample_max_mm':float(err.max()),'fit_sample_p99_mm':float(np.percentile(err,99)),'face_valid':BRepCheck_Analyzer(f).IsValid()};reports.append(report);print(json.dumps(report),flush=True)
        BRepTools.Write_s(f,str(output_dir/f'candidate_surface_{region}.brep'))
    assert max(r['fit_sample_max_mm'] for r in reports)<.03,reports
    curved=0;retained=np.where(~selected&~removed)[0]
    for j,index in enumerate(retained):
        tri=m.faces[index];pairs=list(zip(tri,np.roll(tri,-1)));is_curved=any(tuple(sorted(map(int,p))) in cache for p in pairs)
        if not is_curved:
            polygon=BRepBuilderAPI_MakePolygon()
            for v in tri:polygon.Add(gp_Pnt(*points[v]))
            polygon.Close();f=BRepBuilderAPI_MakeFace(polygon.Wire()).Face()
        else:
            filling=BRepFill_Filling(3,6,2,False,1e-7,1e-6,.01,.1,5,4)
            for a,b in pairs:
                a=int(a);b=int(b);key=tuple(sorted((a,b)))
                if key in cache:e=cache[key] if a==key[0] else TopoDS.Edge_s(cache[key].Reversed())
                else:e=BRepBuilderAPI_MakeEdge(gp_Pnt(*points[a]),gp_Pnt(*points[b])).Edge()
                filling.Add(e,GeomAbs_C0)
            filling.Build();assert filling.IsDone(),int(index);f=filling.Face();curved+=1
            u0,u1,v0,v1=BRepTools.UVBounds_s(f);prop=BRepLProp_SLProps(BRepAdaptor_Surface(f),.5*(u0+u1),.5*(v0+v1),1,1e-9)
            assert prop.IsNormalDefined();normal=np.array(prop.Normal().Coord())
            if f.Orientation()==TopAbs_REVERSED:normal=-normal
            if normal@m.face_normals[index]<0:f.Reverse()
        all_faces.append(f)
        if j%2000==0:print(json.dumps({'retained_faces_built':j,'total':len(retained),'transition_faces':curved}),flush=True)
    sew=BRepBuilderAPI_Sewing(3e-6)
    for f in all_faces:sew.Add(f)
    sew.Perform();result=sew.SewedShape();shells=shapes(result,TopAbs_SHELL)
    report={'status':'candidate','regions':reports,'retained_faces':len(retained),'transition_faces':curved,'free_edges':sew.NbFreeEdges(),'multiple_edges':sew.NbMultipleEdges(),'shell_count':len(shells),'vertex_move_max_mm':float(np.linalg.norm(points-m.vertices,axis=1).max()),'seconds':time.monotonic()-start}
    report['logo_removal']=logo_report
    BRepTools.Write_s(result,str(output_dir/'hybrid_sewn_candidate.brep'))
    (output_dir/'hybrid_build_report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
    assert len(shells)==1 and not sew.NbFreeEdges() and not sew.NbMultipleEdges(),report
    solid=BRepBuilderAPI_MakeSolid(TopoDS.Shell_s(shells[0])).Solid();g=GProp_GProps();BRepGProp.VolumeProperties_s(solid,g)
    if g.Mass()<0:solid.Reverse()
    report.update({'valid':BRepCheck_Analyzer(solid).IsValid(),'volume_mm3':abs(g.Mass()),'faces':len(shapes(solid,TopAbs_FACE)),'bounds_mm':bounds(solid)})
    BRepTools.Write_s(solid,str(output_dir/'upper_hybrid_candidate.brep'));(output_dir/'hybrid_build_report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
    assert report['valid'] and report['volume_mm3']>0
    return solid

if __name__=='__main__':main()
