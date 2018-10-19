#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pymesh as pm
import trimesh as tri
import pyntcloud as pc
import utils
import pandas as pa
import logging





""" returns two CustoMeshes, Class => (1,2) """

def Basement(Class):
    logger = logging.getLogger('generator.'+__name__+'.Basement')
    T=utils.TicToc(logger)

    box = tri.creation.box()
    normal = np.array([0,0,1])
    origin = np.array([0,0,0])
    upper = tri.intersections.slice_mesh_plane(box,normal,origin)
    upperMesh = utils.WrapMesh('BasementUpper',upper,Class[0])
    lower = tri.intersections.slice_mesh_plane(box,-normal,origin)
    lowerMesh = utils.WrapMesh('BasementLower',lower,Class[1])
    
    return (upperMesh,lowerMesh)


    
""" return one utils.WrapMesh, Class => 1 """

def Container(thickness,Class):
    logger = logging.getLogger('generator.'+__name__+'.Container')
    T=utils.TicToc(logger)
    
    logger.debug('Obacht mit der thickness, kann zu gross sein')
    #Big box minus smaller box inside equals simple container
    pmin = np.array([0,0,0])
    pmax = np.array([1,1,1])
    boxmesh = pm.generate_box_mesh(pmin,pmax)

    newMin = pmin + np.array([thickness,thickness,thickness])
    newMax = pmax - np.array([thickness,thickness,0])
    
    inner_boxmesh= pm.generate_box_mesh(newMin,newMax)

    union_mesh = pm.boolean(boxmesh, inner_boxmesh,'symmetric_difference',engine="cgal")
    union_mesh = utils.PyMesh2Ply(union_mesh)
    mesh = utils.WrapMesh('Container',union_mesh,Class)
    T.toc()
    return mesh 
    


        

def Scaffold(thickness,Class):
    logger = logging.getLogger('generator.'+__name__+'.Scaffold')
    T=utils.TicToc(logger)
    
    p0 = np.array([0,0,0])
    p1 = np.array([1,0,0])
    p2 = np.array([1,1,0])
    p3 = np.array([0,1,0])
    p4 = np.array([0,0,1])
    p5 = np.array([1,0,1])
    p6 = np.array([1,1,1])
    p7 = np.array([0,1,1])
    
    vertices = np.vstack((p0,p1,p2,p3,p4,p5,p6,p7))
    edges = np.array([[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4], 
                        [0,2],[1,3],[4,6],[5,7],
                        [0,4],[1,5],[2,6],[3,7],
                        [0,5],[2,7]])
    
    wire  = pm.wires.WireNetwork.create_from_data(vertices, edges)
    
    inflator = pm.wires.Inflator(wire)
    inflator.inflate(thickness, per_vertex_thickness=False)
    scaffold = inflator.mesh

    scaffold = utils.PyMesh2Ply(scaffold)
    mesh = utils.WrapMesh('Scaffold',scaffold,Class)

    T.toc()
    return mesh 




""" needs two classes """

def House(roofHeight,Classes):
    logger = logging.getLogger('generator.'+__name__+'.House')
    T=utils.TicToc(logger)
    
    pmin = np.array([0,0,0])
    pmax = np.array([1,1,1])


    x = pmin[0]
    y = pmin[1]
    z = pmin[2]

    X = pmax[0]
    Y = pmax[1]
    Z = pmax[2]

    p0 = pmin
    p1 = np.array([X,y,z])
    p2 = np.array([X,Y,z])
    p3 = np.array([x,Y,z])
    p4 = np.array([x,y,Z])
    p5 = np.array([X,y,Z])
    p6 = pmax
    p7 = np.array([x,Y,Z])
    
    vertices = np.vstack((p0,p1,p2,p3,p4,p5,p6,p7)) 
    hull = tri.convex.convex_hull(vertices)

    body = tri.Trimesh(vertices=hull.vertices,faces=hull.faces)
    bodymesh = utils.WrapMesh('body', body,Classes[1])
    
    
    
    
    p8 = pmin + np.array([1/2,0,1+roofHeight])
    p9 = pmin + np.array([1/2,1,1+roofHeight])
    
    vertices = np.vstack((p4,p5,p6,p7,p8,p9))
    hull = tri.convex.convex_hull(vertices)
    
    roof = tri.Trimesh(vertices=hull.vertices,faces=hull.faces)
    roofmesh = utils.WrapMesh('roof',roof,Classes[0])
    meshlist = []
    meshlist.append(roofmesh)
    meshlist.append(bodymesh)
    T.toc() 
    return meshlist
   
   




if __name__ == "__main__":
    print('Test started')
    logging.basicConfig(level=logging.DEBUG)
    T=utils.TicToc(name='Total')

    roofHeight = 1 
    thickness = 0.1
    
    
    house = House(roofHeight,(1,2))
    house[0].SaveMesh()
    house[1].SaveMesh()
    house[0].SavePC()
    house[1].SavePC()

    scaffold = Scaffold(thickness,1)
    scaffold.SaveMesh()
    scaffold.SavePC()
    
    basement = Basement((1,2))
    basement[0].SaveMesh()
    basement[1].SaveMesh()
    basement[0].SavePC()
    basement[1].SavePC()
    

    container = Container(thickness,1)
    container.SaveMesh()
    container.SavePC()
    
    T.toc()






