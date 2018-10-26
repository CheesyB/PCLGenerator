#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import trimesh as tri
import pandas as pa
import pyntcloud as pc
from .tictoc import TicToc


def PyMesh2Ply(target):
    logger = logging.getLogger('generator.'+__name__+'.PyMesh2Ply')
    T=TicToc(logger)
    plymesh = tri.Trimesh(target.vertices.copy(),target.faces.copy()) 
    T.toc()
    return plymesh

def SavePly(name,mesh):
        with open('data/{}.ply'.format(name),'wb') as f:
            byts = tri.io.ply.export_ply(mesh) 
            f.write(byts)

def SamplePointCloud(mesh,num):
    logger = logging.getLogger('generator.'+__name__+'.SamplePointCloud')
    T=TicToc(logger)
    npPoints,_ = tri.sample.sample_surface_even(mesh, num)
    paPoints = pa.DataFrame(columns=['x','y','z'],data=npPoints)
    pointcloud = pc.PyntCloud(paPoints)
    T.toc()
    return pointcloud 





def test():
    print('Not Implemented')


if __name__ == "__main__":
    test()




