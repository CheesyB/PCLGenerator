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


class ElementSaver(object):

    """Docstring for Saver. """

    def __init__(self,color_dict,data_path):
        """TODO: to be defined1.

        :color_dict: TODO
        :data_path: TODO

        """
        self._color_dict = color_dict
        self._data_path = data_path
        self.logger = logging.getLogger('generator.'+__name__+'.Saver')
        
    def save_as_mesh(self,element):
        pass

    
    
    def save_as_pc(self,element):
        for wmesh in element.wmeshes:
            color = self._color_dict[str(wmesh)] 
            T = TicToc(self.logger,' sample pointcloud as np.array \
                    with color {} from {}'.format(color,str(wmesh)))
            
            points = wmesh.pointcloud 
            class_points = np.array([color for _ in range(points.shape[0])])
            points = np.concatenate((points,class_points), axis=1)

            dataframe = pa.DataFrame(columns=['x','y','z','red','green','blue'],data=points)
            pyntcloud = pc.PyntCloud(dataframe)
            pyntcloud.to_file(self._data_path + '/pc_{}_{}.ply'.format(wmesh.name,element.name))
            self.logger.info('{} color pointcloud written'.format(wmesh.name))
            T.toc()
    
    
    def delete_files(self):
        i = 0
        for the_file in os.listdir(self._data_path):
            file_path = os.path.join(self._data_path, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    i += 1
                    self.logger.debug('{} deleted'.format(file_path))
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
        self.logger.info(' {} files deleted'.format(i))





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


def test():
    print('Not Implemented')


if __name__ == "__main__":
    test()




