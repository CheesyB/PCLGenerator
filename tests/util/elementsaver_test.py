#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
import trimesh as tri
from pcgen.util import wrapmesh as wm
from pcgen.util import elementsaver as es
from pcgen.element import container

class ElementSaverTest(unittest.TestCase):
    
    def setUp(self):
        self.box = tri.creation.annulus()
        self.wmesh = wm.WrapMesh(self.box,'body',1)
        self.ele = container.Container(1)         

    def test_save_as_pc(self):
        saver = es.ElementSaver('../../data')
        saver.save_as_pc(self.ele)

    def test_delet_files(self):
        saver = es.ElementSaver('../../data')
        saver.delete_files()


if __name__ == "__main__":
    unittest.main()
