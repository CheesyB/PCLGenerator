#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging 
import numpy as np
from pcgen.util.elementsaver import ElementSaver 
from pcgen.element import elementfactory as ef
from pcgen.element import container 
from pcgen.element import basement
from pcgen.element import house
from pcgen.element import hws
from pcgen.element import scaffold
import arrangement.pack as pk
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from rectpack import float2dec,newPacker




if __name__ == "__main__":
    
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('pcgen').setLevel(logging.INFO)
    logging.getLogger('matplotlib').setLevel(logging.CRITICAL)
    logging.getLogger('trimesh').setLevel(logging.CRITICAL)
    logger = logging.getLogger('pcgen.main') 

    saver = ElementSaver('../data')
    saver.delete_files()    

    
    elefac = ef.ElementFactory() 
    eles = []
    eles.append(container.Container)
    eles.append(basement.Basement)
    eles.append(hws.Hws)
    eles.append(scaffold.Scaffold)
    eles.append(house.House)

    [elefac.register_element(ele) for ele in eles] 
    seq = elefac.get_random_sequence(5)

    xlim = 5 
    ylim = 5 
    kst = pk.RectangleArranger(float2dec(xlim,2),float2dec(ylim,2))
    packer = kst.packstuff(seq)
    rects = packer.rect_list()    

    for ele,rec in zip(seq,rects):
        logger.debug('x: {} '
                    'y: {} '
                    'höhe: {} ' 
                    'breite: {} '.format(rec[1],rec[2],rec[3],rec[4]))
        saver.save_as_pc(ele) 

#    ax.autoscale()
#    plt.show()
    
            
        


        













