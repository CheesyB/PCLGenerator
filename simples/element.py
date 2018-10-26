#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import trimesh as tri
import pandas as pa
import numpy as np
import pyntcloud as pc
import trimesh.transformations as trans
from .wrapmesh import WrapMesh 
from .tictoc import TicToc

class Element(object):

    """Docstring for Element. """

    def __init__(self,wmeshes,name):
        """TODO: to be defined1.

        :wmeshes: TODO

        """
        self.wmeshes = wmeshes
        self.name = name
        self.logger = logging.getLogger('generator.simples.element')
    
    
    @property
    def trimeshes(self):
        return [wmesh._mesh for wmesh in self.wmeshes]

    @property
    def pointcloud(self):
        return np.vstack([wmesh.pointcloud for wmesh in self.wmeshes])
    
    @property 
    def pointcloud_class(self):
        return np.vstack([wmesh.pointcloud_class for wmesh in self.wmeshes])
    
    @property
    def entire_mesh(self):
        return tri.util.concatenate(self.trimeshes)
   

    """ with focus on the rectangle packer  """
    @property
    def ground_truth(self): 
        tol  = 0.1
        bbox = self.entire_mesh.bounding_box
        points = [point for point in bbox.vertices if abs(point[2]) < tol] 
        xmin = min(points[0,:])
        ymin = min(points[1,:])
        xmax = max(points[0,:])
        ymax = max(points[1,:])
        w = xmax - xmin
        h = ymax - ymin 
        return (w, h, xmin, ymin) 


    def transform(self,transl,scale,alpha):
        zaxis = [0,0,1] 
        R = trans.rotation_matrix(alpha,zaxis)
        S = np.diag(scale)
        T = trans.translation_matrix(transl)
        
        #Z = shear_matrix(beta, xaxis, origin, zaxis)
        for wmesh in self.wmeshes:
            wmesh.transform([R,S,T])

    #translate last 
    def translate(self,translation=None):
        if translation is None:
            translation = [np.random.uniform(-1,1),np.random.uniform(-1,1),0] 
        for wmesh in self.wmeshes:
            wmesh._mesh.vertices += translation
   
    #rotate second 
    def rotate(self,alpha=None):
        if alpha is None:
            alpha = np.random.uniform(0,360)
        zaxis = [0,0,1] 
        R = trans.rotation_matrix(alpha,zaxis)
        for wmesh in self.wmeshes:
            wmesh.transform([R])

    # scale first 
    def scale(self,scale=None):
        if scale is None:
            scale = [np.random.normal(1,0.2),
                     np.random.normal(1,0.2),
                     np.random.normal(1,0.1),1] 
        S = np.diag(scale)
        for wmesh in self.wmeshes:
            wmesh.transform([S])
    
    
    
    def get_bboxo(self):
        total_mesh = self.entire_mesh 
        bboxo = total_mesh.bounding_box_oriented
        return bboxo
    
    def add_element(self,other_element):
        self.wmeshes.extend(other_element.wmeshes)
        self.logger.info(' added element ' +
                        '{} to {}'.format(other_element.name, self.name))




##def test():
    

    
#    wmesh = wm.WrapMesh(tri.creation.box,'test',1)
#    elebox = Element(wmesh,'test')
#    
#    basement = basement()
#    pc = basement.pointcloud_class
#    bbox = basement.get_bbox()
#    basement.scale()
#    basement.rotate()
#    basement.translate()
#
#    container = o.container()
#    pc = container.pointcloud_class
#    bbox = container.get_bbox()
#    container.scale()
#    container.rotate()
#    container.translate()
#
#    house = o.house()
#    pc = house.pointcloud_class
#    bbox = house.get_bbox()
#    gt = house.ground_truth
#    house.scale()
#    house.rotate()
#    house.translate()
#
#    scaffold = o.scaffold()
#    pc = scaffold.pointcloud_class
#    bbox = scaffold.get_bbox()
#    scaffold.scale()
#    scaffold.rotate()
#    scaffold.translate()
#
#    basement.add_element(scaffold)
#    basement2 = Element(basement.wmeshes + container.wmeshes,'concat')
#    
#    
#    saver = utils.ElementSaver(cdict,'data')
#    saver.delete_files()
##    saver.save_as_pc(basement) 
##    saver.save_as_pc(container) 
##    saver.save_as_pc(house) 
#    saver.save_as_pc(scaffold) 
#    
##    saver.save_as_pc(basement2)



if __name__ == "__main__":
    test()

