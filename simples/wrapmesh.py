#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
import trimesh as tri
import pandas as pa
import numpy as np
import matplotlib.pyplot as plt
import pyntcloud as pc
from .tictoc import TicToc

class WrapMesh(object): 
    """ WrapMesh holds one Trimesh Object with additional 
        information and methods """
    
    

    def __init__(self,mesh,classname,classnum,numpoints=5000):
        """TODO: to be defined1.

        :mesh: Trimesh 
        :clasname: string 
        :classnum: int
        """
        self.prefix = 'reg_'
        self._mesh = mesh 
        self._class_name = classname
        self.class_num = classnum  
        self.num_points = numpoints 
        self.logger = logging.getLogger('generator.simples.utils.WrapMesh')
        if isinstance(self._mesh,list):
            self._mesh = [self._mesh]
    
    
    def __str__(self):
        return self._class_name


    @property
    def name(self):
        return self.prefix + self._class_name



    @property 
    def pointcloud(self):
        T = TicToc(self.logger,' sample pointcloud as np.array from {}'.format(self.name))
        npPoints,_ = tri.sample.sample_surface_even(self._mesh,self.num_points)
        T.toc()
        return npPoints 
    

    
    @property
    def pointcloud_class(self):
        T = TicToc(self.logger,' sample pointcloud as np.array ' +
               'with class {} from {}'.format(self.class_num,self.name))
        if(self.class_num is None):
            self.logger.warning(' No one set the class for {}! Doing nothing'.format(self.name))
            return None 
        npPoints,_ = tri.sample.sample_surface_even(self._mesh,self.num_points)
        npClass = np.ones((npPoints.shape[0],1))*self.class_num
        npPoints = np.concatenate((npPoints,npClass), axis=1) 
        T.toc()
        return npPoints




    @property 
    def pyntcloud(self):
        T = TicToc(self.logger,' sample pyntcloud from {}'.format(self.name))
        points = self.pointcloud 
        dataframe = pa.DataFrame(columns=['x','y','z'],data=points)
        pyntcloud = pc.PyntCloud(dataframe)
        T.toc()
        return pyntcloud   

    
    @property 
    def pyntcloud_class(self):
        T = TicToc(self.logger,' sample pyntcloud with class from {}'.format(self.name))
        points = self.pointcloud_class
        dataframe = pa.DataFrame(columns=['x','y','z','class'],data=points)
        pyntcloud = pc.PyntCloud(dataframe)
        T.toc()
        return pyntcloud   
    

    def save_mesh(self):
        with open('data/mesh_{}.ply'.format(self.name),'wb') as f:
            byts = tri.io.ply.export_ply(self._mesh) 
            f.write(byts)

    

    
    def transform(self,matrices):
        try:
            it = iter(matrices)
        except:
            self.logger.warning('{} is not iterable,'\
                    ' no transformation applied!'.format(type(matrices)))
            return 
        for T in it:
            center = self._mesh.center_mass
            self._mesh.vertices -= center
            center = np.append(center,1)
            self._mesh.apply_transform(T) 
            center = T.dot(center.T)
            self._mesh.vertices += center[:3]
    


    
     

