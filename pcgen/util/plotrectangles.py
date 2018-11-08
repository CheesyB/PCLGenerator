#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging 
import matplotlib.pyplot as plt
import matplotlib.patches as patches



def PlotRectangles(packed_elements):

    logger = logging.getLogger('pcgen.utils.PlotRectangles')
    fig,ax = plt.subplots(1)
    
    for rec,ele in packed_elements:
        
        tmp = patches.Rectangle((float(rec[1]),float(rec[2])),float(rec[3]),float(rec[4]),
                linewidth=1,edgecolor='black',facecolor='#0091FA')
        ax.add_patch(tmp)
        #so
        rx, ry = tmp.get_xy()
        cx = rx + tmp.get_width()/2.0
        cy = ry + tmp.get_height()/2.0

        ax.annotate(ele.name, (cx, cy), color='w', weight='bold', 
                fontsize=6, ha='center', va='center')
        
        logger.info('höhe: {:2.2f} '
            'breite: {:2.2f} '
            'x: {:2.2f} '
            'y: {:2.2f} '.format(rec[1],rec[2],rec[3],rec[4]))
    ax.autoscale()
    ax.set_aspect('equal')
    ax.grid(True)
    ax.set_axisbelow(True)
    return plt 
