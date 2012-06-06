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

from etsproxy.traits.api import HasStrictTraits, Array, Property, Float, \
    cached_property, Callable, Str, Int, WeakRef, Dict, Event
from rv import RV
import numpy as np
import types
from function_randomization import \
    FunctionRandomization, make_ogrid, make_ogrid_full

#===============================================================================
# Randomization classes
#===============================================================================
class RandomSampling(HasStrictTraits):
    '''Deliver the discretized theta and dG
    '''
    randomization = WeakRef(FunctionRandomization)

    recalc = Event

    # count the random variables
    n_rand_vars = Property
    def _get_n_rand_vars(self):
        return self.randomization.n_rand_vars

    n_sim = Property
    def _get_n_sim(self):
        '''Get the total number of sampling points.
        '''
        n_int = self.randomization.n_int
        return n_int ** self.n_rand_vars

    def get_theta_range(self, tvar):
        '''Return minimu maximum and delta of the variable.
        '''
        if tvar.n_int != None:
            n_int = tvar.n_int
        else:
            n_int = self.randomization.n_int
        min_theta = tvar.ppf(1e-16)
        max_theta = tvar.ppf(1 - 1e-16)
        len_theta = max_theta - min_theta
        d_theta = len_theta / n_int
        return min_theta, max_theta, d_theta

    theta = Property()

    def get_samples(self, n):
        '''Get the fully expanded samples (for plotting)
        '''
        raise NotImplemented

class RegularGrid(RandomSampling):
    '''Grid shape randomization
    '''
    theta_list = Property(Array(float), depends_on = 'recalc')
    @cached_property
    def _get_theta_list(self):
        '''Get the orthogonally oriented arrays of random variables. 
        '''
        theta_list = []
        for tvar in self.randomization.tvar_lst:
            if isinstance(tvar, float):
                theta_list.append(tvar)
            elif isinstance(tvar, int):
                theta_list.append(float(tvar))
            elif isinstance(tvar, RV):
                theta_list.append(self.get_theta_for_distrib(tvar))
            else:
                raise TypeError, 'bad random variable specification: %s' % tvar

        return theta_list

    theta = Property(Array(float), depends_on = 'recalc')
    @cached_property
    def _get_theta(self):
        return make_ogrid(self.theta_list)

    dG = Property(Array(float), depends_on = 'recalc')
    @cached_property
    def _get_dG(self):
        if len(self.dG_ogrid) == 0:
            # deterministic case
            return 1.0
        else:
            # cross product of dG marginal values
            return reduce(lambda x, y: x * y, self.dG_ogrid)

    def get_samples(self, n):
        '''Get the fully expanded samples.
        '''
        # make the random permutation of the simulations and take n of them
        idx = np.random.permutation(np.arange(self.n_sim))[:n]
        # full orthogonalization (including scalars)
        otheta = make_ogrid_full(self.theta_list)
        # array of ones used for expansion 
        oarray = np.ones(np.broadcast(*otheta).shape, dtype = float)
        # expand (broadcast), flatten and stack the arrays
        return np.vstack([ (t * oarray).flatten()[idx] for t in otheta ])

class TGrid(RegularGrid):
    '''
        Regular grid of random variables theta.
    '''
    theta_11 = Array(float)
    def _theta_11_default(self):
        ''' 'discretize the range (-1,1) symmetrically with n_int points '''
        n_int = self.randomization.n_int
        return np.linspace(-(1.0 - 1.0 / n_int),
                             (1.0 - 1.0 / n_int) , n_int)

    def get_theta_for_distrib(self, tvar):
        if tvar.n_int != None:
            n_int = tvar.n_int
        else:
            n_int = self.randomization.n_int
        min_theta, max_theta, d_theta = self.get_theta_range(tvar)
        return np.linspace(min_theta + 0.5 * d_theta,
                            max_theta - 0.5 * d_theta, n_int)

    dG_ogrid = Property(Array(float), depends_on = 'recalc')
    @cached_property
    def _get_dG_ogrid(self):
        dG_ogrid = [ 1.0 for i in range(len(self.theta)) ]
        for i, (tvar, theta) in \
            enumerate(zip(self.randomization.tvar_lst, self.theta)):
            if not isinstance(tvar, float):
                # get the size of the integration cell
                min_theta, max_theta, d_theta = self.get_theta_range(tvar)
                dG_ogrid[i] = tvar.pdf(theta) * d_theta
        return dG_ogrid

class PGrid(RegularGrid):
    '''
        Regular grid of probabilities
    '''
    pi = Array(float)
    def _pi_default(self):
        n_int = self.randomization.n_int
        return np.linspace(0.5 / n_int,
                            1. - 0.5 / n_int, n_int)

    def get_theta_for_distrib(self, distrib):
        return distrib.ppf(self.pi)

    dG_ogrid = Property(Array(float), depends_on = 'recalc')
    @cached_property
    def _get_dG_ogrid(self):
        return np.repeat(1. / self.randomization.n_int, self.n_rand_vars)

    def _get_dG(self):
        return 1.0 / self.n_sim

class IrregularSampling(RandomSampling):
    '''Irregular sampling based on Monte Carlo concept
    '''
    dG = Property(Array(float))
    @cached_property
    def _get_dG(self):
        return 1. / self.n_sim

    def get_samples(self, n):
        n = min(self.n_sim, n)
        idx = np.random.permutation(np.arange(self.n_sim))[:n]
        s_list = []
        for t in self.theta:
            if isinstance(t, np.ndarray):
                s_list.append(t[idx])
            else:
                s_list.append(np.repeat(t, n))
        return np.vstack(s_list)

class MonteCarlo(IrregularSampling):
    '''
        Standard Monte Carlo randomization:
        For each variable generate n_sim = n_int ** n_rv 
        number of sampling points.
    '''

    theta = Property(Array(float), depends_on = 'recalc')
    @cached_property
    def _get_theta(self):

        theta_list = []
        for tvar in self.randomization.tvar_lst:
            if isinstance(tvar, types.FloatType):
                theta_list.append(tvar)
            else:
                theta_arr = tvar.rvs(self.n_sim)
                theta_list.append(theta_arr)
        return theta_list

class LatinHypercubeSampling(IrregularSampling):
    '''
        Latin hypercube sampling generated from the 
        samples of the individual random variables 
        with random perturbation.
    '''

    pi = Array(float)
    def _pi_default(self):
        return np.linspace(0.5 / self.n_sim,
                            1. - 0.5 / self.n_sim, self.n_sim)

    theta = Property(Array(float), depends_on = 'recalc')
    @cached_property
    def _get_theta(self):

        theta_list = []
        for tvar in self.randomization.tvar_lst:
            if isinstance(tvar, float):
                theta_list.append(tvar)
            else:
                # point probability function
                theta_arr = tvar.ppf(self.pi)
                theta_list.append(np.random.permutation(theta_arr))
        return theta_list
