#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import random 
import numpy as np
import pymesh as pm
import trimesh as tri
import pcgen.util.wrapmesh as wm
from pcgen.util.tictoc import TicToc
from pcgen.util.utils import PyMesh2Ply



def count():
    n = 1
    while True:
        yield n
        n += 1


class ElementFactory(object):

    """Docstring for ObjectFactory. """
    class_dict = {'basement':(0,1),
            'house':(2,3),
            'hws':(2,3,5),
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
        self.registered_elements = {} 
        self.logger = logging.getLogger('pcgen.element.ElementFactory')

    def get_registered_element_names(self):
        return [ele.name for ele in self.registered_elements]

    @property
    def id(self):
        self._id += 1
        self.logger.debug('element id is {}'.format(self._id))
        return self._id

    """ This is supposed to be the element constructor """
    def register_element(self,element_ctor):
        self.registered_elements[element_ctor] = 0

    """ This function returns a sequence of given length 
        containing a random amount of registerd elements """
    def get_random_sequence(self,howmany):
        sequence = []
        for _ in range(howmany):
            ctor = random.choice(list(self.registered_elements))
            self.registered_elements[ctor] += 1
            count = self.registered_elements[ctor]
            self.logger.info('We got a {} ({})'.format(ctor.name,count)) 
            ele = ctor(ElementFactory.class_dict[ctor.name])
            ele.prefix = str(count)
            ele.rand_scale()
            ele.rand_rotate()
            sequence.append(ele)
        return sequence
    










    






