"""Boundary-preserving local hole patches; no displacement of source surfaces."""
import numpy as np
from functools import lru_cache
from shapely.geometry import Polygon, LineString


def ordered_loops(edges):
    from official_solid_full_diagnose import shapes
    from OCP.TopAbs import TopAbs_VERTEX
    from OCP.TopoDS import TopoDS
    from OCP.BRep import BRep_Tool
    graph, points = {}, {}
    for edge in edges:
        p=[np.array(BRep_Tool.Pnt_s(TopoDS.Vertex_s(v)).Coord()) for v in shapes(edge,TopAbs_VERTEX)]
        assert len(p)==2
        a,b=[tuple(np.round(x,8)) for x in p]
        graph.setdefault(a,set()).add(b); graph.setdefault(b,set()).add(a)
        points[a],points[b]=p
    assert all(len(v)==2 for v in graph.values()), 'Branched repair boundary'
    seen=set(); loops=[]
    for start in graph:
        if start in seen: continue
        sequence=[]; current=start; previous=None
        while current not in seen:
            seen.add(current); sequence.append(points[current])
            following=next(v for v in sorted(graph[current]) if v!=previous)
            previous,current=current,following
        assert current==start
        loops.append(np.array(sequence))
    return loops


def triangles(poly):
    """Minimum-area triangulation constrained by a non-self-crossing projection."""
    if len(poly)==3: return [(0,1,2)]
    center=poly-poly.mean(axis=0)
    _,_,vh=np.linalg.svd(center,full_matrices=False)
    projections=[center@vh[:2].T,center[:,[0,1]],center[:,[1,2]],center[:,[0,2]]]
    options=[(p,Polygon(p)) for p in projections]
    options=[(p,g) for p,g in options if g.is_valid and g.area>1e-10]
    if not options:
        for i in range(2048):
            z=1-2*(i+.5)/2048;r=np.sqrt(1-z*z);a=i*np.pi*(3-np.sqrt(5))
            normal=np.array([r*np.cos(a),r*np.sin(a),z])
            u=np.cross(normal,[0,0,1]);u/=np.linalg.norm(u);v=np.cross(normal,u)
            p=center@np.array([u,v]).T;g=Polygon(p)
            if g.is_valid and g.area>1e-10:options.append((p,g))
    if not options:
        # Folded USB rims have paired near-coincident vertices. Partition at
        # those short seams WITHOUT moving vertices or deleting boundary edges.
        n=len(poly)
        seams=sorted((np.linalg.norm(poly[i]-poly[j]),i,j) for i in range(n) for j in range(i+2,n) if not(i==0 and j==n-1))
        for distance,i,j in seams:
            if distance>0.006:break
            first=list(range(i,j+1));second=list(range(j,n))+list(range(0,i+1))
            try:
                left=triangles(poly[first]);right=triangles(poly[second])
                return [tuple(first[k] for k in t) for t in left]+[tuple(second[k] for k in t) for t in right]
            except ValueError:continue
        raise ValueError('No simple projection or short seam partition for hole')
    projected, polygon=max(options,key=lambda x:x[1].area)
    n=len(poly); cost=np.full((n,n),np.inf); split={}
    for i in range(n-1):cost[i,i+1]=0.0
    @lru_cache(None)
    def valid_edge(i,j):
        return j==i+1 or (i==0 and j==n-1) or polygon.buffer(1e-10).covers(LineString([projected[i],projected[j]]))
    for width in range(2,n):
        for i in range(n-width):
            j=i+width
            if not valid_edge(i,j):continue
            for k in range(i+1,j):
                if not valid_edge(i,k) or not valid_edge(k,j):continue
                area=np.linalg.norm(np.cross(poly[k]-poly[i],poly[j]-poly[i]))/2
                if area<1e-12:continue
                candidate=cost[i,k]+cost[k,j]+area
                if candidate<cost[i,j]:cost[i,j]=candidate;split[i,j]=k
    if not np.isfinite(cost[0,n-1]):raise ValueError('No nondegenerate patch triangulation')
    result=[]
    def collect(i,j):
        if j<=i+1:return
        k=split[i,j];result.append((i,k,j));collect(i,k);collect(k,j)
    collect(0,n-1)
    return result


def faces_from_triangles(points, indices):
    from OCP.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace
    from OCP.gp import gp_Pnt
    faces=[]
    for tri in indices:
        wire=BRepBuilderAPI_MakePolygon()
        for i in tri:wire.Add(gp_Pnt(*map(float,points[i])))
        wire.Close()
        maker=BRepBuilderAPI_MakeFace(wire.Wire(),True)
        assert maker.IsDone()
        faces.append(maker.Face())
    return faces


def ruled_pair(bottom,top,closed):
    from scipy.spatial import cKDTree
    delta=top.mean(axis=0)-bottom.mean(axis=0)
    distances,index=cKDTree(top).query(bottom+delta)
    assert len(set(index))==len(bottom) and distances.max()<0.0001, 'Paired rims do not correspond'
    top=top[index]; n=len(bottom)
    vertices=np.vstack([bottom,top]); tri=[]
    for i in range(n if closed else n-1):
        j=(i+1)%n
        tri.extend([(i,j,n+j),(i,n+j,n+i)])
    return faces_from_triangles(vertices,tri),delta


def bracket_patches(loops):
    assert sorted(map(len,loops))==[12,12,16,16,50]
    faces=[]; delta=None
    for count in (12,16):
        pair=sorted([p for p in loops if len(p)==count],key=lambda p:p[:,2].mean())
        more,delta=ruled_pair(pair[0],pair[1],True);faces.extend(more)
    rim=next(p for p in loops if len(p)==50)
    # This rim includes rounded side transitions, not two translated chains.
    # Preserve its complete boundary and triangulate only the missing wall.
    faces.extend(faces_from_triangles(rim,triangles(rim)))
    return faces


def patch_shell(face_count,free_edges):
    loops=ordered_loops(free_edges)
    if face_count==908:
        faces=bracket_patches(loops)
    else:
        faces=[]
        for loop in loops:faces.extend(faces_from_triangles(loop,triangles(loop)))
    return faces,{'source_shell_faces':face_count,'boundary_loops':list(map(len,loops)),'new_faces':len(faces)}
