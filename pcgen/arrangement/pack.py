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
        """TODO: Some Bug is appearing. Rectangles do not cover most efficiently"""
        self._height = height
        self._width = width
        self._processed_rectangles = 0
        self.rectangles= []
        self.packer = rp.newPacker(rp.PackingMode.Online,rotation=False)
        self.packer.add_bin(self._width,self._width)
        self._packed_elements = [] 
        self.logger = logging.getLogger('pcgen.arrangement.RectangleArranger')

    @property
    def packed_elements(self):
        return self._packed_elements
        
    """ gettin ugly here. The packer does not indicate if it was able to pack rect into bin 
        Thus, checks are performed """
    def packstuff(self,elements):
        listlength = 0
        for ele in elements:
            rect_ele= self._process_element(ele)
            if rect_ele is not None:
                self._apply_translation(rect_ele)
                self._packed_elements.append(rect_ele)
                
        self.logger.info(' I packed {}/{}'
                ' elements'.format(len(self._packed_elements),len(elements))) 
        only_elements = [ele for rect,ele in self._packed_elements]
        return only_elements 

    
    def _packer_changed(self):
        dif =  len(self.packer.rect_list()) - self._processed_rectangles 
        if dif < 0 or dif > 1:
            self.logger.info('dif: {}'.format(dif))
            raise Exception('This is a bug')
        elif dif == 1:
            self.logger.info('packer changed: Yes!')
            return True 
        elif dif == 0:
            self.logger.info('packer changed: No!')
            return False
    
    
    def _process_element(self,ele):
        
        _,hw= ele.ground_truth
        hw = (rp.float2dec(hw[0], 2), rp.float2dec(hw[1], 2))

        if hw > (self._height,self._width): 
            self.logger.warning('element to big to fit the scene. Element skiped!\n'
                                'Scene {}, element {}'.format((self._height,self._width),hw))
            return None
        
        if not self._packer_changed():
            self.packer.add_rect(*hw,rid=ele.name)
            
            if self._packer_changed():
                self._processed_rectangles += 1
                self.logger.info('{} processed (w:{:2.2f})'
                            ',(b:{:2.2f})'.format(ele.name,hw[0],hw[1]))
                return (self.packer.rect_list()[-1],ele)
            else:
                self.logger.warning('skiped! {} was to big!'.format(ele.name))
                return None
                #raise Exception('why has it not changed?')
        else:
            raise Exception('why has it changed?')
        
    
    
    def _apply_translation(self,rect_ele):
        """TODO: Docstring for apply_translation.
        :returns: TODO

        """
        rect,element = rect_ele
        self.logger.info('{} translated'
                ' by (x:{}, y:{})'.format(element.name,float(rect[1]),float(rect[2])))
        transl = np.array([-element.lower_left[0],-element.lower_left[1],0]) + \
                    np.array([float(rect[1]),float(rect[2]),0.0])
        element.translate(transl)


