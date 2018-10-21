#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import trimesh as tri
import pandas as pa
import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt
import pyntcloud as pc


class Element(object):

    """Docstring for Element. """

    def __init__(self,name,wmeshes):
        """TODO: to be defined1.

        :wmeshes: TODO

        """
        self.wmeshes = wmeshes
        self._name = name
    
    
    @property
    def pointcloud(self):
        return np.hstack([wmesh.pointcloud for wmesh in self._wmeshes])
    
    @property 
    def pointcloud_class(self):
        return np.hstack([wmesh.pointcloud_class for wmesh in self._wmeshes])
    
    @property 
    def pointcloud_color(self):
        return np.hstack([wmesh.pointcloud_color for wmesh in self._wmeshes])
    
    
    def save_mesh():

    def save_mesh():


    def save_pc():



