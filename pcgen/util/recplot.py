#!/usr/bin/env python
# -*- coding: utf-8 -*-


import stuff



def PlotRectangles():
    fig,ax = plt.subplots(1)
    plt.xlim(xlim)
    plt.ylim(ylim)
     

    # Create a Rectangle patch
    for rec in rects:
        
        tmp = patches.Rectangle((float(rec[1]),float(rec[2])),float(rec[3]),float(rec[4]),
                linewidth=1,edgecolor='b',facecolor='r')
        ax.add_patch(tmp)
    
   [logger.info('höhe: {:2.2f} '
        'breite: {:2.2f} '
        'x: {:2.2f} '
        'y: {:2.2f} '.format(ele.ground_truth[1][0],
                                    ele.ground_truth[1][1],
                                    ele.ground_truth[0][0],
                                    ele.ground_truth[0][1]))
                    for ele in eles]

