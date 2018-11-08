#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import pandas as pa
import numpy as np
import pyntcloud as pc
import os, shutil
from .tictoc import TicToc


class ElementSaver(object):


    """Docstring for Saver. """
    default_color_dict = {'basement_up':(1,0,0),
                        'basement_low':(0,1,0),
                        'roof':(1,1,0),
                        'body':(1,0,1),
                        'container':(0,1,1),
                        'scaffold':(0.5,1,0.5)}
    
    def __init__(self,data_path,color_dict=None):
        """TODO: to be defined1.

        :color_dict: TODO
        :data_path: TODO

        """
        self._color_dict = color_dict
        if self._color_dict is None:
            self._color_dict = ElementSaver.default_color_dict
        self._data_path = data_path
        self.logger = logging.getLogger(__name__)
        
    def save_as_mesh(self,element):
        raise NotImplemented
        pass

    """ This return a hopefully destinct color for int; actually a colormap """
    def get_colo(self,val):
            color = np.array([0.22 * val % 1,
                              0.33 * val % 1,
                              0.55 * val % 1])
            return color

    
    
    def save_as_pc(self,element):
        for wmesh in element.wmeshes:
            T = TicToc(self.logger,' sample pointcloud as np.array \
                    with color {} from {}'.format(color,str(wmesh)))
            points = wmesh.pointcloud_class 
            color = points[-1][-1]
            class_points = np.array([color for _ in range(points.shape[0])])
            points = np.concatenate((points,class_points), axis=1)

            dataframe = pa.DataFrame(columns=['x','y','z','red','green','blue'],data=points)
            pyntcloud = pc.PyntCloud(dataframe)
            pyntcloud.to_file(self._data_path + '/pc_{}_{}.ply'.format(wmesh.name,element.savename))
            self.logger.info('pc_{}_{}.ply  pointcloud(color)'
                            'written'.format(wmesh.name,element.name))
            T.toc()
    
    
    def delete_files(self):
        i = 0
        for the_file in os.listdir(self._data_path):
            file_path = os.path.join(self._data_path, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    i += 1
                    self.logger.debug('{} deleted'.format(file_path))
                #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
        self.logger.info(' {} files deleted'.format(i))




