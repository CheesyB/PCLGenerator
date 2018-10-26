#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pymesh as pm
import trimesh as tri
import simples.wrapmesh as wm
import simples.element as ele
from simples.tictoc import TicToc
from simples.utils import PyMesh2Ply
import logging



class ElementFactory(object):

    """Docstring for ObjectFactory. """
    class_dict = {'basement_up':0,
            'basement_low':1,
            'roof':2,
            'body':3,
            'container':4,
            'scaffold':5}

    def __init__(self,roof_height,classdict=None):
        """This Class is creates simple objects with their center 
            in the origin.
            Every object is returned as an Element holding one or 
            more WrapMesh objects        

        :classdict: maps the classe names to their corresponding 
                    class value(int)

        """
        self._class_dict = classdict
        if self._class_dict is None: 
            self._class_dict = ElementFactory.class_dict
        self._roof_heigt = roof_height 

    @staticmethod
    def get_class_names():
        return ['basement_low','basement_up','container','scaffold','roof','body']

    
    """ returns two CustoMeshes """

    def basement(self):
        logger = logging.getLogger('generator.'+__name__+'.Basement')
        T=TicToc(logger)

        box = tri.creation.box()
        normal = np.array([0,0,1])
        origin = np.array([0,0,0])
        
        upper = tri.intersections.slice_mesh_plane(box,normal,origin)
        num = self._class_dict['basement_up']
        upperMesh = wm.WrapMesh(upper,num,'basement_up')
        
        lower = tri.intersections.slice_mesh_plane(box,-normal,origin)
        num = self._class_dict['basement_low']
        lowerMesh = wm.WrapMesh(lower,num,'basement_low')
        element = ele.Element([upperMesh,lowerMesh],'first_ele')
        return element 


        
    """ return one WrapMesh  """

    def container(self):
        thickness = 0.1
        logger = logging.getLogger('generator.'+__name__+'.Container')
        T=TicToc(logger)
        
        #Big box minus smaller box inside equals simple container
        pmin = np.array([-0.5,-0.5,-0.5])
        pmax = np.array([0.5,0.5,0.5])
        boxmesh = pm.generate_box_mesh(pmin,pmax)

        newMin = pmin + np.array([thickness,thickness,thickness])
        newMax = pmax - np.array([thickness,thickness,0])
        
        inner_boxmesh= pm.generate_box_mesh(newMin,newMax)

        union_mesh = pm.boolean(boxmesh, inner_boxmesh,'symmetric_difference',engine="cgal")
        union_mesh = PyMesh2Ply(union_mesh)
        
        num = self._class_dict['container']
        mesh = wm.WrapMesh(union_mesh,num,'container')

        element = ele.Element([mesh],'container_ele') 
        T.toc()
        return element 
        

    """ needs two classes """

    def house(self):
        if self.roofHeight is None:
            roofHeight = np.random.rand()
        logger = logging.getLogger('generator.'+__name__+'.House')
        T=TicToc(logger)
        
        pmin = np.array([-0.5,-0.5,0])
        pmax = np.array([0.5,0.5,1])


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
        
        vertices = np.vstack((p0,p1,p2,p3,p4,p5,p6,p7)) 
        hull = tri.convex.convex_hull(vertices)

        body = tri.Trimesh(vertices=hull.vertices,faces=hull.faces)
        num = self._class_dict['body']
        bodymesh = wm.WrapMesh(body,num,'body')
        
        
        
        
        p8 = pmin + np.array([1/2,0,1+self.roofHeight])
        p9 = pmin + np.array([1/2,1,1+self.roofHeight])
        
        vertices = np.vstack((p4,p5,p6,p7,p8,p9))
        hull = tri.convex.convex_hull(vertices)
        
        roof = tri.Trimesh(vertices=hull.vertices,faces=hull.faces)
        num = self._class_dict['roof']
        roofmesh = wm.WrapMesh(roof,'roof')
        
        meshes = list((roofmesh,bodymesh)) 
        element = ele.Element(meshes,'house_ele') 
        
        T.toc() 
        return element 
   
    
    def _one_scaffold(self):
        thickness = 0.1
        logger = logging.getLogger('generator.'+__name__+'._one_scaffold')
        T=TicToc(logger)
        
        p0 = np.array([-0.5,-0.5,0])
        p1 = np.array([0.5,-0.5,0])
        p2 = np.array([0.5,0.5,0])
        p3 = np.array([-0.5,0.5,0])
        
        p4 = np.array([-0.5,-0.5,1])
        p5 = np.array([0.5,-0.5,1])
        p6 = np.array([0.5,0.5,1])
        p7 = np.array([-0.5,0.5,1])
        
        vertices = np.vstack((p0,p1,p2,p3,p4,p5,p6,p7))
        edges = np.array([[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4], 
                            [0,2],[1,3],[4,6],[5,7],
                            [0,4],[1,5],[2,6],[3,7],
                            [0,5],[2,7]])
        
        wire  = pm.wires.WireNetwork.create_from_data(vertices, edges)
        
        inflator = pm.wires.Inflator(wire)
        inflator.inflate(thickness, per_vertex_thickness=False)
        scaffold = inflator.mesh

        scaffold = PyMesh2Ply(scaffold)
        mesh = wm.WrapMesh(scaffold,'scaffold')
        num = self._class_dict['scaffold']
        element = ele.Element([mesh],'scaffold_ele') 

        T.toc()
        return element 
   
    
    
    """ gibt das Gerüst immer im Eiheitswürfel zurück 
        scaffolds type => List<WrapMesh> 
        Class type => int               """
    def scaffold(self,reps):
#        if reps is None:
#            func = np.random.poisson(lam=1.82)
#            lmb = lambda:  max(min(4, func), 1)
#            reps = [lmb() for _ in range(3)]
#            reps[0] = 1
        
        logger = logging.getLogger('generator.objectfactory.scaffold')
        T = TicToc(logger)
         
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

        ele_scaffold = ele.Element(scaffolds,'scaffols') 
        center = ele_scaffold.entire_mesh.center_mass
        center[2] = 0
        ele_scaffold.translate(-center)

        T.toc() 
        return ele_scaffold


    """ Classes[0] = roof; Classes[1] = body; Classes[2] = scaffold """

    def hws(self,reps):
        
        logger = logging.getLogger('generator.objectfactory.hws')
        T = TicToc(logger)
         
        hws = self.house() # returns (roof,mesh)
        hws.wmeshes[0]._prefix = 'hws_'
        hws.wmeshes[1]._prefix = 'hws_'
        
        width = 0.01
        transl = (1+width,0,0) 
        scale = [1*0.25,1,1,1]
        
        scaffolds = self.scaffold(reps)
        scaffolds.scale(scale)
        scaffolds.translate(transl)
        
        hws.add_element(scaffolds)

        T.toc() 
        return hws

    def scaffold_test(self):
        
        logger = logging.getLogger('generator.objectfactory.scaffold_test')
        T = TicToc(logger)
         
        width = 0.08 
        transl = (1+width,0,0) 
        transf = np.diag([1*0.25,1,1,1])
        
        scaffolds = ScaffoldFactory(reps,None)
        T.toc() 
        return scaffolds 










