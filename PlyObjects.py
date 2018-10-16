#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pymesh as pm
import trimesh as tri
import pyntcloud as pc
import utils
import pandas as pa
import logging



class Basement(object):

    """Docstring for Basement. """

    def __init__(self,scaling):
        """Nothing

        :scaling: TODO

        """
        self._scaling = scaling
    
    def ReturnBasement(self,scaling = None):
        if(scaling == None): scaling = self._scaling
        trans = np.diag(scaling) 
        box = tri.creation.box()
        box.apply_transform(trans)
        return box 

    def SamplePointCloud(self,num=10000,scaling = None):
        T = utils.TicToc('SampelPoints from Basement')
        npPoints,_ = tri.sample.sample_surface_even(self.ReturnBasement(scaling), num)
        # evaluate lambda with extra parenthesis, put it in extra braces to add dimension
        npClass = np.array([[(lambda x: 1 if x > 0 else 0)(x) 
            for x in npPoints[:,2]]])
        npPoints = np.concatenate((npPoints,npClass.T), axis=1) #Transpose to fit the dims
        paPoints = pa.DataFrame(columns=['x','y','z','class'],data=npPoints)
        pointcloud = pc.PyntCloud(paPoints)
        T.toc()
        return pointcloud 

class Container(object):

    """Docstring for Container. """

    def __init__(self,pmin,pmax,thickness):
        """TODO: to be defined1.

        :pmin: TODO
        :pmax: TODO
        :thickness: TODO

        """
        self._pmin = pmin
        self._pmax = pmax
        self._thickness = thickness
        
    
    def ReturnContainer(self):
        T=utils.TicToc('ReturnContainer')
        logging.debug('Obacht mit der thickenss, kann zu gross sein')
        #Big box minus smaller box inside equals simple container
        boxmesh = pm.generate_box_mesh(self._pmin,self._pmax)

        newMin = pmin + np.array([self._thickness,self._thickness,self._thickness])
        newMax = pmax - np.array([self._thickness,self._thickness,0])
        
        inner_boxmesh= pm.generate_box_mesh(newMin,newMax)

        union_mesh = pm.boolean(boxmesh, inner_boxmesh,'symmetric_difference',engine="cgal")
        union_mesh = utils.PyMesh2Ply(union_mesh)
        T.toc()
        return union_mesh
    
    def SamplePointCloud(self,num=10000,Class=1):
        T = utils.TicToc('SampelPoints from Container')
        container = self.ReturnContainer()
        npPoints,_ = tri.sample.sample_surface_even(container, num)
        # evaluate lambda with extra parenthesis, put it in extra braces to add dimension
        npClass = np.ones((npPoints.shape[0],1)) * Class
        
        npPoints = np.concatenate((npPoints,npClass), axis=1) #Transpose to fit the dims
        paPoints = pa.DataFrame(columns=['x','y','z','class'],data=npPoints)
        pointcloud = pc.PyntCloud(paPoints)
        T.toc()
        return pointcloud 


class Scaffold(object):

    """Docstring for Scaffold. """

    def __init__(self,pmin,pmax,thickenss):
        """TODO: to be defined1.

        :pmin: TODO
        :pax: TODO

        """
        self._pmin = pmin
        self._pmax = pmax
        self._thickness = thickness
        


    def ReturnScaffold(self):
        T=utils.TicToc('ReturnScaffold')
        pmin = self._pmin
        pmax = self._pmax

        p0 = pmin 
        p1 = pmin + np.array([0,0,pmax[2]])
        p2 = pmin + np.array([pmax[0],0,pmax[2]])
        p3 = pmin + np.array([pmax[0],0,0])
       
        y = np.array([0,pmax[1],0])
        p4 = p0 + y
        p5 = p1 + y
        p6 = p2 + y 
        p7 = p3 + y 

        vertices = np.vstack((p0,p1,p2,p3,p4,p5,p6,p7))
        edges = np.array([[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4], 
                            [0,2],[1,3],[4,6],[5,7],
                            [0,4],[1,5],[2,6],[3,7],
                            [0,5],[2,7]])
        wire  = pm.wires.WireNetwork.create_from_data(vertices, edges)
        
        inflator = pm.wires.Inflator(wire)
        inflator.inflate(self._thickness, per_vertex_thickness=False)
        scaffold = inflator.mesh

        scaffold = utils.PyMesh2Ply(scaffold)
        T.toc()
        return scaffold

    def SamplePointCloud(self,num=10000,Class=2):
        T = utils.TicToc('SampelPoints from Scaffold')
        scaffold = self.ReturnScaffold()
        npPoints,_ = tri.sample.sample_surface_even(scaffold, num)
        # evaluate lambda with extra parenthesis, put it in extra braces to add dimension
        npClass = np.ones((npPoints.shape[0],1)) * Class
        
        npPoints = np.concatenate((npPoints,npClass), axis=1) #Transpose to fit the dims
        paPoints = pa.DataFrame(columns=['x','y','z','class'],data=npPoints)
        pointcloud = pc.PyntCloud(paPoints)
        T.toc()
        return pointcloud 


class House(object):

    """Docstring for house. """

    def __init__(self,pmin,pmax,roofHeight,classes):
        """TODO: to be defined1.

        :pmin: TODO
        :pmax: TODO
        :roofHeight: TODO

        """
        self._pmin = pmin
        self._pmax = pmax
        self._roofHeight = roofHeight
        self._class = classes
        


    """ Returns np.Array where the points describe a box """
    def BboxCornerPoints(self,pmin,pmax):
        T=utils.TicToc('BoxCornerPoints')
        #cube
        x = pmin[0]
        y = pmin[1]
        z = pmin[2]

        X = pmax[0]
        Y = pmax[1]
        Z = pmax[2]

        p0 = pmin
        p1 = np.array([X,y,z])
        p2 = np.array([X,Y,z])
        p3 = np.array([x,Y,z])
        p4 = np.array([x,y,Z])
        p5 = np.array([X,y,Z])
        p6 = pmax
        p7 = np.array([x,Y,Z])
        
        T.toc()
        
        return  np.vstack((p0,p1,p2,p3,p4,p5,p6,p7))

    
    def ReturnHouse(self,pmin = None, pmax = None,roofHeight = None):
        T = utils.TicToc('House')
        if(pmin == None): pmin = self._pmin
        if(pmax == None): pmax = self._pmax
        if(roofHeight == None): roofHeight = self._roofHeight
        
        vertices = self.BboxCornerPoints(pmin,pmax)
        
        width = pmax[0]-pmin[0]
        length = pmax[1]-pmin[0]
        height = pmax[2]-pmin[2]
        
        p8 = pmin + np.array([width/2,0,height+roofHeight])
        p9 = pmin + np.array([width/2,length,height+roofHeight])

        vertices = np.vstack((vertices,p8,p9))

        #from scipy gives back ConvecHull as nx3 array where each column represents a vertex
        tmpMesh = tri.Trimesh(vertices)
        hull = tmpMesh.convex_hull

        house = tri.Trimesh(hull.vertices.copy(),hull.faces.copy())

        T.toc() 
        return house
   
    def SamplePointCloud(self,num=10000):
        T = utils.TicToc('SampelPoints from Basement')
        
        npPoints,_ = tri.sample.sample_surface_even(self.ReturnHouse(), num)
        
        lmb = lambda x: self._class[0] if x > self._pmax[2]  else self._class[1]
        # Put it in extra braces to add dimension
        npClass = np.array([[lmb(x) for x in npPoints[:,2]]])
        
        npPoints = np.concatenate((npPoints,npClass.T), axis=1) #Transpose to fit the dims
        paPoints = pa.DataFrame(columns=['x','y','z','class'],data=npPoints)
        pointcloud = pc.PyntCloud(paPoints)
        T.toc()
        return pointcloud 
   




if __name__ == "__main__":
    print('Test started')
    logging.basicConfig(level=logging.DEBUG)
    T=utils.TicToc('Total')
    xmax = 1
    ymax = 5
    zmax = 1

    xmin = 0 
    ymin = 0
    zmin = 0 

    roofHeight = 1 
    thickness = 0.1
    
    pmax = np.array([xmax,ymax,zmax])
    pmin = np.array([xmin,ymin,zmin])
    

    houseClasses = [0,1]
    house = House(pmin, pmax, roofHeight,houseClasses)
    houseCloud = house.SamplePointCloud()
    houseCloud.to_file('data/pcHouse.ply') 
    utils.SavePly('plyHouse',house.ReturnHouse())

    
    scaffold = Scaffold(pmin,pmax,thickness)
    ScaffoldCloud = scaffold.SamplePointCloud()
    ScaffoldCloud.to_file('data/pcScaffold.ply') 
    utils.SavePly('plyScaffold',scaffold.ReturnScaffold())
    

    scaling = np.array([10,10,0.1,1])
    basement = Basement(scaling)
    BasementCloud= basement.SamplePointCloud()
    BasementCloud.to_file('data/pcBasementWithClass.ply')
    utils.SavePly('plyBasement',basement.ReturnBasement())


    container = Container(pmin,pmax,thickness)
    ContainerCloud = container.SamplePointCloud()
    ContainerCloud.to_file('data/pcContainerWithClass.ply')
    utils.SavePly('plyContainer',container.ReturnContainer())


#    totalCloud = utils.SamplePointCloud(totalMesh,10000)
#    totalCloud.to_file('data/pcTotal.ply')
    T.toc()






