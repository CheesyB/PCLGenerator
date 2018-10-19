
import numpy as np
import logging 
import Objects as o
import Assembler as a
import trimesh as tri
    
    
 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('generator.ObjectFactory')
logging.getLogger('generator').setLevel(logging.INFO)

class ObjectFactory(object):

    """This is a Class which takes all the inforamtion to
    """

    def __init__(self,classDict,thickness):
        """TODO: to be defined1.

        :classDict: TODO
        :thickness: TODO

        """
        self._classDict = classDict
        self._thickness = thickness
        
