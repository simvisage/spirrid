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

from distribution import Distribution
from etsproxy.pyface.api import ImageResource
from etsproxy.traits.api import HasTraits, Float, Int, Event, Array, Interface, \
    Tuple, Property, cached_property, Instance, Enum, on_trait_change
from etsproxy.traits.ui.api import \
    Item, View, Group, HSplit, VGroup, Tabbed
from math import sqrt
from matplotlib.figure import Figure
from numpy import linspace
from scipy.stats import norm, uniform, weibull_min, gamma
from piecewise_uniform_distr import piecewise_uniform
from sin2x_distr import sin2x
from sinus_distribution import sin_distr
from spirrid.util.traits.editors.mpl_figure_editor import MPLFigureEditor
from pylab import plt
import tempfile

''' a dictionary filled with distribution names (keys) and
    scipy.stats.distribution attributes having None
    or 1 shape parameters (values)'''
# for distr in distributions.__all__[2:84]:
#    if distributions.__dict__[distr].shapes == None:
#        distr_dict[distr] = distributions.__dict__[distr]
#        distr_enum.append(distr)
#
#    elif len(distributions.__dict__[distr].shapes) == 1:
#        distr_dict[distr] = distributions.__dict__[distr]
#        distr_enum.append(distr)

class IPDistrib(Interface):

    n_segments = Int

class PDistrib(HasTraits):

    implements = IPDistrib

    def __init__(self, **kw):
        super(PDistrib, self).__init__(**kw)
        self.on_trait_change(self.refresh, 'distr_type.changed,quantile,n_segments')
        self.refresh()

    # puts all chosen continuous distributions distributions defined
    # in the scipy.stats.distributions module as a list of strings
    # into the Enum trait
    # distr_choice = Enum(distr_enum)

    distr_choice = Enum('sin2x', 'weibull_min', 'sin_distr', 'uniform', 'norm', 'piecewise_uniform', 'gamma')
    distr_dict = {'sin2x' : sin2x,
                  'uniform' : uniform,
                  'norm' : norm,
                  'weibull_min' : weibull_min,
                  'sin_distr' : sin_distr,
                'piecewise_uniform' : piecewise_uniform,
                'gamma' : gamma}

    # instantiating the continuous distributions
    distr_type = Property(Instance(Distribution), depends_on='distr_choice')
    @cached_property
    def _get_distr_type(self):
        return Distribution(self.distr_dict[self.distr_choice])

    # change monitor - accumulate the changes in a single event trait
    changed = Event
    @on_trait_change('distr_choice, distr_type.changed, quantile, n_segments')
    def _set_changed(self):
        self.changed = True

    #------------------------------------------------------------------------
    # Methods setting the statistical modments
    #------------------------------------------------------------------------
    mean = Property
    def _get_mean(self):
        return self.distr_type.mean
    def _set_mean(self, value):
        self.distr_type.mean = value

    variance = Property
    def _get_variance(self):
        return self.distr_type.mean
    def _set_variance(self, value):
        self.distr_type.mean = value

    #------------------------------------------------------------------------
    # Methods preparing visualization
    #------------------------------------------------------------------------

    quantile = Float(1e-14, auto_set=False, enter_set=True)
    range = Property(Tuple(Float), depends_on=\
                      'distr_type.changed, quantile')
    @cached_property
    def _get_range(self):
        return (self.distr_type.distr.ppf(self.quantile), self.distr_type.distr.ppf(1 - self.quantile))

    n_segments = Int(500, auto_set=False, enter_set=True)

    dx = Property(Float, depends_on=\
                      'distr_type.changed, quantile, n_segments')
    @cached_property
    def _get_dx(self):
        range_length = self.range[1] - self.range[0]
        return range_length / self.n_segments

    #-------------------------------------------------------------------------
    # Discretization of the distribution domain
    #-------------------------------------------------------------------------
    x_array = Property(Array('float_'), depends_on=\
                        'distr_type.changed,'\
                        'quantile, n_segments')
    @cached_property
    def _get_x_array(self):
        '''Get the intrinsic discretization of the distribution
        respecting its  bounds.
        '''
        return linspace(self.range[0], self.range[1], self.n_segments + 1)

    #===========================================================================
    # Access function to the scipy distribution
    #===========================================================================
    def pdf(self, x):
        return self.distr_type.distr.pdf(x)

    def cdf(self, x):
        return self.distr_type.distr.cdf(x)

    def rvs(self, n):
        return self.distr_type.distr.rvs(n)

    def ppf(self, e):
        return self.distr_type.distr.ppf(e)

    #===========================================================================
    # PDF - permanent array
    #===========================================================================

    pdf_array = Property(Array('float_'), depends_on=\
                                    'distr_type.changed,'\
                                     'quantile, n_segments')
    @cached_property
    def _get_pdf_array(self):
        '''Get pdf values in intrinsic positions'''
        return self.distr_type.distr.pdf(self.x_array)

    def get_pdf_array(self, x_array):
        '''Get pdf values in externally specified positions'''
        return self.distr_type.distr.pdf(x_array)

    #===========================================================================
    # CDF permanent array
    #===========================================================================
    cdf_array = Property(Array('float_'), depends_on=\
                                    'distr_type.changed,'\
                                     'quantile, n_segments')
    @cached_property
    def _get_cdf_array(self):
        '''Get cdf values in intrinsic positions'''
        return self.distr_type.distr.cdf(self.x_array)

    def get_cdf_array(self, x_array):
        '''Get cdf values in externally specified positions'''
        return self.distr_type.distr.cdf(x_array)

    #-------------------------------------------------------------------------
    # Randomization
    #-------------------------------------------------------------------------
    def get_rvs_array(self, n_samples):
        return self.distr_type.distr.rvs(n_samples)

    figure = Instance(Figure)
    def _figure_default(self):
        figure = Figure(facecolor='white')
        return figure

    data_changed = Event

    def plot(self, fig):
        figure = fig
        figure.clear()
        axes = figure.gca()
        # plot PDF
        axes.plot(self.x_array, self.pdf_array, lw=1.0, color='blue', \
                  label='PDF')
        axes2 = axes.twinx()
        # plot CDF on a separate axis (tick labels left)
        axes2.plot(self.x_array, self.cdf_array, lw=2, color='red', \
                  label='CDF')
        # fill the unity area given by integrating PDF along the X-axis
        axes.fill_between(self.x_array, 0, self.pdf_array, color='lightblue',
                           alpha=0.8, linewidth=2)
        # plot mean
        mean = self.distr_type.distr.stats('m')
        axes.plot([mean, mean], [0.0, self.distr_type.distr.pdf(mean)],
                   lw=1.5, color='black', linestyle='-')
        # plot stdev
        stdev = sqrt(self.distr_type.distr.stats('v'))
        axes.plot([mean - stdev, mean - stdev],
                   [0.0, self.distr_type.distr.pdf(mean - stdev)],
                   lw=1.5, color='black', linestyle='--')
        axes.plot([mean + stdev, mean + stdev],
                   [0.0, self.distr_type.distr.pdf(mean + stdev)],
                   lw=1.5, color='black', linestyle='--')

        axes.legend(loc='center left')
        axes2.legend(loc='center right')
        axes.ticklabel_format(scilimits=(-3., 4.))
        axes2.ticklabel_format(scilimits=(-3., 4.))

        # plot limits on X and Y axes
        axes.set_ylim(0.0, max(self.pdf_array) * 1.15)
        axes2.set_ylim(0.0, 1.15)
        range = self.range[1] - self.range[0]
        axes.set_xlim(self.x_array[0] - 0.05 * range,
                      self.x_array[-1] + 0.05 * range)
        axes2.set_xlim(self.x_array[0] - 0.05 * range,
                      self.x_array[-1] + 0.05 * range)

    def refresh(self):
        self.plot(self.figure)
        self.data_changed = True

    icon = Property(Instance(ImageResource), depends_on='distr_type.changed,quantile,n_segments')
    @cached_property
    def _get_icon(self):
        fig = plt.figure(figsize=(4, 4), facecolor='white')
        self.plot(fig)
        tf_handle, tf_name = tempfile.mkstemp('.png')
        fig.savefig(tf_name, dpi=35)
        return ImageResource(name=tf_name)

    traits_view = View(HSplit(VGroup(Group(Item('distr_choice', show_label=False),
                                           Item('@distr_type', show_label=False),
                                           ),
                                      id='pdistrib.distr_type.pltctrls',
                                      label='Distribution parameters',
                                      scrollable=True,
                                      ),
                                Tabbed(Group(Item('figure',
                                            editor=MPLFigureEditor(),
                                            show_label=False,
                                            resizable=True),
                                            scrollable=True,
                                            label='Plot',
                                            ),
                                       Group(Item('quantile', label='quantile'),
                                             Item('n_segments', label='plot points'),
                                             label='Plot parameters'
                                            ),
                                        label='Plot',
                                        id='pdistrib.figure.params',
                                        dock='tab',
                                       ),
                                dock='tab',
                                id='pdistrib.figure.view'
                                ),
                                id='pdistrib.view',
                                dock='tab',
                                title='Statistical distribution',
                                buttons=['Ok', 'Cancel'],
                                scrollable=True,
                                resizable=True,
                                width=600, height=400
                        )


if __name__ == '__main__':
    pdistrib = PDistrib()
    pdistrib.refresh()
    pdistrib.configure_traits()
