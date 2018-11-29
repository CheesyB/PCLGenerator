#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging 
import numpy as np
import pandas as pd
from pyntcloud  import PyntCloud 
from collections import Counter
from pcgen.util import tictoc
import ipdb


class Scene(object):

    """ This class holdes mulitple elements arranged together in the x,y-plane.
        This composes a scene which is consumned by the hd5dataset. The hd5dataset 
        slices the sene into parts of m-points and samples  m points form that.
        These points become on "Image" of the a mini-batch """ 
        
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

    def __str__(self):
        string = ('number points: {}\n'
        'number classes: {}\n'
        'occ. per class: {}\n'.format(self.shape,
                                            self.contained_classes,
                                            self.occurence_per_class))
        return string 
    
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
    
    #Mega zeitaufwendig...
    def get_nearest_neighbors(self,num_neighbors=3000):
        T = tictoc.TicToc(self.logger)
        self.logger.info('calc. the neighbors {}'.format(num_neighbors))
        pc_df = pd.DataFrame(self._pointcloud,columns=['x','y','z','class_number']) 
        pc = PyntCloud(pc_df)
        neighbors = pc.get_neighbors(k=num_neighbors)
        T.toc()
        return neighbors
    
    def one_slice(self,pmin,pmax):
        pc = self.pointcloud
        index_to_take = [] 
        for index in range(pc.shape[0]):
            point = (pc[index,0],pc[index,1])
            if all(_min < pnt for _min,pnt in zip(pmin,point)) and \
               all(_max > pnt for _max,pnt in zip(pmax,point)):
                index_to_take.append(index) 
        return np.take(pc,index_to_take,axis=0)
                                            
    
    def _sample_pointcloud(self,elements):
        pc_scene = np.empty([1,4]) # fist line will be deleted later
        for ele in self._elements:
            for wmesh in ele.wmeshes:
                pc = wmesh.pointcloud_class      
                self._all_classes.append(int(pc[-1][-1]))
                pc_scene = np.append(pc_scene,pc,axis=0) #inplace?
        pc_scene = np.delete(pc_scene,0,0) 
        return pc_scene
        

    
