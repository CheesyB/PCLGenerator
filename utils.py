#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
import trimesh as tri
import pandas as pa
import numpy as np
import matplotlib.pyplot as plt 
import pyntcloud as pc
import os, shutil
from datetime import timedelta

class WrapMesh(object):

    """Docstring for MyMesh. """

    def __init__(self,name,mesh,Class):
        """TODO: to be defined1.

        :Mesh: TODO
        :Class: TODO 
        """
        self._prefix = 'Regular_'
        self._name = name #Name
        self._mesh = mesh #Tirmesh
        self._Class = Class #ONLY ONE CLASS (int)
        self.logger = logging.getLogger('generator.'+__name__+'.WrapMesh')

    @property
    def name(self):
        return self._prefix + self._name

    def SaveMesh(self):
        with open('data/mesh{}.ply'.format(self.name),'wb') as f:
            byts = tri.io.ply.export_ply(self._mesh) 
            f.write(byts)
        

    def SavePC(self,pointcloud = None, num = 10000):
        self.logger.debug('SavePC')
        if(pointcloud is None): 
            pointcloud = self.SamplePointCloudClasses(num)
        pointcloud.to_file('data/pc{}.ply'.format(self.name))
        
    def SavePCRaw(self,pointcloud = None, num = 10000):
        self.logger.debug('SavePCRaw')
        if(pointcloud is None): 
            pointcloud = self.SamplePointCloudRaw(num)
        pointcloud.to_file('data/pcRaw{}.ply'.format(self.name))

    def SavePCRGB(self,pointcloud = None, num = 10000):
        self.logger.debug('SavePCRGB')
        if(pointcloud is None): 
            pointcloud = self.SamplePointCloudRGB(num)
        pointcloud.to_file('data/pcColor{}.ply'.format(self.name))
         
    
     
    def SamplePointCloudRGB(self,num=10000):
        T = TicToc(self.logger,'SampelPointsRGB from {}'.format(self.name))
        npPoints,_ = tri.sample.sample_surface_even(self._mesh,num)
        cmap = plt.get_cmap()
        self.logger.debug('Class: {}'.format(self._Class))
        npClass = np.array([cmap(self._Class*100) for _ in range(npPoints.shape[0])])
        npPoints = np.concatenate((npPoints,npClass), axis=1)
        paPoints = pa.DataFrame(columns=['x','y','z','R','G','B','alpha'],data=npPoints)
        pointcloud = pc.PyntCloud(paPoints)
        T.toc()
        return pointcloud 
    
    def SamplePointCloudRaw(self,num=10000):
        T = TicToc(self.logger,'SampelPointsRaw from {}'.format(self.name))
        npPoints,_ = tri.sample.sample_surface_even(num)
        pointcloud = pc.PyntCloud(paPoints)
        T.toc()
        return pointcloud   
    
    def SamplePointCloudClasses(self,num=10000):
        T = TicToc(self.logger,'SampelPointsClasses from {}'.format(self.name))
        npPoints,_ = tri.sample.sample_surface_even(self._mesh,num)
        npClass = np.ones((npPoints.shape[0],1))*self._Class 
        npPoints = np.concatenate((npPoints,npClass), axis=1) #Transpose to fit the dims
        paPoints = pa.DataFrame(columns=['x','y','z','class'],data=npPoints)
        pointcloud = pc.PyntCloud(paPoints)
        T.toc()
        return pointcloud 

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
    for the_file in os.listdir(path2folder):
        file_path = os.path.join(path2folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    mesh = tri.creation.box()
    wmesh = WrapMesh('house',mesh,(55))
    wmesh.SavePCRGB()
    print('lol')



