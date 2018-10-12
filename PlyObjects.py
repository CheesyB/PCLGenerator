#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pymesh as pm
import trimesh as tri
import pyntcloud as pc
import pandas as pa
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


def ReturnBasement(pmax,pmin):
    return

def SamplePointCloud(mesh,num):
    T = TicToc('SampelPoints')
    npPoints,_ = tri.sample.sample_surface_even(mesh, num)
    paPoints = pa.DataFrame(columns=['x','y','z'],data=npPoints)
    pointcloud = pc.PyntCloud(paPoints)
    T.toc()
    return pointcloud 


def PMReturnContainer(pmin,pmax,thickness):
    T=TicToc('PMReturnContainer')
    #Big box minus smaller box inside equals simple container
    boxmesh = pm.generate_box_mesh(pmin,pmax)

    newMin = pmin + np.array([thickness,thickness,thickness])
    newMax = pmax - np.array([thickness,thickness,0])
    
    inner_boxmesh= pm.generate_box_mesh(newMin,newMax)

    union_mesh = pm.boolean(boxmesh, inner_boxmesh,'symmetric_difference',engine="cgal")
    union_mesh = PyMesh2Ply(union_mesh)
    union_mesh.vertices -= union_mesh.center_mass
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

    scaffold = PyMesh2Ply(scaffold)
    scaffold.vertices -= scaffold.center_mass
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

def PLYHouse(pmin, pmax,roofHeight):
    T = TicToc('STLHouse')
    
    vertices = STLBbox(pmin,pmax)
    
    width = pmax[0]-pmin[0]
    length = pmax[1]-pmin[0]
    height = pmax[2]-pmin[2]
    
    p8 = pmin + np.array([width/2,0,height+roofHeight])
    p9 = pmin + np.array([width/2,length,height+roofHeight])

    vertices = np.vstack((vertices,p8,p9))

    #from scipy gives back ConvecHull as nx3 array where each column represents a vertex
    tmpMesh = tri.Trimesh(vertices)
    hull = tmpMesh.convex_hull

    house = tri.Trimesh(hull.vertices.copy(),hull.faces.copy())
    house.vertices -= house.center_mass

    T.toc() 
    return house
    


def PyMesh2Ply(target):
    T = TicToc(' -->PyMesh2Ply')
    plymesh = tri.Trimesh(target.vertices.copy(),target.faces.copy()) 
    T.toc()
    return plymesh

def SavePly(name,mesh):
        with open('data/{}.ply'.format(name),'wb') as f:
            byts = tri.io.ply.export_ply(mesh) 
            f.write(byts)


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

    plyHouse = PLYHouse(pmin, pmax, roofHeight)
    plyHouse.vertices += np.array([3,0,0])
    houseCloud = SamplePointCloud(plyHouse,1000)
    houseCloud.to_file('data/pcHouse.ply') 
#    SavePly('plyHouse',plyHouse)

    
    plyScaffold = PMReturnScaffold(pmin,pmax)
    plyScaffold.vertices += np.array([-3,0,0])
    scaffoldCloud = SamplePointCloud(plyScaffold,1000)
    scaffoldCloud.to_file('data/pcScaffold.ply') 
#    SavePly('plyScaffold',plyScaffold)
    
    plyContainer = PMReturnContainer(pmin,pmax,thickness)
    plyContainer.vertices += np.array([0,5,0])
    containerCloud = SamplePointCloud(plyContainer,1000)
    containerCloud.to_file('data/pcContainer.ply') 
#    SavePly('plyContainer',plyContainer)
##
    totalMesh = tri.util.concatenate([plyHouse,plyScaffold,plyContainer])
    SavePly('plyTotal.ply',totalMesh)

    totalCloud = SamplePointCloud(totalMesh,1000000)
    totalCloud.to_file('data/pcTotal.ply')
    T.toc()






