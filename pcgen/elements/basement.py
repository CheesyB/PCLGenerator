#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pymesh as pm
import trimesh as tri
import trimesh.transformations as trans
from ..element import Element
from ..tictoc import TicToc
from ..wrapmesh import WrapMesh
from ..utils import PyMesh2Ply
import logging




class Basement(Element):

    """This is derived form the Element class"""

    def __init__(self,class_numbers):
        """TODO: to be defined1. """

        self.logger = logging.getLogger('generator.simples.elements.basement')
        T=TicToc(self.logger)

        box = tri.creation.box()
        normal = np.array([0,0,1])
        origin = np.array([0,0,0])
        
        upper = tri.intersections.slice_mesh_plane(box,normal,origin)
        upperMesh = WrapMesh(upper,'basement_up',class_numbers[0])
        upperMesh.prefix = 'reg_'
        
        lower = tri.intersections.slice_mesh_plane(box,-normal,origin)
        lowerMesh = WrapMesh(lower,'basement_low',class_numbers[1])
        lowerMesh.prefix = 'reg_'

        Element.__init__(self,[upperMesh,lowerMesh],'basement')


    def rand_translate(self):
        self.logger.info('random translation'.format())
        translation = [np.random.uniform(-1,1),np.random.uniform(-1,1),0] 
        lower_left = self.lower_left
        for wmesh in self.wmeshes:
            wmesh._mesh.vertices += translation
   
    #rotate second 
    def rand_rotate(self):
        self.logger.info('random rotation'.format())
        alpha = np.random.uniform(0,360)
        zaxis = [0,0,1] 
        R = trans.rotation_matrix(alpha,zaxis)
        for wmesh in self.wmeshes:
            wmesh.transform([R])

    # scale first 
    def rand_scale(self):
        self.logger.info('random scale'.format())
        scale = [np.random.normal(1,0.2),
                 np.random.normal(1,0.2),
                 np.random.normal(1,0.1),1] 
        S = np.diag(scale)
        for wmesh in self.wmeshes:
            wmesh.transform([S])










