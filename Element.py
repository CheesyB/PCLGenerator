#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import trimesh as tri
import pandas as pa
import numpy as np
import pyntcloud as pc
import utils
import Objects as o
import trimesh.transformations as trans

class Element(object):

    """Docstring for Element. """

    def __init__(self,wmeshes,name):
        """TODO: to be defined1.

        :wmeshes: TODO

        """
        self.wmeshes = wmeshes
        self.name = name
        self.logger = logging.getLogger('generator.Element')
    
    
   
    def set_class(self,class_dict):
        for wmesh in self.wmeshes:
            cnum = class_dict[str(wmesh)]
            wmesh.class_num = cnum
    
    
    @property
    def trimeshes(self):
        return [wmesh._mesh for wmesh in self.wmeshes]

    @property
    def pointcloud(self):
        return np.hstack([wmesh.pointcloud for wmesh in self.wmeshes])
    
    @property 
    def pointcloud_class(self):
        return np.hstack([wmesh.pointcloud_class for wmesh in self.wmeshes])
    
    @property
    def entire_mesh(self):
        return tri.util.concatenate(self.trimeshes)


    def transform(transl,scale,alpha):
        zaxis = [0,0,1] 
        R = trans.rotation_matrix(alpha,zaxis)
        S = np.diag(scale)
        T = trans.translation_matrix(transl)
        
        #Z = shear_matrix(beta, xaxis, origin, zaxis)
        for wmesh in self.wmeshes:
            self.wmeshes([R,S,T])
    
    def translate(self,translation=None):
        if translation is None:
            translation = [np.random.uniform(-1,1),np.random.uniform(-1,1),0] 
        for wmesh in self.wmeshes:
            wmesh._mesh.vertices += translation
    
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
    
    
    
    def get_bbox(self):
        total_mesh = self.entire_mesh 
        bboxo = total_mesh.bounding_box_oriented
        return bboxo
    
    def add_element(self,other_element):
        self.wmeshes.extend(other_element.wmeshes)
        self.logger.info(' added element ' +
                        '{} to {}'.format(other_element.name, self.name))


if __name__ == "__main__":
    test()


def test():
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('generator').setLevel(logging.INFO)
    logging.getLogger('trimesh').setLevel(logging.CRITICAL)
    
    cdict = {'basement_up':(1,0,0),
            'basement_low':(0,1,0),
            'roof':(1,1,0),
            'body':(1,0,1),
            'container':(0,1,1),
            'scaffold':(0.5,0.5,0.5)}

    basement = o.basement()
    pc = basement.pointcloud_class
    bbox = basement.get_bbox()
    basement.scale()
    basement.rotate()
    basement.translate()

    container = o.container()
    pc = container.pointcloud_class
    bbox = container.get_bbox()
    container.scale()
    container.rotate()
    container.translate()

    house = o.house()
    pc = house.pointcloud_class
    bbox = house.get_bbox()
    house.scale()
    house.rotate()
    house.translate()

    scaffold = o.scaffold()
    pc = scaffold.pointcloud_class
    bbox = scaffold.get_bbox()
#    scaffold.scale()
#    scaffold.rotate()
#    scaffold.translate()

    basement.add_element(scaffold)
    basement2 = Element(basement.wmeshes + container.wmeshes,'concat')
    
    
    saver = utils.ElementSaver(cdict,'data')
    saver.delete_files()
#    saver.save_as_pc(basement) 
#    saver.save_as_pc(container) 
#    saver.save_as_pc(house) 
    saver.save_as_pc(scaffold) 
    
#    saver.save_as_pc(basement2)
    print('stuff')











