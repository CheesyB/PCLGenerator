#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pa
import Objects as po
import trimesh as tri 
import utils 
import logging




""" gibt das Gerüst immer im Eiheitswürfel zurück 
    scaffolds type => List<WrapMesh> 
    Class type => int               """
def ScaffoldFactory(reps,Class=None):
    logger = logging.getLogger('generator.Assembler.ScaffoldFactory')
    T = utils.TicToc(logger)
     
    n = reps[0]*reps[1]*reps[2]
    
    scaffolds = []
    thickness = 0.1
    
    scaling = np.diag([1/reps[0],1/reps[1],1/reps[2],1])
    dx = scaling[0][0]
    dy = scaling[1][1]
    dz = scaling[2][2]
    count = 0 

    for i in range(reps[0]):
        for j in range(reps[1]):
            for k in range(reps[2]):
                count += 1
                x = i*dx
                y = j*dy 
                z = k*dz
                translation = np.array([[1,0,0,x],
                                        [0,1,0,y],
                                        [0,0,1,z],
                                        [0,0,0,1]])
                mat = translation.dot(scaling)
                if Class is None:
                    theClass = 40+count
                    tmp = po.Scaffold(thickness,theClass)
                    logger.info('Random Class {} added to wmesh: {}'.format(theClass,tmp[0].name))
                else:
                    tmp = po.Scaffold(thickness,Class) 
                    logger.debug('Class {} added to wmesh: {}'.format(Class,tmp[0].name))

                tmp[0]._mesh.apply_transform(mat) 
                tmp[0]._prefix = 'hws_{}th'.format(count)
                scaffolds.extend(tmp)
    
    
    logger.info('total of {} scaffolds created'.format(n)) 
    T.toc() 
    return scaffolds 


""" Classes[0] = roof; Classes[1] = body; Classes[2] = scaffold """

def HouseWithScaffold(roofHeight,width,reps,Classes):
    
    logger = logging.getLogger('generator.Assembler.HouseWithScaffold')
    T = utils.TicToc(logger)
     
    house = po.House(roofHeight,Classes[:2]) # returns (roof,mesh)
    house[0]._prefix = 'hws_'
    house[1]._prefix = 'hws_'
    
    transl = (1+width,0,0) 
    transf = np.diag([1*0.25,1,1,1])
    
    scaffolds = ScaffoldFactory(reps,None)
    for wmesh in scaffolds:
        wmesh._mesh.apply_transform(transf)
        wmesh._mesh.apply_translation(transl)
    scaffolds.extend(house)
    T.toc() 
    return scaffolds 

def ScaffoldTest(width,reps):
    
    logger = logging.getLogger('generator.Assembler.ScaffoldTest')
    T = utils.TicToc(logger)
     
    
    transl = (1+width,0,0) 
    transf = np.diag([1*0.25,1,1,1])
    
    scaffolds = ScaffoldFactory(reps,None)
    for wmesh in scaffolds:
        wmesh._mesh.apply_transform(transf)
        wmesh._mesh.apply_translation(transl)
    T.toc() 
    return scaffolds 


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    logging.getLogger('generator').setLevel(logging.INFO)
    logging.getLogger('utils.PyMesh2Ply').setLevel(logging.CRITICAL)    
    logging.getLogger('trimesh').setLevel(logging.CRITICAL)    
    logging.getLogger('utils.TicToc').setLevel(logging.CRITICAL)    

    utils.DelFilesInFolder('data')
    
#    wmeshlist = ScaffoldFactory([2,3,3])
#    scaffold.SaveMesh()
#    scaffold.SavePC()
    
#    wmeshlist(0.1,[2,2,2])

    wmeshlist = HouseWithScaffold(0.7,0.1,[2,2,2],(10,20,None))

    i = 0
    for wmesh in wmeshlist:
        i += 1
        logging.debug(' {} mesh'.format(i))
        wmesh._prefix = '{}_Regular_'.format(i)
        wmesh.SavePCRGB()





















