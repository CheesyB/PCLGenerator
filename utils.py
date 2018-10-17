#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
import trimesh as tri
import pandas as pa
import numpy as np
import pyntcloud as pc
from datetime import timedelta

class WrapMesh(object):

    """Docstring for MyMesh. """

    def __init__(self,name,mesh,Class):
        """TODO: to be defined1.

        :Mesh: TODO
        :Class: TODO 
        """
        self._name = name
        self._mesh = mesh
        self._Class = Class

    def SaveMesh(self):
        with open('data/mesh{}.ply'.format(self._name),'wb') as f:
            byts = tri.io.ply.export_ply(self._mesh) 
            f.write(byts)
        

    def SavePC(self,pointcloud = None, num = 10000):
        if(pointcloud is None): 
            pointcloud = self.SamplePointCloud(num)
        pointcloud.to_file('data/pc{}.ply'.format(self._name))
        
    def SavePCRaw(self,pointcloud = None, num = 10000):
        if(pointcloud is None): 
            pointcloud = self.SamplePointCloudRaw(num)
        pointcloud.to_file('data/pcRaw{}.ply'.format(self._name))

    def SavePCColor(self,pointcloud = None, num = 10000):
        raise NotImplemented
       
    def SamplePointCloudRaw(self,num=10000):
        T = TicToc('SampelPoints from {}'.format(self._name))
        npPoints,_ = tri.sample.sample_surface_even(num)
        pointcloud = pc.PyntCloud(paPoints)
        T.toc()
        return pointcloud   
    
    def SamplePointCloud(self,num=10000):
        T = TicToc('SampelPoints from {}'.format(self._name))
        npPoints,_ = tri.sample.sample_surface_even(self._mesh,num)
        npClass = np.ones((npPoints.shape[0],1))*self._Class 
        npPoints = np.concatenate((npPoints,npClass), axis=1) #Transpose to fit the dims
        paPoints = pa.DataFrame(columns=['x','y','z','class'],data=npPoints)
        pointcloud = pc.PyntCloud(paPoints)
        T.toc()
        return pointcloud 

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
