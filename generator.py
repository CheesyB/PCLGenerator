#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ipdb
import numpy as np
import pymesh as pm


def returnHouse(pmin,pmax,roofheight):
    
    z = pmax[2] + pmax[2]*roofheight

    p0 = pmin + np.array([pmax[0]/2,0,0])
    p1 = pmin + np.array([pmax[0]/2,pmax[1],0])
    p2 = p0 + np.array([0,0,z])
    p3 = p1 + np.array([0,0,z])

    #ipdb.set_trace()
    # Wire mesh
    vertices = np.vstack((p0,p1,p2,p3))
    edges = np.array([[0,1],
                    [1,3],
                    [3,2],
                    [2,0]]) # scheiß Nummerierung 
    wire  = pm.wires.WireNetwork.create_from_data(vertices, edges)
    inflator = pm.wires.Inflator(wire)
    inflator.inflate(0.1, per_vertex_thickness=True)
    wiremesh = inflator.mesh


    boxmesh = pm.generate_box_mesh(pmin,pmax)



    union_mesh = pm.boolean(boxmesh, wiremesh, operation="union",engine="cgal")


    #ipdb.set_trace()

    mesh = pm.convex_hull(union_mesh)
    
    return mesh


def returnContainer(pmin,pmax,thickness):
    boxmesh = pm.generate_box_mesh(pmin,pmax)

    newMin = pmin + np.array([thickness,thickness,thickness])
    newMax = pmax - np.array([thickness,thickness,0])
    
    inner_boxmesh= pm.generate_box_mesh(newMin,newMax)

    union_mesh = pm.boolean(boxmesh, inner_boxmesh,'symmetric_difference',engine="cgal")
    
    return union_mesh



if(__name__=='__main__'):
    xmax = 1
    ymax = 5
    zmax = 1

    xmin = 0 
    ymin = 0
    zmin = 0 

    h = 0.3 
    
    pmax = np.array([xmax,ymax,zmax])
    pmin = np.array([xmin,ymin,zmin])
    
    #mesh = returnHouse(pmin,pmax,h) 
    mesh = returnContainer(pmin,pmax,0.1)
    pm.save_mesh('thing.ply',mesh)






