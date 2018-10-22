#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pa
import Objects as o
import trimesh as tri 
import Element as ele
import utils 
import logging




""" gibt das Gerüst immer im Eiheitswürfel zurück 
    scaffolds type => List<WrapMesh> 
    Class type => int               """
def scaffold_factory(reps=None):
    if reps is None:
        func = np.random.poisson(lam=1.82)
        lmb = lambda:  max(min(4, func), 1)
        reps = [lmb() for _ in range(3)]
        reps[0] = 1
    
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
                tmp = o.scaffold()
                tmp.transform(mat) 
                tmp._prefix = 'hws_{}th'.format(count)
                scaffolds.extend(tmp)
    
    
    logger.info('total of {} scaffolds created'.format(n)) 
    scaffold = ele.Element(scaffolds[0],'scaffols',meshlist=scaffolds[1:]) 
    T.toc() 
    return scaffold


""" Classes[0] = roof; Classes[1] = body; Classes[2] = scaffold """

def hws(roofHeight,width,reps,Classes):
    
    logger = logging.getLogger('generator.Assembler.HouseWithScaffold')
    T = utils.TicToc(logger)
     
    house = po.House(roofHeight,Classes[:2]) # returns (roof,mesh)
    house[0]._prefix = 'hws_'
    house[1]._prefix = 'hws_'
    
    transl = (1+width,0,0) 
    transf = np.diag([1*0.25,1,1,1])
    
    scaffolds = ScaffoldFactory(reps)
    for wmesh in scaffolds:
        wmesh._mesh.apply_transform(transf)
        wmesh._mesh.apply_translation(transl)
    scaffolds.extend(house)
    T.toc() 
    return scaffolds 

def scaffold_test(width,reps):
    
    logger = logging.getLogger('generator.Assembler.ScaffoldTest')
    T = utils.TicToc(logger)
     
    
    transl = (1+width,0,0) 
    transf = np.diag([1*0.25,1,1,1])
    
    scaffolds = ScaffoldFactory(reps,None)
    T.toc() 
    return scaffolds 


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    logging.getLogger('generator').setLevel(logging.INFO)
    logging.getLogger('trimesh').setLevel(logging.CRITICAL)    

    cdict = {'basement_up':(1,0,0),
            'basement_low':(0,1,0),
            'roof':(1,1,0),
            'body':(1,0,1),
            'container':(0,1,1),
            'scaffold':(0.5,0.5,0.5)}
    
    saver =  utils.ElementSaver(cdict, 'data')
    saver.delete_files()

    ele = scaffold_factory()
    saver.save_as_pc(ele)

#    wmeshlist = HouseWithScaffold(0.7,0.1,[2,2,2],(10,20,None))
#
#    i = 0
#    for wmesh in wmeshlist:
#        i += 1
#        logging.debug(' {} mesh'.format(i))
#        wmesh._prefix = '{}_Regular_'.format(i)
#        wmesh.SavePCRGB()





















