#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import logging
import numpy as np
import pandas as pd
from scipy import spatial
import h5py 
sys.setrecursionlimit(10000)


class Dataset(object):

    """ We assume a nx4 Array where the 4th column represents the class as int.
        The class is not represented as an in in the scene class but as the coordinates
        as floats. Here they are converted, to save diskspace. Just in case we get
        rounding error porblems """

    def __init__(self,file_path,named_classes=None,extended=1):
        """

        """
        self.logger = logging.getLogger('pcgen.scene.dataset')
        
#        self._operating_path = operating_path
        
#        if not os.path.isdir(operating_path):
#            self.logger.warning('operating folder not found!')
#            raise Exception('operating folder not found!') 
#        
#        if not os.path.exists(os.path.join(operating_path,file_name))
#            self.logger.warning('file does not exist. Creating new one')
#            self._create_file()
        with open(file_path, 'wb') as self._file:
            self._file = h5py.File(file_path,'w')
        """ Add named_classes to the attributes of the root group """
        self._named_classes = named_classes 
        self._extended = extended
        self._scenes = []
        
   
    def append(self,scene):
        self._scenes.append(scene)
        self.logger.info('{}th scene added'.format(len(self._scenes)))

    def write_data(self):
        for idx,scene in enumerate(self._scenes):
            current_pc = scene.pointcloud.copy()
            grp = self._file.create_group('scene{}'.format(idx))
            grp.attrs['description'] =  str(scene)
            if self._extended > 0:
                grp.create_dataset('cloud',
                                    data=scene.pointcloud,
	                            dtype=np.float32)#we wirte the whole cloud
            count = 0 
            while current_pc.shape[0] > 3000:
                random_point = current_pc[np.random.choice(current_pc.shape[0])]
                _,index = spatial.KDTree(current_pc[:,:3]).query(random_point[:3],k=3000)
                point_sample = current_pc[index]
                current_pc = np.delete(current_pc,index,0) 
                self.logger.debug('the overall length must reduce: {}'.format(current_pc.shape[0]))
                grp.create_dataset('slice{}'.format(count),
                                    data=point_sample,
	                            dtype=np.float32)# pytorch demands float32 
                count += 1
            self.logger.info('I got {} slices out of this scene'.format(count))
            grp.attrs['scenes'] = count

		


            
            

