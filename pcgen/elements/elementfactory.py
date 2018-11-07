#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pymesh as pm
import trimesh as tri
import simples.wrapmesh as wm
import simples.element as ele
from simples.tictoc import TicToc
from simples.utils import PyMesh2Ply
import logging



def count():
    n = 1
    while True:
        yield n
        n += 1


class ElementFactory(object):

    """Docstring for ObjectFactory. """
    class_dict = {'basement_up':0,
            'basement_low':1,
            'roof':2,
            'body':3,
            'container':4,
            'scaffold':5}

    def __init__(self):
        """This Class is creates simple objects with their center 
            in the origin.
            Every object is returned as an Element holding one or 
            more WrapMesh objects        

        :classdict: maps the classe names to their corresponding 
                    class value(int)

        """
        self._id = 0 
        self.registerd_elements = {} 
        self.logger = logging.getLogger('generator.simples.ElementFactory')

    @staticmethod
    def get_registered_element_names():
        return [ele.name for ele in self.registerd_elements]

    @property
    def id(self):
        self._id += 1
        self.logger.debug('element id is {}'.format(self._id))
        return self._id

    def register_element(self,element_class):
        self.registerd_elements[element_class] = 0

   
    






