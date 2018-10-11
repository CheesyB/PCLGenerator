#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from stl import mesh
from scipy.spatial import ConvexHull
import pyntcloud as pynt
import pandas as pa


def bbox(pmin,pmax):
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
    
    return  np.vstack((p0,p1,p2,p3,p4,p5,p6,p7))

def house(pmin, pmax,roofHeight):
    box = bbox(pmin,pmax)
    
    width = pmax[0]-pmin[0]
    length = pmax[1]-pmin[0]
    height = pmax[2]-pmin[2]
    
    p8 = pmin + np.array([width/2,0,height+roofHeight])
    p9 = pmin + np.array([width/2,length,height+roofHeight])

    return np.vstack((box,p8,p9))
    



if __name__ == "__main__":
    
    pmin = np.array([0,0,0])
    pmax = np.array([1,3,1])
    roofHeight = 1
    
    vertices = house(pmin, pmax, roofHeight)

    #from scipy gives back ConvecHull as nx3 array where each column represents a vertex
    simplices = ConvexHull(vertices).simplices

    cube = mesh.Mesh(np.zeros(simplices.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(simplices):
        for j in range(3):
            cube.vectors[i][j] = vertices[f[j],:]

    # Write the mesh to file "cube.stl"
    cube.save('cube.stl')



