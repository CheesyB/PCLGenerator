#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import numpy as np
import pymesh as pm
import trimesh as tri
import trimesh.transformations as trans
from pcgen.util.wrapmesh import WrapMesh 
from pcgen.util.tictoc import TicToc
from pcgen.util.utils import PyMesh2Ply
from .element import Element




class House(Element):

    """This is derived form the Element class"""

    name = 'house'

    def __init__(self,class_numbers):
        
        self._roof_height = np.random.normal(0.8,0.2)
        self.logger = logging.getLogger('pcgen.element.house')
        T=TicToc(self.logger)
        
        pmin = np.array([-0.5,-0.5,0])
        pmax = np.array([0.5,0.5,1])


        x = pmin[0]
        y = pmin[1]
        z = pmin[2]

        X = pmax[0]
        Y = pmax[1]
        Z = pmax[2]

        p0 = pmin
        p1 = np.array([X,y,z])
        p2 = np.array([X,Y,z])
        p3 = np.array([x,Y,z])
        p4 = np.array([x,y,Z])
        p5 = np.array([X,y,Z])
        p6 = pmax
        p7 = np.array([x,Y,Z])
        
        vertices = np.vstack((p0,p1,p2,p3,p4,p5,p6,p7)) 
        hull = tri.convex.convex_hull(vertices)

        body = tri.Trimesh(vertices=hull.vertices,faces=hull.faces)
        bodymesh = WrapMesh(body,'body',class_numbers[0])
        bodymesh.prefix = 'reg_'
        
        
        
        
        p8 = pmin + np.array([1/2,0,1+self._roof_height])
        p9 = pmin + np.array([1/2,1,1+self._roof_height])
        
        vertices = np.vstack((p4,p5,p6,p7,p8,p9))
        hull = tri.convex.convex_hull(vertices)
        
        roof = tri.Trimesh(vertices=hull.vertices,faces=hull.faces)
        roofmesh = WrapMesh(roof,'roof',class_numbers[1])
        roofmesh.prefix = 'reg_'
        
        meshes = list((roofmesh,bodymesh)) 
        Element.__init__(self,[roofmesh,bodymesh],'house')
        
        T.toc() 



    def rand_translate(self):
        self.logger.debug('random translation'.format())
        translation = [np.random.uniform(-1,1),np.random.uniform(-1,1),0] 
        lower_left = self.lower_left
        for wmesh in self.wmeshes:
            wmesh._mesh.vertices += translation
   
    #rotate second 
    def rand_rotate(self):
        self.logger.debug('random rotation'.format())
        alpha = np.random.uniform(0,360)
        zaxis = [0,0,1] 
        R = trans.rotation_matrix(alpha,zaxis)
        for wmesh in self.wmeshes:
            wmesh.transform([R])

    # scale first 
    def rand_scale(self):
        self.logger.debug('random scale'.format())
        scale = [np.random.normal(3,1),
                 np.random.normal(1.5,0.7),
                 np.random.normal(1.5,0.6),1] 
        S = np.diag(scale)
        for wmesh in self.wmeshes:
            wmesh.transform([S])










