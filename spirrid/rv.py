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

from etsproxy.traits.api import HasStrictTraits, Property, Float, cached_property, \
    Str, Int, Tuple, Dict

from pdistrib import PDistrib as PD

#===============================================================================
# Probability distribution specification
#===============================================================================
class RV(HasStrictTraits):

    def __init__(self, type, loc=0.0, scale=0.0, shape=1.0,
                  *args, **kw):
        '''Convenience initialization'''
        super(RV, self).__init__(*args, **kw)
        self.type = type
        self.loc = loc
        self.scale = scale
        self.shape = shape
        self.args = args
        self.kw = kw

    def __str__(self):
        return '%s( loc = %g, scale = %g, shape = %g)[n_int = %s]' % \
            (self.type, self.loc, self.scale, self.shape, str(self.n_int))

    n_int = Int(None)
    '''Number of integration points
    '''

    loc = Float
    '''Location parameter.
    '''

    scale = Float
    '''Scale parameter.
    '''

    shape = Float
    '''Shape parameter.
    '''

    type = Str
    '''Type specifier.
    '''

    args = Tuple
    '''Generic arguments.
    '''

    kw = Dict
    '''Generic keyword arguments.
    '''

    _distr = Property(depends_on='mu,std,loc,type')
    '''Construct a distribution.
    hidden property instance of the scipy stats distribution
    '''
    @cached_property
    def _get__distr(self):
        if self.n_int == None:
            n_segments = 10
        else:
            n_segments = self.n_int
        pd = PD(distr_choice=self.type, n_segments=n_segments)
        pd.distr_type.set(scale=self.scale, shape=self.shape, loc=self.loc)
        return pd

    # access methods to pdf, ppf, rvs
    def pdf(self, x):
        return self._distr.pdf(x)

    def ppf(self, x):
        return self._distr.ppf(x)

    def rvs(self, x):
        return self._distr.rvs(x)

