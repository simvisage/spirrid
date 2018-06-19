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

from numpy import array,linspace, trapz, arange
from etsproxy.traits.api import Array, Bool, Callable, Enum, Float, Event, HasTraits, \
                                 Instance, Int, Trait, ToolbarButton, Button, on_trait_change, \
                                 Property, cached_property, List

from etsproxy.traits.ui.api import Item, View, Group, Handler, HGroup

from etsproxy.traits.ui.menu import NoButtons, OKButton, CancelButton, Action, CloseAction, Menu, \
                                     MenuBar, Separator

from mfn_line import MFnLineArray

import time
import math

class MFnMultiLine(HasTraits):

    # Public Traits
    lines = List( MFnLineArray )
    
    xdata = Property( List( Array ) ) 
    def _get_xdata(self):
        return [ mfn.xdata for mfn in self.lines ]
    
    ydata = Property( List( Array ) ) 
    def _get_ydata(self):
        return [ mfn.ydata for mfn in self.lines ]
    
    data_changed = Event
