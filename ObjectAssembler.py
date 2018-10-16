#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pa
import PlyObjects as po
import utils 

# house = trimesh, normal = orientation of the scaffold, w|h|l dims of one scaffold
# reps= (repitition in x, repition in y)
def AddScaffold(house,normal,gap,witdh,height,length,reps):
    obb = house.bounding_box_oriented
    pmin = obb.vertices.argmin(0)
    pmax = obb.verices.argmax(0)
    
    for i in range(reps[0]):
        for j in range(reps[1]):
            

    








if __name__ == "__main__":
    po.
    
