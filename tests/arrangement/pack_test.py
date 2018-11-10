#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from pcgen.arrangement import pack 
from pcgen.element import container 
from pcgen.element import basement 



class RectangleArrangerTest(unittest.TestCase):
   
    def setUp(self):
        self.arranger = pack.RectangleArranger(10,10)
        self.cont = container.Container(1)
        self.basem = basement.Basement((2,3))
    
    def test_pack_stuff(self):
        packer =  self.arranger.packstuff([self.cont,self.basem])
        self.assertTrue(packer)



if __name__ == "__main__":
    unittest.main(verbosity=2)

