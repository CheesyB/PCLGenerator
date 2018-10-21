#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
import trimesh as tri
import pandas as pa
import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
import pyntcloud as pc
import os, shutil
from datetime import timedelta
import ipdb


class TicToc():

    """Docstring for TicToc. """

    def __init__(self,logger=None,name=''):
        """TODO: to be defined1. """
        if logger is None:
            logger = logging.getLogger('generator.utils.TicToc')
        self.logger = logger
        self.name = name
        self.tic = time.time() 

        self.logger.debug('{} started'.format(self.name))

    def toc(self):
        tac = time.time() - self.tic
        tac = timedelta(seconds=tac)
        self.logger.debug('{} finished: {}'.format(self.name,str(tac)))

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

def DelFilesInFolder(path2folder):
    logger = logging.getLogger('generator.'+__name__+'.DelFilesInFolder')
    i = 0
    for the_file in os.listdir(path2folder):
        file_path = os.path.join(path2folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                i += 1
                logger.debug('{} deleted'.format(file_path))
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    logger.info('{} files deleted'.format(i))


if __name__ == "__main__":
    mesh = tri.creation.box()
    wmesh = WrapMesh('house',mesh,(55))
    wmesh.SavePCRGB()
    print('lol')



