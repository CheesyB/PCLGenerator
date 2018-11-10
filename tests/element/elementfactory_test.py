#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from pcgen.element import elementfactory as ef
from pcgen.element import container 
from pcgen.element import basement 
from pcgen.element import house
from pcgen.element import hws
from pcgen.element import scaffold



class ElementFactoryTest(unittest.TestCase):
    
    def setUp(self):
        self.elefac = ef.ElementFactory()
        self.ele = []
        self.ele.append(scaffold.Scaffold)
        self.ele.append(basement.Basement)
        self.ele.append(container.Container)
        self.ele.append(house.House)
        self.ele.append(hws.Hws)
        [self.elefac.register_element(ele) for ele in self.ele]

    def test_get_registerd_element_ctor_names(self): 
        classnames = self.elefac.get_registered_element_names()
        self.assertEqual(classnames,['scaffold','basement',
            'container','house','hws'])
   
    def test_get_random_sequence(self):
        sequ = self.elefac.get_random_sequence(5)
        self.assertTrue(sequ,'This should be a list')
        self.assertEqual(len(sequ),5)



if __name__ == "__main__":
    unittest.main(verbosity=2)
