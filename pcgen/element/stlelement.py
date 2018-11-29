#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import numpy as np
import pymesh as pm
import trimesh as tri
import trimesh.transformations as trans
from .element import Element # this thing makes it not invocable directly
from pcgen.util.tictoc import TicToc
from pcgen.util.wrapmesh import WrapMesh
from pcgen.util.utils import PyMesh2Ply




class StlElementFactory(object):

    
    name = 'filelement'

    def __init__(self,class_numbers,name,file_path,transformer):
        self.logger = logging.getLogger('pcgen.element.filelement')
        T=TicToc(self.logger)
      
        self._class_number = class_numbers
        self._name = name
        self._file_path = file_path
        self._transformer = transformer
        mesh = tri.load(self._file_path)
        wmesh = WrapMesh(mesh,classname,classnum) 

    def __call__(self):
        return Element(self,wmesh,self._name)
    



