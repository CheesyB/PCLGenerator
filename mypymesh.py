#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ipdb
import numpy as np
import pymesh as pm


def ReturnHouse(pmin,pmax,roofheight):
    #roofheight 
    z = pmax[2] + pmax[2]*roofheight
    
    #wire mesh
    p0 = pmin + np.array([pmax[0]/2,0,0])
    p1 = pmin + np.array([pmax[0]/2,pmax[1],0])
    p2 = p0 + np.array([0,0,z])
    p3 = p1 + np.array([0,0,z])

    #ipdb.set_trace()
    # Wire mesh
    vertices = np.vstack((p0,p1,p2,p3))
    edges = np.array([[0,1],
                    [1,3],
                    [3,2],
                    [2,0]]) # scheiß Nummerierung 
    wire  = pm.wires.WireNetwork.create_from_data(vertices, edges)
    inflator = pm.wires.Inflator(wire)
    inflator.inflate(0.1, per_vertex_thickness=True)
    wiremesh = inflator.mesh

    #big box, where the inflated wiremesh sits in
    boxmesh = pm.generate_box_mesh(pmin,pmax)
    
    #gluing the two meshes together. Works with cgal, not with default engine
    union_mesh = pm.boolean(boxmesh, wiremesh, operation="union",engine="cgal")

    # Magic happens here:) 
    mesh = pm.convex_hull(union_mesh)
    
    return mesh


def ReturnContainer(pmin,pmax,thickness):
    #Big box minus smaller box inside equals simple container
    boxmesh = pm.generate_box_mesh(pmin,pmax)

    newMin = pmin + np.array([thickness,thickness,thickness])
    newMax = pmax - np.array([thickness,thickness,0])
    
    inner_boxmesh= pm.generate_box_mesh(newMin,newMax)

    union_mesh = pm.boolean(boxmesh, inner_boxmesh,'symmetric_difference',engine="cgal")
    
    return union_mesh

def ReturnScaffoldWire(pmin, pmax):

    p0 = pmin 
    p1 = pmin + np.array([0,0,pmax[2]])
    p2 = pmin + np.array([pmax[0],0,pmax[2]])
    p3 = pmin + np.array([pmax[0],0,0])
   
    y = np.array([0,pmax[1],0])
    p4 = p0 + y
    p5 = p1 + y
    p6 = p2 + y 
    p7 = p3 + y 

    vertices = np.vstack((p0,p1,p2,p3,p4,p5,p6,p7))
    edges = np.array([[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4], 
                        [0,2],[1,3],[4,6],[5,7],
                        [0,4],[1,5],[2,6],[3,7],
                        [0,5],[2,7]])

    wire  = pm.wires.WireNetwork.create_from_data(vertices, edges)
    
    return wire



def InfalteWire(wire,thickness=0.02):
    
    inflator = pm.wires.Inflator(wire)
    inflator.inflate(thickness, per_vertex_thickness=False)
    scaffold = inflator.mesh

    return scaffold

    

def AddScaffoldToHouse(house):
    
     
    reps = [1,5,3] 
    scwidth = 0.3 
    gap = 0.5 
    fx = 0.3 
    fy = 1.0 
    fz = 0.8 

    vmin = house.bbox[0]
    vmax = house.bbox[1]
    
    maxx = vmax[0] * fx 
    maxy = vmax[1] * fy
    maxz = vmax[2] * fz
     
    p0 = vmin 
    p1 = vmin + np.array([0.0,0.0,maxz])
    p2 = vmin + np.array([0.0,maxy,maxz])
    p3 = vmin + np.array([0.0,maxy,0.0])
    #np1 = p1-p0
    #np2 = p3-p0
    #normal = np.cross(np1,np2)/np.linalg.norm(np.cross(np1,np2))
    
    normal = np.array([-1,0,0])
    
    pminnew = p0 + gap*normal + scwidth*normal
    
    # d distance to the edge, gap*nomal gap between sc. and house
    # scwidth*normal width of the scaffold
    pmaxnew = p2 + gap*normal
    
   
    scaffoldWire = ReturnScaffoldWire([0,0,0],[1,1,1])
    print(str(pminnew) + ' ' + str(pmaxnew))
    
    tiler = pm.Tiler(scaffoldWire)
    tiler.tile_with_guide_bbox([-10,-10,-10] ,[-5,-5,-5],reps)
    tiled_wires = tiler.wire_network
    inflator = pm.wires.Inflator(tiled_wires)
    inflator.inflate(0.02, per_vertex_thickness=False)
    scaffoldMesh = inflator.mesh

    ipdb.set_trace()
    
    union_mesh = pm.merge_meshes([house,scaffoldMesh]) 
    return union_mesh


if(__name__=='__main__'):
    xmax = 1
    ymax = 5
    zmax = 1

    xmin = 0 
    ymin = 0
    zmin = 0 

    h = 0.3 
    
    pmax = np.array([xmax,ymax,zmax])
    pmin = np.array([xmin,ymin,zmin])

#    swire = ReturnScaffoldWire(pmin,pmax)
#    mesh = InfalteWire(swire)

    house = ReturnHouse(pmin,pmax,h) 
    mesh = AddScaffoldToHouse(house)

#    mesh = ReturnContainer(pmin,pmax,0.1)
#    mesh = ReturnScaffold(pmin, pmax)
    pm.save_mesh('thing.ply',mesh)






