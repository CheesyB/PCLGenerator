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



class WrapMesh(object):

    """ WrapMesh holds one Trimesh Object with additional 
        information and methods """

    def __init__(self,mesh,className,classNum,color=None,numpoints=5000):
        """TODO: to be defined1.

        :Mesh: TODO
        :Class: TODO 
        :classNum: int
        :color: (R,G,B)
        """
        self.prefix = 'reg_'
        self._mesh = mesh #Tirmesh
        self._class_name = className
        self._class_num = classNum #ONLY ONE CLASS (int)
        self._color = color
        if self._color is None:
           self._color = (0.5,0.5,0.5) 
        self.num_points = numpoints 
        self.logger = logging.getLogger('generator.'+__name__+'.WrapMesh')
    
    @property
    def name(self):
        return self.prefix + self._class_name

    # expects an list of matrices 

    @property 
    def pointcloud(self):
        T = TicToc(self.logger,' sample pointcloud as np.array from {}'.format(self.name))
        npPoints,_ = tri.sample.sample_surface_even(num)
        T.toc()
        return npPoints 
    
    @property 
    def pointcloud_color(self):
        T = TicToc(self.logger,' sample pointcloud as np.array \
                with color {} from {}'.format(self._color,self.name))
        npPoints,_ = tri.sample.sample_surface_even(num)
        self.logger.debug(' Save Class: {} to Color: {}'.format(self._class_num,color))

        npPoints,_ = tri.sample.sample_surface_even(self._mesh,self._class_num)
        npClass = np.array([self._color for _ in range(npPoints.shape[0])])
        npPoints = np.concatenate((npPoints,npClass), axis=1)
        T.toc()
        return npPoints 
    
    @property
    def pointcloud_class(self):
        T = TicToc(self.logger,'sample pointcloud as np.array \
                with class {} from {}'.format(self._classNum,self.name))
        npPoints,_ = tri.sample.sample_surface_even(num)
        npClass = np.ones((npPoints.shape[0],1))*self._ClassNum
        npPoints = np.concatenate((npPoints,npClass), axis=1) 
        T.toc()
        return npPoints

    @property 
    def pyntcloud(self):
        T = TicToc(self.logger,'sample pyntcloud from {}'.format(self.name))
        points = self.pointcloud 
        dataframe = pa.DataFrame(columns=['x','y','z'],data=points)
        pyntcloud = pc.PyntCloud(dataframe)
        T.toc()
        return pyntcloud   

    @property 
    def pyntcloud_color(self):
        T = TicToc(self.logger,'sample pyntcloud with color from {}'.format(self.name))
        points = self.pointcloud_color
        datafram = pa.DataFrame(columns=['x','y','z','red','green','blue'],data=points)
        pyntcloud = pc.PyntCloud(dataframe)
        T.toc()
        return pyntcloud   
    
    @property 
    def pyntcloud_class(self):
        T = TicToc(self.logger,'sample pyntcloud with class from {}'.format(self.name))
        points = self.pointcloud_color
        datafram = pa.DataFrame(columns=['x','y','z','class'],data=points)
        pyntcloud = pc.PyntCloud(dataframe)
        T.toc()
        return pyntcloud   
    
    def save_pc(self,mode='color'):
        dic =  {'raw':self.pyntcloud,
                'class':self.pyntcloud_class,
                'color':self.pyntcloud_color,
                None:self.pyntcloud}
        self.logger.debug(' save pointcloud {}'.format(dic[mode]))
        pyntcloud = dic[mode]
        pyntcloud.to_file('data/pc_{}_{}.ply'.format(mode,self.name))

    
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
    
    def save_mesh(self):
        with open('data/mesh_{}.ply'.format(self.name),'wb') as f:
            byts = tri.io.ply.export_ply(self._mesh) 
            f.write(byts)


         
if __name__ == "__main__":
   #write tests 
        
        
    
    
         
    
     

