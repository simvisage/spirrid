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

from etsproxy.traits.api import \
    HasStrictTraits, WeakRef, Bool, on_trait_change, \
    Event

#===============================================================================
# Generator of the integration code 
#===============================================================================
class CodeGen(HasStrictTraits):
    '''
        Base class for generators of the integration code.
        
        The code may be scripted or compiled depending on the choice 
        of the class. 
    '''
    # backward link to the spirrid object
    spirrid = WeakRef

    recalc = Event

    #===========================================================================
    # Consfiguration of the algorithm
    #===========================================================================
    implicit_var_eval = Bool(False, codegen_option = True)

    #===========================================================================
    # Propagate the change to the spirrid
    #===========================================================================
    @on_trait_change('+codegen_option')
    def set_codegen_option_changed(self):
        self.spirrid.codegen_option = True

