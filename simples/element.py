#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import trimesh as tri
import pandas as pa
import numpy as np
import pyntcloud as pc
import trimesh.transformations as trans
from .wrapmesh import WrapMesh 
from .tictoc import TicToc

class Element(object):

    """Docstring for Element. """

    def __init__(self,wmeshes,name):
        """TODO: to be defined1.

        :wmeshes: TODO

        """
        self.wmeshes = wmeshes
        self.name = name
        self.logger = logging.getLogger('generator.simples.element')
        if isinstance(self.wmeshes,WrapMesh):
            self.wmeshes = [self.wmeshes]
    
    
    @property
    def trimeshes(self):
        return [wmesh._mesh for wmesh in self.wmeshes]

    @property
    def pointcloud(self):
        return np.vstack([wmesh.pointcloud for wmesh in self.wmeshes])
    
    @property 
    def pointcloud_class(self):
        return np.vstack([wmesh.pointcloud_class for wmesh in self.wmeshes])
    
    @property
    def entire_mesh(self):
        return tri.util.concatenate(self.trimeshes)
    
    
    @property
    def ground_truth(self):
        tol  = 0.1
        vert = np.array(self.entire_mesh.bounding_box.vertices)
        vert_cleaned = np.delete(vert,(0,2,4,6),0)
	
        xmin = min(vert_cleaned[0,:])
        ymin = min(vert_cleaned[1,:])
        xmax = max(vert_cleaned[0,:])
        ymax = max(vert_cleaned[1,:])
        width = xmax - xmin
        height  = ymax - ymin 
        return (xmin,ymin),(width,height) 


    def transform(self,transl,scale,alpha):
        zaxis = [0,0,1] 
        R = trans.rotation_matrix(alpha,zaxis)
        S = np.diag(scale)
        T = trans.translation_matrix(transl)
        
        #Z = shear_matrix(beta, xaxis, origin, zaxis)
        for wmesh in self.wmeshes:
            wmesh.transform([R,S,T])

    #translate last 
    def translate(self,translation=None):
        if translation is None:
            translation = [np.random.uniform(-1,1),np.random.uniform(-1,1),0] 
        for wmesh in self.wmeshes:
            wmesh._mesh.vertices += translation
   
    #rotate second 
    def rotate(self,alpha=None):
        if alpha is None:
            alpha = np.random.uniform(0,360)
        zaxis = [0,0,1] 
        R = trans.rotation_matrix(alpha,zaxis)
        for wmesh in self.wmeshes:
            wmesh.transform([R])

    # scale first 
    def scale(self,scale=None):
        if scale is None:
            scale = [np.random.normal(1,0.2),
                     np.random.normal(1,0.2),
                     np.random.normal(1,0.1),1] 
        S = np.diag(scale)
        for wmesh in self.wmeshes:
            wmesh.transform([S])
    
    
    
    def get_bboxo(self):
        total_mesh = self.entire_mesh 
        bboxo = total_mesh.bounding_box_oriented
        return bboxo
    
    def add_element(self,other_element):
        self.wmeshes.extend(other_element.wmeshes)
        self.logger.info(' added element ' +
                        '{} to {}'.format(other_element.name, self.name))

