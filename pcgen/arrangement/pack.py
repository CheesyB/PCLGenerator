#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rectpack as rp #float2dec,newPacker
import numpy as np
import logging


class RectangleArranger(object):

    """ Takes a list of elements, gets their groundtruth and calculates the
        translations for each element to fit in the scene without overlap
        b, x, y, w, h, rid = rect

         b[0] - Bin index
         x[1] - Rectangle bottom-left corner x coordinate
         y[2] - Rectangle bottom-left corner y coordinate
         w[3] - Rectangle width
         h[4] - Rectangle height
         rid - User asigned rectangle id or None
    """ 
    def __init__(self,height, width):
        """TODO: to be defined1. """
        self._height = height
        self._width = width
        self.rectangles= []
        self.packer = rp.newPacker(rp.PackingMode.Online,rotation=False)
        self.packer.add_bin(self._width,self._width)
        self.logger = logging.getLogger('pcgen.arrangement.RectangleArranger')
        
    def packstuff(self,elements):
        for ele in elements:
            self.logger.info('{} processed'.format(ele.name))
            _,hw= ele.ground_truth
            hw = (rp.float2dec(hw[0], 2), rp.float2dec(hw[1], 2))
            self.packer.add_rect(*hw,rid=ele.name)
            rect = self.packer.rect_list()[-1]
            self._apply_translation(ele,rect)
        return self.packer

    def _apply_translation(self,element,rect):
        """TODO: Docstring for apply_translation.
        :returns: TODO

        """
        self.logger.info('{} translated'
                ' by (x:{}, y:{})'.format(element.name,float(rect[1]),float(rect[2])))
        transl = np.array([-element.lower_left[0],-element.lower_left[1],0]) + \
                    np.array([float(rect[1]),float(rect[2]),0.0])
        element.translate(transl)



## Bin dimmensions (bins can be reordered during packing)
#width, height = abin.width, abin.height
#
## Number of rectangles packed into first bin
#nrect = len(packer[0])
#
## Second bin first rectangle
#rect = packer[0][0]
#
## rect is a Rectangle object
#x = rect.x # rectangle bottom-left x coordinate
#y = rect.y # rectangle bottom-left y coordinate
#w = rect.width
#h = rect.height
#
#for abin in packer:
#  print(abin.bid) # Bin id if it has one
#  for rect in abin:
#    print(rect)
#
## Full rectangle list
#all_rects = packer.rect_list()
#for rect in all_rects:
#	b, x, y, w, h, rid = rect
#
## b - Bin index
## x - Rectangle bottom-left corner x coordinate
## y - Rectangle bottom-left corner y coordinate
## w - Rectangle width
## h - Rectangle height
## rid - User asigned rectangle id or None:

print('end')
