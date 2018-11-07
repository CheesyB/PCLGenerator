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
from .house import House
from .scaffold import Sacffold
import logging




class Hws(Element):

    """This is derived form the Element class"""

    def __init__(self,class_numbers):

        self.logger = logging.getLogger('generator.simples.elements.hws')
        reps = ** 
        T = TicToc(self.logger)
        

        hws = House() # returns (roof,mesh)
        hws.name = 'hws_ele'
        hws.wmeshes[0]._prefix = 'hws_'
        hws.wmeshes[1]._prefix = 'hws_'
        
        width = 0.01
        transl = (1+width,0,0) 
        scale = [1*0.25,1,1,1]
        
        scaffolds = Scaffold(reps)
        scaffolds.scale(scale)
        scaffolds.translate(transl)
        
        wmeshes = hws.wmeshes
        wmeshes.extend(scaffolds.wmeshes)
        
        Element.__init__(self,wmeshes,'hws')

        T.toc() 

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










