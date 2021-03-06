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

import wx

import matplotlib
# We want matplotlib to use a wxPython backend
matplotlib.use( 'WXAgg' )
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_wx import NavigationToolbar2Wx

from etsproxy.traits.api import Any, Instance
#from etsproxy.traits.ui.api import Editor
from etsproxy.traits.ui.api import Editor
#from etsproxy.traits.ui.basic_editor_factory import BasicEditorFactory
from etsproxy.traits.ui.api import BasicEditorFactory

class _MPLFigureEditor( Editor ):

    scrollable = True

    def init( self, parent ):
        self.control = self._create_canvas( parent )
        self.object.on_trait_change( self.update_editor, 'data_changed' )
        self.set_tooltip()

    def update_editor( self ):
        figure = self.value
        figure.canvas.draw()

    def _create_canvas( self, parent ):
        """ Create the MPL canvas. """
        # The panel lets us add additional controls.
        panel = wx.Panel( parent, -1, style = wx.CLIP_CHILDREN )
        sizer = wx.BoxSizer( wx.VERTICAL )
        panel.SetSizer( sizer )

        # matplotlib commands to create a canvas
        mpl_control = FigureCanvas( panel, -1, self.value )
        toolbar = NavigationToolbar2Wx( mpl_control )
        sizer.Add( toolbar, 0, wx.EXPAND )
        sizer.Add( mpl_control, 1, wx.LEFT | wx.TOP | wx.GROW )
        self.value.canvas.SetMinSize( ( 100, 100 ) )
        return panel

class MPLFigureEditor( BasicEditorFactory ):

    klass = _MPLFigureEditor


if __name__ == "__main__":
    # Create a window to demo the editor
    from etsproxy.traits.api import HasTraits
    from etsproxy.traits.ui.api import View, Item
    from numpy import sin, cos, linspace, pi

    class Test( HasTraits ):

        figure = Instance( Figure, () )

        view = View( Item( 'figure', editor = MPLFigureEditor(),
                                show_label = False ),
                        width = 400,
                        height = 300,
                        resizable = True )

        def __init__( self ):
            super( Test, self ).__init__()
            axes = self.figure.add_subplot( 111 )
            t = linspace( 0, 2 * pi, 200 )
            axes.plot( sin( t ) * ( 1 + 0.5 * cos( 11 * t ) ), cos( t ) * ( 1 + 0.5 * cos( 11 * t ) ) )

    Test().configure_traits()
