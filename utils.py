#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
import trimesh as tri
import pandas as pa
import pyntcloud as pc
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

def PyMesh2Ply(target):
    T = TicToc(' -->PyMesh2Ply')
    plymesh = tri.Trimesh(target.vertices.copy(),target.faces.copy()) 
    T.toc()
    return plymesh

def SavePly(name,mesh):
        with open('data/{}.ply'.format(name),'wb') as f:
            byts = tri.io.ply.export_ply(mesh) 
            f.write(byts)

def SamplePointCloud(mesh,num):
    T = TicToc('SampelPoints')
    npPoints,_ = tri.sample.sample_surface_even(mesh, num)
    paPoints = pa.DataFrame(columns=['x','y','z'],data=npPoints)
    pointcloud = pc.PyntCloud(paPoints)
    T.toc()
    return pointcloud 


if __name__ == "__main__":
    print('nothing to do here')
