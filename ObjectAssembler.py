#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pa
import PlyObjects as po
import trimesh as tri 
import utils 
import logging

# house = trimesh, normal = orientation of the scaffold, w|h|l dims of one scaffold
# reps= (repitition in x, repition in y)

#def AddScaffold(house,normal,gap,witdh,height,length,reps):
#    obb = house.bounding_box_oriented
#    pmin = obb.vertices.argmin(0)
#    pmax = obb.verices.argmax(0)
#    
#    for i in range(reps[0]):
#        for j in range(reps[1]):
            


""" gibt das Gerüst immer im Eiheitswürfel zurück """         
def ScaffoldFactory(reps):
    
    T = utils.TicToc('ScaffoldFactory')
    n = reps[0]*reps[1]*reps[2]
    logging.debug('total of {} scaffolds created'.format(n)) 
    
    scaling = np.diag([1/reps[0],1/reps[1],1/reps[2],1])
    dx = scaling[0][0]
    dy = scaling[1][1]
    dz = scaling[2][2]
    
    scaffold = po.Scaffold(0.1)
    scaffolds = [] 
    for i in range(reps[0]):
        for j in range(reps[1]):
            for k in range(reps[2]):
                x = i*dx
                y = j*dy 
                z = k*dz
                translation = np.array([[1,0,0,x],
                                        [0,1,0,y],
                                        [0,0,1,z],
                                        [0,0,0,1]])
                mat = translation.dot(scaling)
                tmp = scaffold.ReturnUnitScaffold()
                tmp.apply_transform(mat)
                scaffolds.append(tmp)
    
    scaffolds = tri.util.concatenate(scaffolds)
    T.toc() 
    return scaffolds 


def UniformHouse():
    pmin = np.array([0,0,0])
    pmax = np.array([1,1,1])

    house = po.House(pmin,pmax,0.2,[0,1])
    return house.ReturnHouse()

def HouseWithScaffold(pmin,pmax,reps):
    
    house = po.House(pmin,pmax,0.5,[0,1])
    housemesh = house.ReturnHouse(roofHeight=2)
    transl = (1.1,0,0) 
    transf = np.diag([1*0.25,1,1,1])
    
    scaffold = ScaffoldFactory(reps)
    scaffold.apply_transform(transf)
    scaffold.apply_translation(transl)

    ScafHouse = tri.util.concatenate(housemesh,scaffold)
    return ScafHouse




if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    pmin = np.array([0,0,0])
    pmax = np.array([1,1,1])
    
#    Scaffold = ScaffoldFactory(pmin,pmax,[1,4,3])
#    scPointCloud = utils.SamplePointCloud(Scaffold,20000)
#    scPointCloud.to_file('data/pcScaffoldArray.ply')
#    utils.SavePly('plyScaffoldsArray',Scaffold)
    
    ScafHouse = HouseWithScaffold(pmin,pmax,[1,2,4])
    scScafHouse = utils.SamplePointCloud(ScafHouse,40000)
    scScafHouse.to_file('data/scScafHouse.ply')
    utils.SavePly('plyScafHouse',ScafHouse)

    house = UniformHouse()
    utils.SavePly('plyHouse',house)




















