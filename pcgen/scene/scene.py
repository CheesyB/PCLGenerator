#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging 
import numpy as np
import pandas as pd
import pyntcloud as pc
from collections import Counter


class Scene(object):

    """Docstring for Scene. """

    def __init__(self,elements):
        """TODO: manage numbers of points
            

        :elements: TODO

        """
        self._elements = elements
        self._all_classes = []
        self._pointcloud = self._sample_pointcloud(elements)
        self.logger = logging.getLogger('pcgen.scene.scene.Scene')
        self.logger.info(' classes: {}'.format(self.occurence_per_class))

    def __len__(self):
        return self._pointcloud.shape[0] # number of points
    
    @property
    def shape(self):
        return self._pointcloud.shape

    @property
    def contained_classes(self):
        return set(self._all_classes)

    @property 
    def different_classes(self):
        return len(self.contained_classes)
    
    @property
    def occurence_per_class(self):
        cnt = Counter(self._all_classes)
        [cnt[class_number] + 1 for class_number in self._all_classes] 
        self.logger.debug('counter counted: {}'.format(cnt))
        return cnt
    
    @property 
    def pointcloud(self):
        return self._pointcloud
    
    def _sample_pointcloud(self,elements):
        pc_scene = np.empty([1,4]) # fist line will be deleted later
        for ele in self._elements:
            for wmesh in ele.wmeshes:
                pc = wmesh.pointcloud_class      
                self._all_classes.append(int(pc[-1][-1]))
                pc_scene = np.append(pc_scene,pc,axis=0) #inplace
        pc_scene = np.delete(pc_scene,0,0) 
        return pc_scene
        

    
