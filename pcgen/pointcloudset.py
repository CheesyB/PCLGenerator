#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import h5py as hd



class PointCloudSet(object):

    """ We assume a nx4 Array where the 4th column represents the class as int.
        The class is not represented as an in in the scene class but as the coordinates
        as floats. Here they are converted, to save diskspace. Just in case we get
        rounding error porblems """

    def __init__(self,filehandle,named_classes):
        """

        """
        self.logger = logging.getLogger('pcgen.scene..Scene')
#        self._operating_path = operating_path
        
#        if not os.path.isdir(operating_path):
#            self.logger.warning('operating folder not found!')
#            raise Exception('operating folder not found!') 
#        
#        if not os.path.exists(os.path.join(operating_path,file_name))
#            self.logger.warning('file does not exist. Creating new one')
#            self._create_file()
        
        self._file = filehandle
        self._named_classes = named_classes
        self._scenes = []
        
   
    def append(self,scene):
        self._scenes.append(scene)
        self.logger.info('{}th scene added'.format(len(self._scenes)))

    def write_data(self):
        count = 0
        f = self._file
        custom_type = np.dtype([('x', np.float),
                        ('y', np.float),
                        ('z', np.float),
                        ('class_number', np.uint8)]) # should be enought:)
        for scene in self._scenes:
            pc = scene.pointcloud
            f.create_dataset('/{}scene'.format(count),
                            secene.shape)
                 
h5 = h5py.File("my_data.h5", "w")
data = [(1003, 4321, 43.2, "ACGTACTG"), (55, 4098, 12.1, "GGT"), (3209, 909, 59.7, "ACTAC")]
dataset = h5.create_dataset('/coordinates', (len(data),), dtype=my_datatype)
data_array = np.array(data, dtype=my_datatype)






    

    
    def save(self, path):
        """TODO: Docstring for .

        :path: TODO
        :returns: TODO

        """
        pass 
    
    def _generate_attribute(self):
        """TODO: Docstring for _generate_attribute.
        :returns: TODO

        """
        pass

