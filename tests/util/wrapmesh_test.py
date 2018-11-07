#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
import logging 
import numpy as np
import trimesh as tri
from pcgen.util import wrapmesh as wm


class WrapMeshTest(unittest.TestCase):


    def setUp(self):
        self.box = tri.creation.annulus() 
        self.wmesh = wm.WrapMesh(self.box,'test',1) #logging in unittests is a bad idea
    


    def test_type(self):
        self.assertEqual(type(self.wmesh),wm.WrapMesh,'Obj is not a WrapMesh')

    def test_stringing(self):
        self.assertEqual(str(self.wmesh),'test','Stringing the obj is wrong')

    def test_name(self):
        self.assertEqual(self.wmesh.name,'raw_test','Property does not work')
    
    def test_pointcloud(self): 
        cloud = self.wmesh.pointcloud
        self.assertEqual(cloud.shape[1],3 ,'dimensions are wrong')

    def test_pointcloud_class(self): 
        cloud = self.wmesh.pointcloud_class
        self.assertEqual(cloud.shape[1],4 ,'dimensions are wrong')
    
    def test_pyntcloud(self): 
        cloud = self.wmesh.pyntcloud
        self.assertEqual(cloud.points.shape[1],3 ,'dimensions are wrong')

    def test_pyntcloud_class(self): 
        cloud = self.wmesh.pyntcloud_class
        self.assertEqual(cloud.points.shape[1],4 ,'dimensions are wrong')

    def test_transform(self):
        self.wmesh.transform([np.diag([1,1,1,4])])

if __name__ == "__main__":
    unittest.main()


