#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import logging 
import trimesh as tri
import simples.element  as ele
import simples.wrapmesh as wm
import simples.elementsaver as es
import simples.utils as utils
import simples.elementfactory as ef
import arrangement.pack as pk
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from rectpack import float2dec,newPacker




if __name__ == "__main__":
    
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('generator').setLevel(logging.INFO)
    logging.getLogger('trimesh').setLevel(logging.CRITICAL)
    logger = logging.getLogger('generator.generator') 

    saver = es.ElementSaver('data')
    saver.delete_files()    

    
    elefac = ef.ElementFactory(1.2) 
    eles = []
    eles.append(elefac.container())
    eles.append(elefac.house())
    eles.append(elefac.hws([1,2,2]))
    eles.append(elefac.hws([1,2,2]))
    eles.append(elefac.scaffold([1,3,2]))
    xlim = 4.5 
    ylim = 3 
    [logger.info('höhe: {:2.2f} '
        'breite: {:2.2f} '
        'x: {:2.2f} '
        'y: {:2.2f} '.format(ele.ground_truth[1][0],
                                    ele.ground_truth[1][1],
                                    ele.ground_truth[0][0],
                                    ele.ground_truth[0][1]))
                    for ele in eles]
    kst = pk.RectangleArranger(float2dec(xlim,2),float2dec(ylim,2))
    packer = kst.packstuff(eles)
    rects = packer.rect_list()    


    # Create figure and axes
    fig,ax = plt.subplots(1)
    plt.xlim(xlim)
    plt.ylim(ylim)
     

    # Create a Rectangle patch
    for rec in rects:
        logger.info('höhe: {} '
                    'breite: {} '
                    'x: {} '
                    'y: {} '.format(rec[3],rec[4],rec[1],rec[1]))
        
        tmp = patches.Rectangle((float(rec[1]),float(rec[2])),float(rec[3]),float(rec[4]),
                linewidth=1,edgecolor='b',facecolor='r')
        ax.add_patch(tmp)

    # Add the patch to the Axes
    [saver.save_as_pc(ele) for ele in eles]

    plt.show()
    
            
        


        













