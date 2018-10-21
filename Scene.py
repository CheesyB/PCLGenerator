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


Classes = {'Basement':(0,10),'Container':(16),'Scaffold':(35),'House':(40,50),\
        'HouseWithScaffold':(40,50,30)}

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
    
    #return np.eye(4) 
    return [S,R,T] # Rotationmatix macht Häuser kopfstehend


def BasementInit():
    basement =  o.Basement(Classes['Basement'])
    T = np.diag([8,8,0.1,1])
    [wmesh.Transform([T]) for wmesh in basement]
    return basement

def ContainerInit():
    thickness = uni(0.05,0.05)
    transl = [uni(-1,1),uni(-1,1),0] 
    scale = [norma(0.2,0.15),norma(0.4,0.1),norma(0.3,0.1),1] 
    alpha = uni(0,360)

    container = o.Container(thickness,Classes['Container'])
    T = Transform(transl,scale,alpha)
    [wmesh.Transform(T) for wmesh in container]
    return container

def ScaffoldInit():
    thickness = uni(0.05,0.15)
    transl = [uni(-1,1),uni(-1,1),0] 
    scale = [norma(0.35,0.15),norma(0.4,0.1),norma(0.4,0.1),1] 
    alpha = uni(0,360)
    
    scaffold = o.Scaffold(thickness,Classes['Scaffold'])
    T = Transform(transl,scale,alpha)
    [wmesh.Transform(T) for wmesh in scaffold]
    return scaffold

def HouseInit():
    transl = [uni(-1,1),uni(-1,1),0] 
    scale = [norma(1.4,0.1),norma(0.8,0.1),norma(1,0.3),1] 
    alpha = uni(0,360)
    roofHeight = uni(0.7,0.8) 
    
    house = o.House(roofHeight,Classes['House'])
    T = Transform(transl,scale,alpha)
    [wmesh.Transform(T) for wmesh in house]
    return house

def HouseWithScaffoldInit():
    transl = [uni(-1,1),uni(-1,1),0] 
    scale = [norma(1,0.2),norma(1.8,0.1),norma(1,0.2),1] 
    alpha = uni(0,360)
    roofHeight = uni(0.7,0.8) 
    
    
    func = np.random.poisson(lam=1.82)
    lmb = lambda:  max(min(4, func), 1)
    reps = [lmb() for _ in range(3)]
    reps[0] = 1
    
    logger.info(' Scaffold Repititions: {}'.format(reps))
    width = np.random.uniform(0.1,0.3)
    hws = a.HouseWithScaffold(roofHeight,width,reps,Classes['House'])
    T = Transform(transl,scale,alpha)
    [wmesh.Transform(T) for wmesh in hws]
    return hws





def GenerateMeshes():

    logger = logging.getLogger('generator.Scene.GenerateMeshes')
    
    initFunc = [BasementInit,ContainerInit,ScaffoldInit,HouseInit,HouseWithScaffoldInit]

    objectCount = {func:np.random.randint(1,6) for func in initFunc} 
    nObj = sum(value for value in objectCount.values())
    
    for func in list(objectCount):
        logger.info('{}: {}'.format(func.__name__, objectCount[func]))
    
    elementList = []
    for functionAsKey in initFunc:
        for i in range(objectCount[functionAsKey]):
            colMan = tri.collision.CollisionManager()
            while(True): 
                meshlist = functionAsKey()
                for wmesh in meshlist:
                    wmesh._prefix = str(i) + wmesh._prefix 
                assert(isinstance(meshlist,list)), 'The obj is of type: {}\
                        not list'.format(type(meshlist))
                for wmesh in meshlist:  
                    assert(isinstance(wmesh,utils.WrapMesh)), 'The obj is of type: {}\
                            not WrapMesh'.format(type(wmesh))
                for wmesh in meshlist:
                    colMan.add_object(wmesh.name,wmesh._mesh)
                    if colMan.in_collision_internal():
                        logger.warning(' collision detected,'+ 
                                'recreating {}'.format(functionAsKey.__name__))
                        colMan.remove_object(wmesh.name)
                        continue
                elementList.extend(meshlist)
                break

            logger.info('[{}/{}] {}s created'.format(i+1,objectCount[functionAsKey],\
                    functionAsKey.__name__))
            logger.info(' {} wmeshes created'.format(len(elementList)))

    return elementList 



if __name__ == "__main__":
    utils.DelFilesInFolder('data')    

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('generator').setLevel(logging.INFO)
    logging.getLogger('trimesh').setLevel(logging.CRITICAL)

    
    wmeshlist = GenerateMeshes()
    #wmeshlist = HouseInit()
     
    
    for wmesh in wmeshlist:
        logger.info('name: {}'.format(wmesh.name))
        wmesh.SavePCRGB(num=8000)
            
        


        













