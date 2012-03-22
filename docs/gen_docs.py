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
# Created on Dec 21, 2011 by: rch


from etsproxy.traits.api import \
    HasTraits, Instance, Str, Property, cached_property, \
    Enum, List
from etsproxy.traits.ui.api import \
    View, Item

from examples.fiber_tt_2p import fiber_tt_2p
from examples.fiber_tt_5p import fiber_tt_5p
from examples.fiber_po_8p import fiber_po_8p

import os.path
import shutil
import fnmatch

SRC_DIR = 'source'

HOME_DIR = os.path.expanduser("~")
# output directory for the documentation
DOCS_DIR = os.path.join(HOME_DIR, '.spirrid')
# output directory for the documentation
BUILD_DIR = os.path.join(DOCS_DIR, 'build')
# output directory for the example documentation
EX_BUILD_DIR = os.path.join(BUILD_DIR, 'examples')
# output directory for the example documentation
EX_CACHE_DIR = os.path.join(DOCS_DIR, 'examples')
# build directory
HTML_DIR = os.path.join(DOCS_DIR, 'html')

class GenExampleDoc(HasTraits):

    header = Str('''
Comparison of sampling structure
================================

The different types of sampling for sample size 100. Both variables are randomized with 
normal distribution. 
The exact solution is depicted with the black line. The gray lines indicate the sampling. 
The response diagram correspond to the sampling types (left to right):

Regular grid of random variables
Grid of constant probabilities8
Monte Carlo sampling
Latin Hypercube Sampling 
    ''')

    demo_module = fiber_tt_2p

    #===========================================================================
    # Derived traits
    #===========================================================================
    demo_object = Property(depends_on = 'demo_module')
    @cached_property
    def _get_demo_object(self):
        dm = self.demo_module
        return dm.create_demo_object()

    qname = Property(depends_on = 'demo_module')
    @cached_property
    def _get_qname(self):
        return self.demo_object.get_qname()

    ex_build_dir = Property(depends_on = 'demo_module')
    @cached_property
    def _get_ex_build_dir(self):
        # check if the directory exists
        out_dir = os.path.join(EX_BUILD_DIR, self.qname)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        return out_dir

    ex_cache_dir = Property(depends_on = 'demo_module')
    @cached_property
    def _get_ex_cache_dir(self):
        # check if the directory exists
        out_dir = os.path.join(EX_CACHE_DIR, self.qname)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        return out_dir

    fig_cache_dir = Property()
    @cached_property
    def _get_fig_cache_dir(self):
        # check if the directory exists
        out_dir = os.path.join(self.ex_cache_dir, 'fig')
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        return out_dir

    rst_file_name = Property(depends_on = 'demo_module')
    @cached_property
    def _get_rst_file_name(self):
        return os.path.join(self.ex_cache_dir, 'index.rst')

    def generate_examples_sampling_structure(self):
        dobj = self.demo_object
        dobj.set(fig_output_dir = self.ex_cache_dir, show_output = False,
                 dpi = 70,
                 save_output = True, plot_mode = 'figures')
        dobj.sampling_structure()

    def generate_examples_sampling_efficiency(self):
        dobj = self.demo_object
        dobj.set(fig_output_dir = self.ex_cache_dir, show_output = False,
                 dpi = 70,
                 save_output = True, plot_mode = 'figures')
        dobj.sampling_efficiency()

    def generate_examples_language_efficiency(self):
        dobj = self.demo_object
        dobj.set(fig_output_dir = self.ex_cache_dir, show_output = False,
                 dpi = 70,
                 save_output = True, plot_mode = 'figures')
        dobj.codegen_language_efficiency()

    def generate_examples(self):
        self.generate_examples_sampling_structure()
        self.generate_examples_sampling_efficiency()
        self.generate_examples_language_efficiency()
    def generate_html(self):

        print 'generating documentation for', self.qname, '...'

        rst_text = '''
================================
Parametric study for %s
================================
        ''' % self.qname

        dobj = self.demo_object

        if dobj.s.q.__doc__ != None:
            rst_text += dobj.s.q.__doc__

        rst_text += self.header

        for st in dobj.sampling_types:
            rst_text += '''
            
.. image:: %s_%s.png
    :width: 24%%

            ''' % (self.qname, st)

        for st in dobj.sampling_types:
            rst_text += '''
                
.. image:: %s_sampling_%s.png
    :width: 24%%
    
            ''' % (self.qname, st)

        rst_text += '\nFollowing spirrid configuration has been used to produce the sampling figures:\n\n'
        rst_text += '\n>>> print demo_object\n' + str(dobj.s) + '\n'

        rst_text += '''
Comparison of execution time for different sampling types
=========================================================
Execution time evaluated for an increasing number of sampling points n_sim:
'''
        for basename in dobj.fnames_sampling_efficiency:
            rst_text += '''
        
.. image:: %s
    :width: 100%%

            ''' % basename
            print 'written file %s' % basename

        rst_text += '\n'

        rst_text += '''
Comparison of efficiency for different code types
=========================================================
Execution time evaluated for an numpy, weave and cython code:
'''
        for basename in dobj.fnames_language_efficiency:
            rst_text += '''
            
.. image:: %s
    :width: 100%%

            ''' % basename
            print 'written file %s' % basename

        rst_text += '\n'

        print 'writing rst file %s' % self.rst_file_name

        rst_file = open(self.rst_file_name, 'w')
        rst_file.write(rst_text)
        rst_file.close()

class GenDoc(HasTraits):
    '''
    Configuration of the document generation using sphinx.
    '''
    demo_modules = [fiber_tt_2p] #, fiber_tt_5p, fiber_po_8p]

    build_dir = Property()
    @cached_property
    def _get_build_dir(self):
        # check if the directory exists
        out_dir = os.path.join(BUILD_DIR)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        return out_dir

    ex_build_dir = Property()
    @cached_property
    def _get_ex_build_dir(self):
        # check if the directory exists
        out_dir = os.path.join(EX_BUILD_DIR)
        return out_dir
    
    ex_cache_dir = Property()
    @cached_property
    def _get_ex_cache_dir(self):
        # check if the directory exists
        out_dir = os.path.join(EX_CACHE_DIR)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        return out_dir
    
    html_dir = Property(depends_on = 'build_mode')
    def _get_html_dir(self):
        return HTML_DIR

    html_server = 'root@mordred.imb.rwth-aachen.de:/var/www/docs/spirrid'

    method_dispatcher = {'all' : 'generate_examples',
                         'sampling_structure' : 'generate_examples_sampling_structure',
                         'sampling_efficiency' : 'generate_examples_sampling_efficiency',
                         'language_efficiency' : 'generate_examples_language_efficiency',
                         }

    genexdoc = Property(List)
    @cached_property
    def _get_genexdoc(self):
        return [ GenExampleDoc(demo_module = demo) 
                for demo in self.demo_modules ]

    def generate_examples(self, kind = 'all'):
        method_name = self.method_dispatcher[kind]
        for ged in self.genexdoc:
            getattr(ged, method_name)()

    def generate_examples_index(self):

        # remove the old index.rst 
        rst_file_name = os.path.join(self.ex_cache_dir, 'index.rst')       
        if os.path.exists(rst_file_name):        
            os.remove(rst_file_name)
            
        rst_text = '''
========
Examples
========

.. toctree::
   :maxdepth: 2
   
'''
        for path, dirs, files in os.walk(self.ex_cache_dir):
            for f in fnmatch.filter(files, '*.rst'):

                abspath = os.path.join(path, f)
                relpath = os.path.relpath(abspath, self.ex_cache_dir)
                rst_text += '   %s/index\n' % os.path.dirname(relpath)
        print rst_text

        rst_file = open(rst_file_name, 'w')
        rst_file.write(rst_text)
        rst_file.close()

    def generate_html(self):

        shutil.rmtree(self.build_dir)
        shutil.copytree(SRC_DIR, self.build_dir)

        for ged in self.genexdoc:
            ged.generate_html()

        self.generate_examples_index()

        shutil.copytree(self.ex_cache_dir, self.ex_build_dir)

        sphings_cmd = 'sphinx-build -b html -E %s %s' % \
            (self.build_dir, self.html_dir)
        os.system(sphings_cmd)

    def push_html(self):
        '''
        Push the documentation to the server.
        '''
        rsync_cmd = 'rsync -av --delete %s/ %s' % (self.html_dir, self.html_server)
        os.system(rsync_cmd)

if __name__ == '__main__':

    gd = GenDoc(demo_modules = [
                                fiber_tt_2p
                                #fiber_tt_5p,
                                #fiber_po_8p
                                ]
                )

    gd.generate_examples(kind = 'sampling_structure')
    gd.generate_html()
    gd.push_html()
