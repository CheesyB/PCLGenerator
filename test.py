#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import logging 
import numpy as np
import trimesh as tri
import simples.wrapmesh as  wm
import simples.element as el
import simples.elementsaver as es
import simples.elementfactory as ef


class TestWrapMesh(unittest.TestCase):


    def setUp(self):
        self.box = tri.creation.annulus()
        self.wmesh = wm.WrapMesh(self.box,'test',1)
        #logging in unittests is a bad idea
    


    def test_type(self):
        self.assertEqual(type(self.wmesh),wm.WrapMesh,'Obj is not a WrapMesh')

    def test_stringing(self):
        self.assertEqual(str(self.wmesh),'test','Stringing the obj is wrong')

    def test_name(self):
        self.assertEqual(self.wmesh.name,'reg_test','Property does not work')
    
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


class TestElement(unittest.TestCase):

    def setUp(self):
        self.box = tri.creation.annulus()
        self.wmesh = wm.WrapMesh(self.box,'test',1)
        self.ele = el.Element([self.wmesh,self.wmesh],'test')         

    def test_type(self):
        self.assertEqual(type(self.ele),el.Element,'Obj is not an Element')

    def test_trimeshes(self):
        trimeshes = self.ele.trimeshes 
        self.assertTrue(trimeshes,'Obj is of type {}, should be list'.format(type(trimeshes)))

    def test_pointcloud(self):
        pointcloud = self.ele.pointcloud
        self.assertEqual(pointcloud.shape[1],3,' dims not correct')

    
    def test_pointcloud_class(self):
        pointcloud_class = self.ele.pointcloud_class
        self.assertEqual(pointcloud_class.shape[1],4,' dims not correct')
    
    def test_entire_mesh(self):
        try:
            bigmesh = self.ele.entire_mesh
        except ValueError:
            self.fail("Element.entire_mesh raised ExceptionType unexpectedly!")
    
    def test_ground_truth(self):
        try:
            gt = self.ele.ground_truth
        except ValueError:
            self.fail("Element.ground_truth raised ExceptionType unexpectedly!")
    
    """ transform anytime, rotation ony around the z-axis """
    def test_transform(self):
        self.ele.transform([1,2,3,4],[1,2,3,4], 100)

    #translate last 
    def test_translate(self):
        self.ele.translate()
   
    #rotate second 
    def test_rotate(self):
        self.ele.rotate()

    # scale first 
    def test_scale(self):
        self.ele.scale()
    
    def test_get_bboxo(self):
        self.ele.get_bboxo()

    def test_add_element(self):
        self.ele.add_element(self.ele)

class TestElementSaver(unittest.TestCase):
    
    def setUp(self):
        self.box = tri.creation.annulus()
        self.wmesh = wm.WrapMesh(self.box,'body',1)
        self.ele = el.Element([self.wmesh,self.wmesh],'test')         

    def test_save_as_pc(self):
        saver = es.ElementSaver('/home/tbreu/workbench/generator/data')
        saver.save_as_pc(self.ele)

    def test_delet_files(self):
        saver = es.ElementSaver('/home/tbreu/workbench/generator/data')
        saver.delete_files()



class TestElementFactory(unittest.TestCase):
    
    def setUp(self):
        self.box = tri.creation.annulus()
        self.wmesh = wm.WrapMesh(self.box,'body',1)
        self.ele = el.Element([self.wmesh,self.wmesh],'test')         
        self.EleFac = ef.ElementFactory(2)
    
    
    def test_element_factory(self):
        EleFac = ef.ElementFactory(2)

    def test_get_class_names(self): 
        classnames = ef.ElementFactory.get_class_names()
        self.assertEqual(classnames,['basement_low','basement_up',
            'container','scaffold','roof','body'])

    def test_basement(self):
        self.EleFac.basement()

    def test_container(self):
        self.EleFac.container()

    def test_scaffold(self):
        self.EleFac.container()

    def test_house(self):
        self.EleFac.container()

    def test_hws(self):
        self.EleFac.container()



if __name__ == "__main__":
    unittest.main()













