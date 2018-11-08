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
from pcgen.util.plotrectangles import PlotRectangles
from rectpack import float2dec,newPacker
import arrangement.pack as pk
import matplotlib.pyplot as plt




if __name__ == "__main__":
    
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('pcgen').setLevel(logging.INFO)
    logging.getLogger('matplotlib').setLevel(logging.CRITICAL)
    logging.getLogger('trimesh').setLevel(logging.CRITICAL)
    logger = logging.getLogger('pcgen.main') 

    saver = ElementSaver('../data')
    saver.delete_files()    
    
    xlim = 7
    ylim = 7 
    
    elefac = ef.ElementFactory() 

    basem = basement.Basement((0,1))
    basem.scale([xlim,ylim,0.1,1]) 
    basem.translate([xlim/2,ylim/2,0])
    
    eles = []
    eles.append(container.Container)
    eles.append(hws.Hws)
    eles.append(scaffold.Scaffold)
    eles.append(house.House)

    [elefac.register_element(ele) for ele in eles] 
    seq = elefac.get_random_sequence(8)

    kst = pk.RectangleArranger(float2dec(xlim,2),float2dec(ylim,2))
    packed_elements = kst.packstuff(seq)
    
    PlotRectangles(packed_elements)

    for rec,ele in packed_elements:
        logger.debug('x: {} '
                    'y: {} '
                    'höhe: {} ' 
                    'breite: {} '.format(rec[1],rec[2],rec[3],rec[4]))
        saver.save_as_pc(ele) 
    saver.save_as_pc(basem) # adding this will place the others on top 
    plt.show()
    


