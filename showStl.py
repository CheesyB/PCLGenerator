#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ipdb
import os
#from pyntcloud import PyntCloud
from render.show3d_balls import showpoints
import numpy as np
import pandas as pd
import stl as stl
import matplotlib as plt

mesh = stl.mesh.Mesh.from_file('data/stanford_dragon.stl')
normals = mesh.data['normals']
vectors = mesh.data['vectors']
points = vectors.reshape([-1,3])

pd_points = pd.DataFrame(data=points,columns=['x','y','z'])

#ipdb.set_trace()

showpoints(points)









