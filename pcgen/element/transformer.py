#!/usr/bin/env python
# -*- coding: utf-8 -*-



class Transformer(object):
    
    def __init__(self,**kwargs):
        
        self._translate = kwargs['translate']
        self._rotate = kwargs['rotate']
        sefl._scale = kwargs['scale']
    
    
    
    def rand_translate(self):
        self.logger.debug('random translation'.format())
        translation = self._transformer.rand_translate()
        #translation = [np.random.uniform(-1,1),np.random.uniform(-1,1),0] 
        translation = self._translate()

        lower_left = self.lower_left
        for wmesh in self.wmeshes:
            wmesh._mesh.vertices += translation

    def rand_rotate(self):
        R = transformer.rand_rotate()
         self.logger.debug('random rotation'.format())
         alpha = np.random.uniform(0,360)
         zaxis = [0,0,1] 
         R = trans.rotation_matrix(alpha,zaxis)
        for wmesh in self.wmeshes:
            wmesh.transform([R])

    def rand_scale(self):
        self.logger.debug('random scale'.format())
        S = self._transformer.rand_scale()
        #scale = np.array([15,15,0.1,1])
        #S = np.diag(scale)
        for wmesh in self.wmeshes:
            wmesh.transform([S])

