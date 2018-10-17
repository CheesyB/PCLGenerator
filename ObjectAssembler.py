#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pa
import PlyObjects as po
import trimesh as tri 
import utils 
import logging



""" gibt das Gerüst immer im Eiheitswürfel zurück """         
def ScaffoldFactory(reps):
    
    T = utils.TicToc('ScaffoldFactory')
    n = reps[0]*reps[1]*reps[2]
    logging.debug('total of {} scaffolds created'.format(n)) 
    
    scaffolds = []
    thickness = 0.1
    Class = 0
    
    scaling = np.diag([1/reps[0],1/reps[1],1/reps[2],1])
    dx = scaling[0][0]
    dy = scaling[1][1]
    dz = scaling[2][2]
    
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
                tmp = po.Scaffold(thickness,1)
                tmp._mesh.apply_transform(mat) 
                scaffolds.append(tmp)
    
    meshlist = [x._mesh for x in scaffolds]
    TotalScaffoldMesh = tri.util.concatenate(meshlist)
    TotalScaffoldWrap = utils.WrapMesh('TotalScaffold', TotalScaffoldMesh,1)
    
    T.toc() 
    return TotalScaffoldWrap 


""" Classes[0] = roof; Classes[1] = body; Classes[2] = scaffold """

def HouseWithScaffold(roofHeight,width,reps,Classes):
     
    house = po.House(roofHeight,Classes[:2])
    
    transl = (1+width,0,0) 
    transf = np.diag([1*0.25,1,1,1])
    
    scaffold = ScaffoldFactory(reps)
    scaffold._mesh.apply_transform(transf)
    scaffold._mesh.apply_translation(transl)
    housemesh = [x._mesh for x in house]
    SH = tri.util.concatenate(housemesh,scaffold._mesh)
    wrapMesh = utils.WrapMesh('Scaffold on House', SH, 1)
    return wrapMesh 




if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    
#    scaffold = ScaffoldFactory([2,3,3])
#    scaffold.SaveMesh()
#    scaffold.SavePC()
#    
    ScafHouse = HouseWithScaffold(0.1,0.1,[1,2,4],(1,2,3))
    ScafHouse.SaveMesh()
    ScafHouse.SavePC()





















