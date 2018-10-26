#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rectpack import newPacker



class KnapSackTranslator(object):

    """ Takes a list of elements, gets their groundtruth and calculates the
        translations for each element to fit in the scene without overlap """
     
    def __init__(self,height, width):
        """TODO: to be defined1. """
        self._height = height
        self._width = width
        

    def get_scene_parts(self,elements):
        self.elements = elements 
        for ele in elements
            gt = ele.groundtruth
            self.rectangles = # gt iwas

#    def calcualte_translations(self,distance=None):
#        """ 
#        self.translations = {self.elements[i]:translation_matrix}
#        """
#        pass
#
#    def apply_translation(self):
#        """TODO: Docstring for apply_translation.
#        :returns: TODO
#
#        """
#        for ele in self.current_elements:
#            ele.tranlate(self.translations[ele])













rectangles = [(100, 30), (40, 60), (30, 30),(70, 70), (100, 50), (30, 30)]
bins = [(300, 450)]

packer = newPacker()

# Add the rectangles to packing queue
for r in rectangles:
	packer.add_rect(*r)

# Add the bins where the rectangles will be placed
for b in bins:
	packer.add_bin(*b)

# Start packing
packer.pack()


#btain number of bins used for packing
nbins = len(packer)

# Index first bin
abin = packer[0]

# Bin dimmensions (bins can be reordered during packing)
width, height = abin.width, abin.height

# Number of rectangles packed into first bin
nrect = len(packer[0])

# Second bin first rectangle
rect = packer[0][0]

# rect is a Rectangle object
x = rect.x # rectangle bottom-left x coordinate
y = rect.y # rectangle bottom-left y coordinate
w = rect.width
h = rect.height

for abin in packer:
  print(abin.bid) # Bin id if it has one
  for rect in abin:
    print(rect)

# Full rectangle list
all_rects = packer.rect_list()
for rect in all_rects:
	b, x, y, w, h, rid = rect

# b - Bin index
# x - Rectangle bottom-left corner x coordinate
# y - Rectangle bottom-left corner y coordinate
# w - Rectangle width
# h - Rectangle height
# rid - User asigned rectangle id or None:

print('end')
