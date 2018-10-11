#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import stl 
from scipy.spatial import ConvexHull

import CustomPyMesh as cpm 
import CustomStl as cstl 


pmin = np.array([0,0,0])
pmax = np.array([1,3,1])
roofHeight = 1

house_vertices = cstl.house(pmin, pmax, roofHeight)

#from scipy gives back ConvecHull as nx3 array where each column represents a vertex
simplices = ConvexHull(vertices).simplices

house_stl = stl.mesh.Mesh(np.zeros(simplices.shape[0], dtype=stl.mesh.Mesh.dtype))
for i, f in enumerate(simplices):
    for j in range(3):
        house_stl.vectors[i][j] = house_vertices[f[j],:]

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

swire = cpm.ReturnScaffoldWire(pmin,pmax)
scaffold_mesh = cpm.InfalteWire(swire)

container_mesh = cpm.ReturnContainer(pmin,pmax,0.1)


print('done')
