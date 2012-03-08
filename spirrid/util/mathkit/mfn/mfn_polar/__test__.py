#-------------------------------------------------------------------------------
#
# Copyright (c) 2012
# IMB, RWTH Aachen University,
# ISM, Brno University of Technology
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in the Spirrid top directory "licence.txt" and may be
# redistributed only under the conditions described in the aforementioned
# license.
#
# Thanks for using Simvisage open source!
#
#-------------------------------------------------------------------------------

from mfn_polar import MFnPolar
import unittest

class TestSequenceFunctions(unittest.TestCase):
    
    def setUp(self):
        self.mp = MFnPolar( alpha = 0.7, delta_alpha = 0.25, delta_trans = 1. )

    def test_get_value(self):
        '''
        make sure that the values for corner nodes get returned properly
        - testing (x,y) plane
        '''
        value = self.mp( 0.225 )
        self.assertEqual( value, 0.4475 ) 
        
if __name__ == '__main__':
    unittest.main()
