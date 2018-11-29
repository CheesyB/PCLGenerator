#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
import h5py 
from pcgen.scene.scene import Scene
from pcgen.scene.h5dataset import Dataset
from pcgen.element import container 



class DatasetTest(unittest.TestCase):
   
    def setUp(self):
        ele1 = container.Container(0)
        ele2 = container.Container(1)
        ele3 = container.Container(2)
        self.eles = [ele1,ele2,ele3]
        self.scene1 = Scene(self.eles)
        self.scene2 = Scene(self.eles)
    

    def test_dataset(self):
        dataset = Dataset('test.hdf5',None)
        dataset.append(self.scene1)
        dataset.append(self.scene2)
        
    def test_write_data(self):
        dataset = Dataset('test.hdf5',None)
        dataset.append(self.scene1)
        dataset.append(self.scene2)
        dataset.write_data()


if __name__ == "__main__":
    unittest.main(verbosity=2)
