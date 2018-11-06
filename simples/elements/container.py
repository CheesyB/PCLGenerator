#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pymesh as pm
import trimesh as tri
from ..element import Element
from ..tictoc import TicToc
from ..wrapmesh import WrapMesh
from ..utils import PyMesh2Ply
import logging




class Container(Element):

    """This is derived form the Element class"""

    def __init__(self):
        """TODO: to be defined1. """
        Element.__init__(self)
        self.name = 'container'
        self.thickness = 0.1
        self.logger.getLogger('generator.simples.elements.container')
        
        T=TicToc(self.logger)
        
        #Big box minus smaller box inside equals simple container
        pmin = np.array([-0.5,-0.5,0])
        pmax = np.array([0.5,0.5,1])
        boxmesh = pm.generate_box_mesh(pmin,pmax)

        newMin = pmin + np.array([thickness,thickness,thickness])
        newMax = pmax - np.array([thickness,thickness,0])
        
        inner_boxmesh= pm.generate_box_mesh(newMin,newMax)

        union_mesh = pm.boolean(boxmesh, inner_boxmesh,'symmetric_difference',engine="cgal")
        union_mesh = PyMesh2Ply(union_mesh)
        
        num = self._class_dict['container']
        mesh = wm.WrapMesh(union_mesh,'container',num)
        mesh.prefix = 'reg_'

        Element.wmeshes = [mesh] 
        T.toc()
