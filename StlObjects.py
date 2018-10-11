#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import stl
from scipy.spatial import ConvexHull
import pymesh as pm

import logging
import time
from datetime import timedelta


class TicToc():

    """Docstring for TicToc. """

    def __init__(self,name):
        """TODO: to be defined1. """
        self.name = name
        self.tic = time.time() 
        logging.debug('{} started'.format(self.name))

    def toc(self):
        tac = time.time() - self.tic
        tac = timedelta(seconds=tac)
        logging.debug('{} finished: {}'.format(self.name,str(tac)))

        

def PMReturnHouse(pmin,pmax,roofheight):
    #roofheight 
    T=TicToc('PMReturnHouse') 
    
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
    mesh = PyMesh2Stl(mesh) 
    
    T.toc()
    return mesh


def PMReturnContainer(pmin,pmax,thickness):
    T=TicToc('PMReturnContainer')
    #Big box minus smaller box inside equals simple container
    boxmesh = pm.generate_box_mesh(pmin,pmax)

    newMin = pmin + np.array([thickness,thickness,thickness])
    newMax = pmax - np.array([thickness,thickness,0])
    
    inner_boxmesh= pm.generate_box_mesh(newMin,newMax)

    union_mesh = pm.boolean(boxmesh, inner_boxmesh,'symmetric_difference',engine="cgal")
    union_mesh = PyMesh2Stl(union_mesh)
    T.toc()
    return union_mesh

def PMReturnScaffold(pmin, pmax):
    T=TicToc('PMReturnScaffold')
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
    
    inflator = pm.wires.Inflator(wire)
    inflator.inflate(thickness, per_vertex_thickness=False)
    scaffold = inflator.mesh

    scaffold = PyMesh2Stl(scaffold)
    T.toc()
    return scaffold


def STLBbox(pmin,pmax):
    T=TicToc('STLBbox')
    #cube
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
    
    T.toc()
    
    return  np.vstack((p0,p1,p2,p3,p4,p5,p6,p7))

def STLHouse(pmin, pmax,roofHeight):
    T = TicToc('STLHouse')
    
    vertices = STLBbox(pmin,pmax)
    
    width = pmax[0]-pmin[0]
    length = pmax[1]-pmin[0]
    height = pmax[2]-pmin[2]
    
    p8 = pmin + np.array([width/2,0,height+roofHeight])
    p9 = pmin + np.array([width/2,length,height+roofHeight])

    vertices = np.vstack((vertices,p8,p9))

    #from scipy gives back ConvecHull as nx3 array where each column represents a vertex
    simplices = ConvexHull(vertices).simplices

    house = stl.mesh.Mesh(np.zeros(simplices.shape[0], dtype=stl.mesh.Mesh.dtype))
    for i, f in enumerate(simplices):
        for j in range(3):
            house.vectors[i][j] = vertices[f[j],:]
    
    T.toc() 
    return house
    


def PyMesh2Stl(target):
    T = TicToc(' -->PyMesh2Stl')
    stlmesh = stl.mesh.Mesh(np.zeros(target.faces.shape[0], dtype=stl.mesh.Mesh.dtype))
    for i, f in enumerate(target.faces):
        for j in range(3):
            stlmesh.vectors[i][j] = target.vertices[f[j],:]
    T.toc()
    return stlmesh



if __name__ == "__main__":
    print('Test started')
    logging.basicConfig(level=logging.DEBUG)
    T=TicToc('Total')
    xmax = 1
    ymax = 5
    zmax = 1

    xmin = 0 
    ymin = 0
    zmin = 0 

    roofHeight = 1 
    thickness = 0.1
    
    pmax = np.array([xmax,ymax,zmax])
    pmin = np.array([xmin,ymin,zmin])

    stlHouse = STLHouse(pmin, pmax, roofHeight)
    stlHouse.save('data/House.stl')

    stlHousePM = PMReturnHouse(pmin, pmax,roofHeight)
    stlHousePM.save('data/PMHouse.stl')
    
    stlScaffold = PMReturnScaffold(pmin,pmax)
    stlScaffold.save('data/Scaffold.stl')
    
    stlContainer = PMReturnContainer(pmin,pmax,thickness)
    stlContainer.save('data/Container.stl')

    T.toc()






