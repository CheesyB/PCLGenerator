#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pymesh as pm
import trimesh as tri
import pyntcloud as pc
import utils
import WrapMesh as wm
import Element as ele
import pandas as pa
import logging






""" returns two CustoMeshes, Class => (1,2) """

def basement():
    logger = logging.getLogger('generator.'+__name__+'.Basement')
    T=utils.TicToc(logger)

    box = tri.creation.box()
    normal = np.array([0,0,1])
    origin = np.array([0,0,0])
    
    upper = tri.intersections.slice_mesh_plane(box,normal,origin)
    upperMesh = wm.WrapMesh(upper,'basement_up')
    
    lower = tri.intersections.slice_mesh_plane(box,-normal,origin)
    lowerMesh = wm.WrapMesh(lower,'basement_low')
    element = ele.Element([upperMesh,lowerMesh],'first_ele')
    return element 


    
""" return one WrapMesh, Class => 1 """

def container():
    thickness = 0.1
    logger = logging.getLogger('generator.'+__name__+'.Container')
    T=utils.TicToc(logger)
    
    #Big box minus smaller box inside equals simple container
    pmin = np.array([-0.5,-0.5,-0.5])
    pmax = np.array([0.5,0.5,0.5])
    boxmesh = pm.generate_box_mesh(pmin,pmax)

    newMin = pmin + np.array([thickness,thickness,thickness])
    newMax = pmax - np.array([thickness,thickness,0])
    
    inner_boxmesh= pm.generate_box_mesh(newMin,newMax)

    union_mesh = pm.boolean(boxmesh, inner_boxmesh,'symmetric_difference',engine="cgal")
    union_mesh = utils.PyMesh2Ply(union_mesh)
    mesh = wm.WrapMesh(union_mesh,'container')
    element = ele.Element([mesh],'container_ele') 
    T.toc()
    return element 
    


        

def scaffold():
    thickness = 0.1
    logger = logging.getLogger('generator.'+__name__+'.Scaffold')
    T=utils.TicToc(logger)
    
    p0 = np.array([-0.5,-0.5,0])
    p1 = np.array([0.5,-0.5,0])
    p2 = np.array([0.5,0.5,0])
    p3 = np.array([-0.5,0.5,0])
    
    p4 = np.array([-0.5,-0.5,1])
    p5 = np.array([0.5,-0.5,1])
    p6 = np.array([0.5,0.5,1])
    p7 = np.array([-0.5,0.5,1])
    
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
    mesh = wm.WrapMesh(scaffold,'scaffold')
    element = ele.Element([mesh],'scaffold_ele') 

    T.toc()
    return element 




""" needs two classes """

def house(roofHeight=None):
    if roofHeight is None:
        roofHeight = np.random.rand()
    logger = logging.getLogger('generator.'+__name__+'.House')
    T=utils.TicToc(logger)
    
    pmin = np.array([-0.5,-0.5,0])
    pmax = np.array([0.5,0.5,1])


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
    bodymesh = wm.WrapMesh(body,'body')
    
    
    
    
    p8 = pmin + np.array([1/2,0,1+roofHeight])
    p9 = pmin + np.array([1/2,1,1+roofHeight])
    
    vertices = np.vstack((p4,p5,p6,p7,p8,p9))
    hull = tri.convex.convex_hull(vertices)
    
    roof = tri.Trimesh(vertices=hull.vertices,faces=hull.faces)
    roofmesh = wm.WrapMesh(roof,'roof')
    
    meshes = list((roofmesh,bodymesh)) 
    element = ele.Element(meshes,'house_ele') 
    
    T.toc() 
    return element 
   
   




if __name__ == "__main__":
    test() 


def test():

    logging.basicConfig(level=logging.INFO)
    logging.getLogger('generator').setLevel(logging.INFO)
    logging.getLogger('trimesh').setLevel(logging.CRITICAL)    

    cdict = {'basement_up':(1,0,0),
            'basement_low':(0,1,0),
            'roof':(1,1,0),
            'body':(1,0,1),
            'container':(0,1,1),
            'scaffold':(0.5,1,0.5)}
    
    saver =  utils.ElementSaver(cdict, 'data')
    saver.delete_files()
    
    roofHeight = 1 
    thickness = 0.1
    
    
    myhouse = house(roofHeight)
    saver.save_as_pc(myhouse)
    

    myscaffold = scaffold()
    saver.save_as_pc(myscaffold)
    
    
    mybasement = basement()
    saver.save_as_pc(mybasement)
    

    mycontainer = container()
    saver.save_as_pc(mycontainer)
    






