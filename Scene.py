#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import logging 
import Objects as o
import Assembler as a
import trimesh as tri
import trimesh.transformations as trans
import utils 

logger = logging.getLogger('generator.Scene')
logging.getLogger('generator').setLevel(logging.INFO)


origin, xaxis, yaxis, zaxis = [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]
axes = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

Classes = {'Basement':(0,1),'Container':(2),'Scaffold':(3),'House':(4,5),\
        'HouseWithScaffold':(4,5,3)}

def Transform():
    
    scaleScalar  = lambda : np.random.normal(1,0.5)  
    S = []
    for i in range(3):
        S.append(trans.scale_matrix(scaleScalar(), origin))
    
    S = np.linalg.multi_dot(S)

    transl = [np.random.uniform(0.1,0.8) for _ in range(3)]
    T = trans.translation_matrix(transl)
    
    #Z = shear_matrix(beta, xaxis, origin, zaxis)
    
    alpha = np.random.uniform(0,360)
    R = trans.rotation_matrix(alpha,zaxis)
    
    M = trans.concatenate_matrices(T, R, S)
    return M


def BasementInit():
    basement =  o.Basement(Classes['Basement'])
    T = np.diag([10,10,0.1,1])
    [wmesh._mesh.apply_transform(T) for wmesh in basement]
    return basement

def ContainerInit():
    thickness = np.random.uniform(0.1,0.2) 
    return o.Container(thickness,Classes['Container'])

def ScaffoldInit():
    thickness = np.random.uniform(0.1,0.2) 
    return o.Scaffold(thickness,Classes['Scaffold'])

def HouseInit():
    roofHeight = np.random.uniform(0.1,0.8) 
    return o.House(roofHeight,Classes['House'])

def HouseWithScaffoldInit():
    roofHeight = np.random.uniform(0.1,0.8) 
    func = np.random.poisson(lam=1)
    lmb = lambda:  max(min(4, func), 1)
    repititions = [lmb() for _ in range(3)]
    logger.info(' Scaffold Repititions: {}'.format(repititions))
    width = np.random.uniform(0.1,0.3)
    return a.HouseWithScaffold(roofHeight,width,repititions,Classes['House'])



def GenerateMeshes():

    logger = logging.getLogger('generator.Scene.GenerateMeshes')
    
    initFunc = [BasementInit,ContainerInit,ScaffoldInit,HouseInit,HouseWithScaffoldInit]

    objectCount = {func:np.random.randint(0,3) for func in initFunc} 
    nObj = sum(value for value in objectCount.values())
    logger.info('SceneDict: \n{}'.format(objectCount))
    
    objList = []

    for functionAsKey in initFunc:
        for i in range(objectCount[functionAsKey]):
            logger.info('[{}/{}] {}s created'.format(i+1,objectCount[functionAsKey],\
                    functionAsKey.__name__))
            
            meshlist = functionAsKey()
            assert(isinstance(meshlist,list)), 'The obj is of type: {}\
                    not list'.format(type(meshlist))
            for wmesh in meshlist:  
                assert(isinstance(wmesh,utils.WrapMesh)), 'The obj is of type: {}\
                        not WrapMesh'.format(type(wmesh))
            objList.extend(meshlist)
            logger.info(' {} wmeshes created'.format(len(objList)))

    return objList 



if __name__ == "__main__":
    utils.DelFilesInFolder(data)    
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('generator').setLevel(logging.INFO)
    logging.getLogger('trimesh').setLevel(logging.CRITICAL)

    M = Transform()
    
    wmeshlist = GenerateMeshes() 
    
    for wmesh in wmeshlist:
        T = Transform()
        wmesh._mesh.apply_transform(T)
        wmesh.SavePCRGB(num=8000)
            
        


        













