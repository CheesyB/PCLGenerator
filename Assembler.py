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
    
    scaling = [1/reps[0],1/reps[1],1/reps[2],1]
    dx = scaling[0]
    dy = scaling[1]
    dz = scaling[2]
    count = 0 

    for i in range(reps[0]):
        for j in range(reps[1]):
            for k in range(reps[2]):
                count += 1
                x =  i*dx
                y =  j*dy 
                z =  k*dz
             
                tmp = o.scaffold()
                tmp.scale(scaling)
                tmp.translate([x,y,z]) 
                tmp.wmeshes[0].prefix = 'hws_{}th'.format(count)
                mesh = tmp.wmeshes
                scaffolds.extend(mesh)
    
    
    logger.info('total of {} scaffolds created'.format(n)) 

    scaffold = ele.Element(scaffolds,'scaffols') 
    center = scaffold.entire_mesh.center_mass
    center[2] = 0
    scaffold.translate(-center)

    T.toc() 
    return scaffold


""" Classes[0] = roof; Classes[1] = body; Classes[2] = scaffold """

def hws():
    
    logger = logging.getLogger('generator.Assembler.HouseWithScaffold')
    T = utils.TicToc(logger)
     
    hws = o.house() # returns (roof,mesh)
    hws.wmeshes[0]._prefix = 'hws_'
    hws.wmeshes[1]._prefix = 'hws_'
    
    width = 0.01
    transl = (1+width,0,0) 
    scale = [1*0.25,1,1,1]
    
    scaffolds = scaffold_factory()
    scaffolds.scale(scale)
    scaffolds.translate(transl)
    
    hws.add_element(scaffolds)

    T.toc() 
    return hws

def scaffold_test(width,reps):
    
    logger = logging.getLogger('generator.Assembler.ScaffoldTest')
    T = utils.TicToc(logger)
     
    
    transl = (1+width,0,0) 
    transf = np.diag([1*0.25,1,1,1])
    
    scaffolds = ScaffoldFactory(reps,None)
    T.toc() 
    return scaffolds 


if __name__ == "__main__":
    test()


def test():
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('generator').setLevel(logging.INFO)
    logging.getLogger('trimesh').setLevel(logging.CRITICAL)    

    cdict = {'basement_up':(1,0,0),
            'basement_low':(0,1,0),
            'roof':(1,1,0),
            'body':(1,0,1),
            'container':(0,1,1),
            'scaffold':(0.5,1,0.5)}
    
    saver =  utils.ElementSaver(cdict, 'data')
    saver.delete_files()

    sf = scaffold_factory()
    saver.save_as_pc(sf)
    
    myhws = hws()
    saver.save_as_pc(myhws)






