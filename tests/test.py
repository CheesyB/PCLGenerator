#!/usr/bin/env python
# -*- coding: utf-8 -*-

import generator as gen

import unittest
import logging 
import numpy as np
import trimesh as tri
import simples.wrapmesh as  wm 
import simples.element as el 
import simples.elementsaver as es
import simples.elementfactory as ef
import simples.elements.container as container
import simples.elements.basement as basement 




#class TestElement(unittest.TestCase):
#
#    def setUp(self):
#        self.box = tri.creation.annulus() 
#        self.wmesh = wm.WrapMesh(self.box,'test',1)
#        self.ele = el.Element([self.wmesh,self.wmesh],'test')         
#
#    def test_type(self):
#        self.assertEqual(type(self.ele),el.Element,'Obj is not an Element')
#
#    def test_trimeshes(self):
#        trimeshes = self.ele.trimeshes 
#        self.assertTrue(trimeshes,'Obj is of type {}, should be list'.format(type(trimeshes)))
#
#    def test_pointcloud(self):
#        pointcloud = self.ele.pointcloud
#        self.assertEqual(pointcloud.shape[1],3,' dims not correct')
#
#    
#    def test_pointcloud_class(self):
#        pointcloud_class = self.ele.pointcloud_class
#        self.assertEqual(pointcloud_class.shape[1],4,' dims not correct')
#    
#    def test_entire_mesh(self):
#        try:
#            bigmesh = self.ele.entire_mesh
#        except ValueError:
#            self.fail("Element.entire_mesh raised ExceptionType unexpectedly!")
#    
#    def test_ground_truth(self):
#            gt = self.ele.ground_truth
#    
#    """ transform anytime, rotation ony around the z-axis """
#    def test_transform(self):
#        self.ele.transform([1,2,3,4],[1,2,3,4], 100)
#
#    #translate last 
#    def test_translate(self):
#        self.ele.translate()
#   
#    #rotate second 
#    def test_rotate(self):
#        self.ele.rotate()
#
#    # scale first 
#    def test_scale(self):
#        self.ele.scale()
#    
#    def test_get_bboxo(self):
#        self.ele.get_bboxo()
#
#    def test_add_element(self):
#        self.ele.add_element(self.ele)
#    
#    def test_lower_left(self):
#        ll = self.ele.lower_left 



        

if __name__ == "__main__":
    unittest.main()













