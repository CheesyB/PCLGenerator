#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from util.wrapmesh_test import WrapMeshTest 
from util.elementsaver_test import ElementSaverTest
from element.container_test import ContainerTest
from element.basement_test import BasementTest
from element.house_test import HouseTest
from element.hws_test import HwsTest
from element.scaffold_test import ScaffoldTest
from element.elementfactory_test import ElementFactoryTest

if __name__ == "__main__":
    unittest.main(verbosity=2)
