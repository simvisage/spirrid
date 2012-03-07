#-------------------------------------------------------------------------------
#
# Copyright (c) 2009, IMB, RWTH Aachen.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in simvisage/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.simvisage.com/licenses/BSD.txt
#
# Thanks for using Simvisage open source!
#
# Created on Dec 16, 2011 by: rch

import sys
import os

cdir = os.path.abspath('../../')
sys.path.append(cdir)

from etsproxy.traits.api import HasTraits, Instance, Button
from etsproxy.traits.ui.api import View, Item

from spirrid.examples import SPIRRIDLAB

from fiber_tt_2p import fiber_tt_2p
from fiber_tt_5p import fiber_tt_5p
from fiber_po_8p import fiber_po_8p
from fiber_cb_8p import fiber_cb_8p
from masked_arrays import mask_arr
from numexpr_test import numexpr_test
import script


class Demo(HasTraits):
    '''Demo class for response functions'''

    fiber_tt_2p = Instance(SPIRRIDLAB)
    def _fiber_tt_2p_default(self):
        return fiber_tt_2p.create_demo_object()

    fiber_tt_5p = Instance(SPIRRIDLAB)
    def _fiber_tt_5p_default(self):
        return fiber_tt_5p.create_demo_object()

    fiber_po_8p = Instance(SPIRRIDLAB)
    def _fiber_po_8p_default(self):
        return fiber_po_8p.create_demo_object()

    fiber_cb_8p = Button()
    def _fiber_cb_8p_fired(self):
        return fiber_cb_8p.main()

    mask_arr_b = Button()
    def _mask_arr_b_fired(self):
        return mask_arr.main()

    numexpr_b = Button()
    def _numexpr_b_fired(self):
        return numexpr_test.main()

    script_b = Button()
    def _script_b_fired(self):
        return script.main()

    traits_view = View(Item('fiber_tt_2p', show_label = False),
                       Item('fiber_tt_5p', show_label = False),
                       Item('fiber_po_8p', show_label = False),
                       Item('fiber_cb_8p', show_label = False),
                       Item('mask_arr_b', show_label = False),
                       Item('numexpr_b', show_label = False),
                       Item('script_b', show_label = False),
                       width = 0.2,
                       height = 0.3,
                       buttons = ['OK', 'Cancel'])


if __name__ == '__main__':
    d = Demo()
    d.configure_traits()
