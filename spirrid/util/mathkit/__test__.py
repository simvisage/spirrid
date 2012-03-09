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

from mfn.mfn_ndgrid.mfn_ndgrid import MFnNDGrid, GridPoint
import unittest

class TestSequenceFunctions(unittest.TestCase):
    
    def setUp(self):
        self.mfn = MFnNDGrid( shape = (1,1,1),
                            active_dims = ['x','y'],
                            x_maxs = GridPoint( x = 1, y = 1, z = 1 ) )

    def test_set_values_in_range(self):
        '''
        make sure that the values for corner nodes get returned properly
        - testing (x,y) plane
        '''
        self.mfn.set_values_in_box( 4.3, [0.5,0.5,0.5], [5,5,2] )
        self.assertEqual( self.mfn.get_value([0,0,0]), 1 )        
        self.assertEqual( self.mfn.get_value([0,0,0]), 1 )        
        self.assertEqual( self.mfn.get_value([0,0,0]), 1 )        
        self.assertAlmostEqual( self.mfn.get_value([1,1,0]), 4.3 )

    def test_refine_grid(self):
        '''
        Refine the grid and test the new set of point values
        '''
        self.mfn.shape = (2,2,1)
        self.mfn.set_values_in_box( 4.3, [0.49, 0.49, 0.49], [1, 1, 2] )
        
        self.assertAlmostEqual( self.mfn([1, 1, 0]), 4.3 )
        self.assertAlmostEqual( self.mfn([0.5, 0.5, 0]), 4.3 )
        self.assertAlmostEqual( self.mfn([0, 0, 0]), 1 )
        self.assertAlmostEqual( self.mfn([0, 1, 0]), 1 )

    def xtest_reshape_grid(self):
        '''
        Reshape the array and test the new set of point values
        @TODO - finish the test
        '''
        self.mfn.active_dims = ['x','z']
        self.mfn.shape = (2,2,2)
        self.mfn.set_values_in_box( 2, [0.49, 0.49, 0], [1.1, 2, 0] )
        
        self.assertAlmostEqual( self.mfn([1, 1, 0]), 2 )
