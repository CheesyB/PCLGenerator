#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import logging 
import trimesh as tri
import simples.element  as ele
import simples.wrapmesh as wm
import simples.elementsaver as es
import simples.utils as utils

logger = logging.getLogger('generator.generator')
logging.getLogger('generator').setLevel(logging.INFO)






if __name__ == "__main__":
    

    cdict = utils.color_dict()
    saver = es.ElementSaver(cdict,'data')
    saver.delete_files()    

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('generator').setLevel(logging.INFO)
    logging.getLogger('trimesh').setLevel(logging.CRITICAL)
    
    box = tri.creation.box()
    wm_box = wm.WrapMesh(box,'box',1)
    ele_box = ele.Element(wm_box,'test')
    gt = ele_box.ground_truth 
            
        


        













