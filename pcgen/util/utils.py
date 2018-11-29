#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import trimesh as tri
import numpy as np
import pandas as pa
import pyntcloud as pc
import os.path 
from .tictoc import TicToc
import ipdb

def PyMesh2Ply(target):
    logger = logging.getLogger('pcgen.'+__name__+'.PyMesh2Ply')
    T=TicToc(logger)
    plymesh = tri.Trimesh(target.vertices.copy(),target.faces.copy()) 
    T.toc()
    return plymesh

def SavePly(name,mesh):
        with open('data/{}.ply'.format(name),'wb') as f:
            byts = tri.io.ply.export_ply(mesh) 
            f.write(byts)
            

def SamplePointCloud(mesh,num):
    logger = logging.getLogger('pcgen.'+__name__+'.SamplePointCloud')
    T=TicToc(logger)
    npPoints,_ = tri.sample.sample_surface_even(mesh, num)
    paPoints = pa.DataFrame(columns=['x','y','z'],data=npPoints)
    pointcloud = pc.PyntCloud(paPoints)
    T.toc()
    return pointcloud 


def save_pointcloud_color(points,data_path,color_func=None):
    
    def get_color(val):
        val = int(val)
        color = np.array([0.82 * val % 1,
                          0.33 * val % 1,
                          0.55 * val % 1])
        return color
    if color_func is not None:
        get_color = color_func

    """ we need special treatment when the data is from the dataloader """
    if type(points) is tuple:
        points = np.concatenate((points[0],np.expand_dims(points[1],axis=1)),axis=1)
 
    
    assert points.shape[1] is 4, 'Shape komisch' 
    if(points.shape[0] is 0):
        print('no points in cloud.. normal?')
        return None
    class_points = np.array([get_color(class_number) for class_number in points[:,3]])
    points = points[:,:3]    # drop the class_number and add color
    points = np.concatenate((points,class_points), axis=1)

    dataframe = pa.DataFrame(columns=['x','y','z','red','green','blue'],data=points)
    pyntcloud = pc.PyntCloud(dataframe)
    if data_path is not None:   
        pyntcloud.to_file(data_path)
    return pyntcloud


def render_batch(batch_points,batch_pred,folder_path):
    
    """ we need special treatment when the data is from the dataloader """
    if not os.path.isdir(folder_path):
        raise Exception('This is not a folder path')
    
    if not isinstance(batch_points,np.ndarray) and not isinstance(batch_pred,np.ndarray):
        raise Exception('Hoops, I expected numpy arrays got {} '
                            ' and {}'.format(type(batch_points),type(batch_pred)))
    batch_pred = batch_pred.reshape(batch_points.shape[0],batch_points.shape[1])
    batch_pred.astype(np.int16)
    
    for idx in range(batch_points.shape[0]):
        points = batch_points[idx,:,:]
        pred = batch_pred[idx,:]
        data_path = folder_path + '/slice{}.ply'.format(idx)
        save_pointcloud_color((points, pred), data_path)

    
def render_batch_bool(batch_points,batch_pred,batch_target,folder_path):
    
    # oh weh dont compare floats:)
    def get_color(val): 
        color = {1.0:[1,0,0], #red 
                 0.0:[0,1,0]} #green
        return color[val]

    """ we need special treatment when the data is from the dataloader """
    if not os.path.isdir(folder_path):
        raise Exception('This is not a folder path')
    
    if not isinstance(batch_points,np.ndarray) and not isinstance(batch_pred,np.ndarray):
        raise Exception('Hoops, I expected numpy arrays got {} '
                            ' and {}'.format(type(batch_points),type(batch_pred)))
   
    batch_target = batch_target.flatten()
    batch_bool = np.equal(batch_pred,batch_target)
    batch_bool = batch_bool.reshape(batch_points.shape[0],batch_points.shape[1])
    batch_bool.astype(np.int16)
    
    for idx in range(batch_points.shape[0]):
        points = batch_points[idx,:,:]
        one_batch_bool = batch_bool[idx,:]
        data_path = folder_path + '/bool_slice{}.ply'.format(idx)
        save_pointcloud_color((points, one_batch_bool), data_path, get_color)

        


