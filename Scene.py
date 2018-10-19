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

uni = np.random.uniform
norma = np.random.normal
ar = np.array

origin, xaxis, yaxis, zaxis = [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]
axes = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

Classes = {'Basement':(0,1),'Container':(2),'Scaffold':(3),'House':(4,5),\
        'HouseWithScaffold':(4,5,3)}

def Transform(transl,scale,alpha):
   
    """    
    translationScalar = lambda:  np.random.uniform(0.1,0.8)
    scaleScalar  = list 
    alpha = float
    """
    S = np.diag(scale)
    T = trans.translation_matrix(transl)
    #Z = shear_matrix(beta, xaxis, origin, zaxis)
    R = trans.rotation_matrix(alpha,zaxis)
    
    M = trans.concatenate_matrices(R, S,T)
    return M


def BasementInit():
    basement =  o.Basement(Classes['Basement'])
#    T = np.diag([10,10,0.1,1])
#    [wmesh._mesh.apply_transform(T) for wmesh in basement]
    return basement

def ContainerInit():
    thickness = uni(0.05,0.15)
    transl = [uni(-5,5),uni(-5,5),1] 
    scale = [norma(0.25,0.15),norma(0.4,0.3),norma(0.4,0.1),1] 
    alpha = uni(0,360)

    container = o.Container(thickness,Classes['Container'])
    T = Transform(transl,scale,alpha)
    [wmesh._mesh.apply_transform(T) for wmesh in container]
    return container

def ScaffoldInit():
    thickness = uni(0.05,0.15)
    transl = [uni(-5,5),uni(-5,5),1] 
    scale = [norma(0.25,0.15),norma(0.4,0.3),norma(0.2,0.1),1] 
    alpha = uni(0,360)
    
    scaffold = o.Scaffold(thickness,Classes['Scaffold'])
    T = Transform(transl,scale,alpha)
    [wmesh._mesh.apply_transform(T) for wmesh in scaffold]
    return scaffold

def HouseInit():
    transl = [uni(-5,5),uni(-5,5),1] 
    scale = [norma(1.4,0.5),norma(1,0.3),norma(1,2),1] 
    alpha = uni(0,360)
    roofHeight = uni(0.7,0.8) 
    
    house = o.House(roofHeight,Classes['House'])
    T = Transform(transl,scale,alpha)
    [wmesh._mesh.apply_transform(T) for wmesh in house]
    return house

def HouseWithScaffoldInit():
    transl = [uni(-5,5),uni(-5,5),1] 
    scale = [norma(2,0.5),norma(1.8,0.3),norma(1,2),1] 
    alpha = uni(0,360)
    roofHeight = uni(0.7,0.8) 
    
    
    func = np.random.poisson(lam=1.22)
    lmb = lambda:  max(min(4, func), 1)
    reps = [lmb() for _ in range(3)]
    reps[0] = 1
    
    logger.info(' Scaffold Repititions: {}'.format(reps))
    width = np.random.uniform(0.1,0.3)
    hws = a.HouseWithScaffold(roofHeight,width,reps,Classes['House'])
    T = Transform(transl,scale,alpha)
    [wmesh._mesh.apply_transform(T) for wmesh in hws]
    return hws





def GenerateMeshes():

    logger = logging.getLogger('generator.Scene.GenerateMeshes')
    
    initFunc = [BasementInit,ContainerInit,ScaffoldInit,HouseInit,HouseWithScaffoldInit]

    objectCount = {func:np.random.randint(1,2) for func in initFunc} 
    nObj = sum(value for value in objectCount.values())
    
    for func in list(objectCount):
        logger.info('{}: {}'.format(func.__name__, objectCount[func]))
    
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
    utils.DelFilesInFolder('data')    

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('generator').setLevel(logging.INFO)
    logging.getLogger('trimesh').setLevel(logging.CRITICAL)

    
    wmeshlist = GenerateMeshes() 
    
    
    for wmesh in wmeshlist:
        wmesh.SavePCRGB(num=8000)
            
        


        













