#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
import trimesh as tri
from subprocess import call
from pcgen.util import wrapmesh as wm
from pcgen.util import elementsaver as es
from pcgen.element import container

class ElementSaverTest(unittest.TestCase):
    
    def setUp(self):
        self.box = tri.creation.annulus()
        self.wmesh = wm.WrapMesh(self.box,'body',1)
        self.ele = container.Container(1)         
        call(['touch', '/home/tbreu/workbench/pcgen/tests/util/data/tmp1.txt'])

        

    def test_save_as_pc(self):
        saver = es.ElementSaver('/home/tbreu/workbench/pcgen/tests/util/data')
        saver.save_as_pc(self.ele)

    def test_delet_files(self):
        saver = es.ElementSaver('/home/tbreu/workbench/pcgen/tests/util/data')
        saver.delete_files()


if __name__ == "__main__":
    unittest.main()
