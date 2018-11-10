#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from pcgen.scene.scene import Scene
from pcgen.element import container 



class SceneTest(unittest.TestCase):
   
    def setUp(self):
        ele1 = container.Container(0)
        ele2 = container.Container(1)
        ele3 = container.Container(2)
        self.eles = [ele1,ele2,ele3]

    def test_scene(self):
        scene = Scene(self.eles)
        self.assertEqual(scene._pc_scene.shape[1],4)
    
    def test_number_classes(self):
        scene = Scene(self.eles)
        self.assertEqual(scene.different_classes,3)
    
    def test_occurence_per_class(self):
        scene = Scene(self.eles)
        self.assertEqual(scene.occurence_per_class,{0:1,1:1,2:1})

if __name__ == "__main__":
    unittest.main(verbosity=2)
