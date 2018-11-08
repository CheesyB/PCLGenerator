#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pymesh as pm
import trimesh as tri
import trimesh.transformations as trans
from .element import Element
from pcgen.util.tictoc import TicToc
from pcgen.util.wrapmesh import WrapMesh
from pcgen.util.utils import PyMesh2Ply
import logging




class Container(Element):

    """This is derived form the Element class"""
    name = 'container'

    def __init__(self,class_number):
        
        self.thickness = 0.1
        self.logger = logging.getLogger('pcgen.element.container') # define here, otherwise logger
        T=TicToc(self.logger)
        
        #Big box minus smaller box inside equals simple container
        pmin = np.array([-0.5,-0.5,0])
        pmax = np.array([0.5,0.5,1])
        boxmesh = pm.generate_box_mesh(pmin,pmax)

        newMin = pmin + np.array([self.thickness,self.thickness,self.thickness])
        newMax = pmax - np.array([self.thickness,self.thickness,0])
        
        inner_boxmesh= pm.generate_box_mesh(newMin,newMax)

        union_mesh = pm.boolean(boxmesh, inner_boxmesh,'symmetric_difference',engine="cgal")
        union_mesh = PyMesh2Ply(union_mesh)
        
        mesh = WrapMesh(union_mesh,'container',class_number)
        mesh.prefix = 'reg_'

        Element.__init__(self,mesh,'container')
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
        scale = [np.random.normal(0.5,0.1),
                 np.random.normal(0.3,0.1),
                 np.random.normal(0.2,0.1),1] 
        S = np.diag(scale)
        for wmesh in self.wmeshes:
            wmesh.transform([S])

            









