#!/usr/bin/env python
# -*- coding: utf-8 -*-




class Scene(object):

    """Docstring for Scene. """

    def __init__(self,elements,path):
        """TODO: manage numbers of points
            

        :elements: TODO

        """
        self._elements = elements
        self._path = path
        
    def _sample_pointcloud(self):
        pass

    def save_pointcloud(self):
        pass

    def _slice(self):
        pass

    def save_to_hdf5(self):
        pass

    
