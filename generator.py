#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import stl as mymesh
import mypymesh as mpm
import mystl 
from scipy.spatial import ConvexHull


def PyMesh2Stl(target):
    stlmesh = mymesh.Mesh(np.zeros(target.faces.shape[0], dtype=mymesh.Mesh.dtype))
    for i, f in enumerate(target.faces):
        for j in range(3):
            stlmesh.vectors[i][j] = target.vertices[f[j],:]
    return stlmesh


pmin = np.array([0,0,0])
pmax = np.array([1,3,1])
roofHeight = 1

vertices = mystl.house(pmin, pmax, roofHeight)

#from scipy gives back ConvecHull as nx3 array where each column represents a vertex
simplices = ConvexHull(vertices).simplices

cube = mymesh.Mesh(np.zeros(simplices.shape[0], dtype=mymesh.Mesh.dtype))
for i, f in enumerate(simplices):
    for j in range(3):
        cube.vectors[i][j] = vertices[f[j],:]

# Write the mesh to file "cube.stl"
#cube.save('cube.stl')

xmax = 1
ymax = 5
zmax = 1

xmin = 0 
ymin = 0
zmin = 0 

h = 0.3 

pmax = np.array([xmax,ymax,zmax])
pmin = np.array([xmin,ymin,zmin])

swire = mpm.ReturnScaffoldWire(pmin,pmax)

scaffold_mesh = mpm.InfalteWire(swire)

container_mesh = ReturnContainer(pmin,pmax,0.1)


print('done')
