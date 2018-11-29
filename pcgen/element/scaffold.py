#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import numpy as np
import pymesh as pm
import trimesh as tri
import trimesh.transformations as trans
from .element import Element
from pcgen.util.tictoc import TicToc
from pcgen.util.wrapmesh import WrapMesh
from pcgen.util.utils import PyMesh2Ply




class Scaffold(Element):

    """This is derived form the Element class"""

    name = 'scaffold'

    """ gibt das Gerüst immer im Eiheitswürfel zurück 
        scaffolds type => List<WrapMesh> 
        Class type => int               """
    
    def __init__(self,class_number,repetitions=[1,2,1]):
       
        self.class_number = class_number
        self.logger = logging.getLogger('pcgen.element.scaffold')
        T = TicToc(self.logger)
         
        n = repetitions[0]*repetitions[1]*repetitions[2]
        
        scaffolds = []
        thickness = 0.1
        
        scaling = [1/repetitions[0],1/repetitions[1],1/repetitions[2],1]
        dx = scaling[0]
        dy = scaling[1]
        dz = scaling[2]
        count = 0 

        for i in range(repetitions[0]):
            for j in range(repetitions[1]):
                for k in range(repetitions[2]):
                    count += 1
                    x =  i*dx
                    y =  j*dy 
                    z =  k*dz
                 
                    tmp = self._one_scaffold()
                    tmp.scale(scaling)
                    tmp.translate([x,y,z]) 
                    tmp.wmeshes[0].prefix = 'reg_{}'.format(count)
                    mesh = tmp.wmeshes
                    scaffolds.extend(mesh)
        
        
        self.logger.debug('total of {} scaffolds created'.format(n)) 

        Element.__init__(self,scaffolds,'scaffold')
        center = self.entire_mesh.center_mass
        center[2] = 0
        self.translate(-center)

        T.toc() 

    
    def _one_scaffold(self):
        thickness = 0.1
        T=TicToc(self.logger)
        
        p0 = np.array([-0.5,-0.5,0])
        p1 = np.array([0.5,-0.5,0])
        p2 = np.array([0.5,0.5,0])
        p3 = np.array([-0.5,0.5,0])
        
        p4 = np.array([-0.5,-0.5,1])
        p5 = np.array([0.5,-0.5,1])
        p6 = np.array([0.5,0.5,1])
        p7 = np.array([-0.5,0.5,1])
        
        vertices = np.vstack((p0,p1,p2,p3,p4,p5,p6,p7))
        edges = np.array([[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4], 
                            [0,2],[1,3],[4,6],[5,7],
                            [0,4],[1,5],[2,6],[3,7],
                            [0,5],[2,7]])
        
        wire  = pm.wires.WireNetwork.create_from_data(vertices, edges)
        
        inflator = pm.wires.Inflator(wire)
        inflator.inflate(thickness, per_vertex_thickness=False)
        scaffold = inflator.mesh

        scaffold = PyMesh2Ply(scaffold)
        mesh = WrapMesh(scaffold,'scaffold',self.class_number)
        mesh.prefix = 'raw_'
        element = Element([mesh],'raw_scaffold_ele') #not so clean here

        T.toc()
        return element 
   
    
    



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
        scale = [np.random.normal(0.8,0.3),
                 np.random.normal(1.3,0.2),
                 np.random.normal(0.8,0.1),1] 
        S = np.diag(scale)
        for wmesh in self.wmeshes:
            wmesh.transform([S])










