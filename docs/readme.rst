Source directory for documentation generation
=============================================

The generated documentation is available online at

http://simvisage.com/docs/spirrid
 
In order to generate the
documentation you need to install sphinx utility
(http://sphinx.pocoo.org). On ubuntu 
it can be installed by issuing
::

    $ apt-get install python-sphinx 

Then, the **gen_docs.py** script can be run to 
generate the documentation. The root directory
of the **spirrid** package must be contained in the 
PYTHONPATH environment variable. 
::

    $ cd docs
    $ export PYTHONPATH="../"
    $ python gen_docs.py

Note that the **gen_docs.py** script starts the 
efficiency studies of all implemented sampling schemes
on your computer that may take up to
one hour to construct all the diagrams. 

The **GenDoc** object can be configured to generate
only a part of the documentation. At the bottom of the
**gen_docs.py** script you will find the code for 
the full generation: 
::

    gd = GenDoc(demo_modules = [
                                fiber_tt_2p,
                                fiber_tt_5p,
                                fiber_po_8p
                                ]
                )

    gd.generate_examples(kind = 'all')
    gd.generate_html()

The amount of generated documentation can be limited by avoiding
some of the documentation components, either the call to the method
**generate_examples()**, or setting the example kind to
one of the options

 * sampling_structure 
 * sampling_efficiency, 
 * language_efficiency

or commenting out one or more of the response functions
 * fiber_tt_2p - two parametric response function
 * fiber_tt_5p - five parametric response function
 * fiber_po_8p - eight parametric response function
	
The generated documentation is located in the directory
::

    $HOME/.spirrid/html/index.html
 

