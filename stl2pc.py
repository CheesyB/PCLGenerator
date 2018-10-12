#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import  pyntcloud as pc
import trimesh

# This function eats a numpy-stl mesh object and return
# a pyntcloud obj.
#def stl2pc():



if __name__ == "__main__":
    print('lol')
        # Define the 8 vertices of the cube
    vertices = np.array([\
        [-1, -1, -1],
        [+1, -1, -1],
        [+1, +1, -1],
        [-1, +1, -1],
        [-1, -1, +1],
        [+1, -1, +1],
        [+1, +1, +1],
        [-1, +1, +1]])
    # Define the 12 triangles composing the cube
    faces = np.array([\
        [0,3,1],
        [1,3,2],
        [0,4,7],
        [0,7,3],
        [4,5,6],
        [4,6,7],
        [5,1,2],
        [5,2,6],
        [2,3,6],
        [3,7,6],
        [0,1,5],
        [0,5,4]])
    
    mesh = trimesh.Trimesh(vertices,faces)
    with open('data/trimesh.ply','wb'):
        f.write(trimesh.io.ply.export_ply(T))

    print('lol')

    
    
