# -------------------------------------------------------------------------------
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
# -------------------------------------------------------------------------------

from etsproxy.traits.api import HasStrictTraits, Array, Property, Float, \
    cached_property, Callable, Str, Int, WeakRef, Dict, Event
from .rv import RV
import inspect
import numpy as np
import string
import types

# ===============================================================================
# Helper methoods to produce an-dimensional array from a list of arrays
# ===============================================================================
def make_ogrid(args):
    '''Orthogonalize a list of one-dimensional arrays.
    scalar values are left untouched.
    '''
    # count the number of arrays in the list
    dt = list(map(type, args))
    n_arr = dt.count(np.ndarray)

    oargs = []
    i = 0
    for arg in args:
        if isinstance(arg, np.ndarray):
            shape = np.ones((n_arr,), dtype='int')
            shape[i] = len(arg)
            i += 1
            oarg = np.copy(arg).reshape(tuple(shape))
            oargs.append(oarg)
        elif isinstance(arg, float):
            oargs.append(arg)
    return oargs

def make_ogrid_full(args):
    '''Orthogonalize a list of one-dimensional arrays.\
    including scalar values in args.
    '''
    oargs = []
    n_args = len(args)
    for i, arg in enumerate(args):
        if isinstance(arg, float):
            arg = np.array([arg], dtype='d')

        shape = np.ones((n_args,), dtype='int')
        shape[i] = len(arg)
        i += 1
        oarg = np.copy(arg).reshape(tuple(shape))
        oargs.append(oarg)
    return oargs

# ===============================================================================
# Function randomization
# ===============================================================================
class FunctionRandomization(HasStrictTraits):

    # response function
    q = Callable(input=True)

    # ===========================================================================
    # Inspection of the response function parameters
    # ===========================================================================
    var_spec = Property(depends_on='q')
    @cached_property
    def _get_var_spec(self):
        '''Get the names of the q_parameters'''
        if type(self.q) is types.FunctionType:
            arg_offset = 0
            q = self.q
        else:
            arg_offset = 1
            q = self.q.__call__
        argspec = inspect.getargspec(q)
        args = np.array(argspec.args[ arg_offset:])
        dflt = np.array(argspec.defaults)
        return args, dflt

    var_names = Property(depends_on='q')
    @cached_property
    def _get_var_names(self):
        '''Get the array of default values.
        None - means no default has been specified
        '''
        return self.var_spec[0]

    var_defaults = Property(depends_on='q')
    @cached_property
    def _get_var_defaults(self):
        '''Get the array of default values.
        None - means no default has been specified
        '''
        dflt = self.var_spec[1]
        defaults = np.repeat(None, len(self.var_names))
        start_idx = min(len(dflt), len(defaults))
        defaults[ -start_idx: ] = dflt[ -start_idx:]
        return defaults

    # ===========================================================================
    # Control variable specification
    # ===========================================================================
    eps_vars = Dict(Str, Array, input_change=True)
    def _eps_vars_default(self):
        return { 'e': [0, 1] }

    evar_lst = Property()
    def _get_evar_lst(self):
        ''' sort entries according to var_names.'''
        return [ self.eps_vars[ nm ] for nm in self.evar_names ]

    evar_names = Property(depends_on='eps_vars')
    @cached_property
    def _get_evar_names(self):
        evar_keys = list(self.eps_vars.keys())
        return [nm for nm in self.var_names if nm in evar_keys ]

    evar_str = Property()
    def _get_evar_str(self):
        s_list = ['%s = [%g, ..., %g] (%d)' % (name, value[0], value[-1], len(value))
                  for name, value in zip(self.evar_names, self.evar_lst)]
        return string.join(s_list, '\n')

    # convenience property to specify a single control variable without
    # the need to send a dictionary
    e_arr = Property
    def _set_e_arr(self, e_arr):
        '''Get the first free argument of var_names and set it to e vars
        '''
        self.eps_vars[self.var_names[0]] = e_arr

    # ===========================================================================
    # Specification of parameter value / distribution
    # ===========================================================================

    theta_vars = Dict(input_change=True)

    _theta_vars = Property(depends_on='theta_vars')
    @cached_property
    def _get__theta_vars(self):
        _theta_vars = {}
        for key, value in list(self.theta_vars.items()):

            # type checking
            is_admissible = False
            for admissible_type in [float, int, RV]:
                if isinstance(value, admissible_type):
                    is_admissible = True
            if not is_admissible:
                raise TypeError('bad type of theta variable %s' % key)

            # type conversion
            if isinstance(value, int):
                value = float(value)

            _theta_vars[key] = value
        return _theta_vars

    tvar_lst = Property()
    def _get_tvar_lst(self):
        '''sort entries according to var_names
        '''
        return [ self._theta_vars[ nm ] for nm in self.tvar_names ]

    tvar_names = Property
    def _get_tvar_names(self):
        '''get the tvar names in the order given by the callable'''
        tvar_keys = list(self._theta_vars.keys())
        return np.array([nm for nm in self.var_names if nm in tvar_keys ], dtype=str)

    tvar_str = Property()
    def _get_tvar_str(self):
        s_list = ['%s = %s' % (name, str(value))
                  for name, value in zip(self.tvar_names, self.tvar_lst)]
        return string.join(s_list, '\n')

    # number of integration points
    n_int = Int(10, input_change=True)

    # count the random variables
    n_rand_vars = Property
    def _get_n_rand_vars(self):
        dt = list(map(type, self.tvar_lst))
        return dt.count(RV)

    # get the indexes of the random variables within the parameter list
    rand_var_idx_list = Property(depends_on='theta_vars, recalc')
    @cached_property
    def _get_rand_var_idx_list(self):
        dt = np.array(list(map(type, self.tvar_lst)))
        return np.where(dt == RV)[0]

if __name__ == '__main__':
    fr = FunctionRandomization(q=lambda eps, theta : eps * theta,
                               eps_vars=dict(eps=[1.0]),
                               theta_vars=dict(theta=1.0))
    print('n_rand_vars', fr.n_rand_vars)
