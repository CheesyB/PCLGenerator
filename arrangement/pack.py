#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rectpack as rp #float2dec,newPacker
import logging


class RectangleArranger(object):

    """ Takes a list of elements, gets their groundtruth and calculates the
        translations for each element to fit in the scene without overlap """
     
    def __init__(self,height, width):
        """TODO: to be defined1. """
        self._height = height
        self._width = width
        self.rectangles= []
        self.packer = rp.newPacker(rp.PackingMode.Online,rotation=False)
        self.packer.add_bin(self._width,self._width)
        self.logger = logging.getLogger('generator.arrangement.RectangleArranger')
        
    def packstuff(self,elements):
        for ele in elements:
            self.logger.info('{} is processed'.format(ele.name))
            _,hw= ele.ground_truth
            hw = ((rp.float2dec(hw[0], 3), rp.float2dec(hw[1], 3)))
            self.packer.add_rect(*hw,rid=ele.name)
            rect = self.packer.rect_list()[-1]
            self._apply_translation(ele,rect)

#        rects = self.packer.rect_list()
#        
#        for ele in elements:
#            rect = [rect for rect in rects if rect[-1] == ele.name]
#            assert len(rect) is 1, 'only one rectangle makes sense here...'
                
        return self.packer

    def _calcualte_translation(self,element):
        """ 
        self.translations = {self.elements[i]:translation_matrix}
        """
        pass



    def _apply_translation(self,element,rect):
        """TODO: Docstring for apply_translation.
        :returns: TODO

        """
        
#        self.logger.info('we came this far:)')
        element.translate([float(rect[3]),float(rect[4]),0.0])












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
