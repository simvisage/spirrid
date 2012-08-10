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

if __name__ == '__main__':
    from spirrid.rv import RV
    from etsproxy.traits.ui.api import View, Item
    v = View(Item('type', label = 'Distribution type'),
             Item('loc', label = 'Location'),
             Item('scale', label = 'Scale'),
             Item('shape', label = 'Shape'),
             title = 'Random variable',
             buttons = ['OK', 'Cancel'])
    
    rv = RV(type = 'norm', scale = 10, shape = 1)
    rv.configure_traits(view = v)
