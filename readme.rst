========
SPIRRID
========

The **SPIRRID** package is the part of the project SIMVISAGE 
(https://github.com/simvisage/spirrid). Use the zip button 
to download the source code for testing and see the Examples section below. 
Examples are accompanying 
and extending the studies provided in the prepared paper 
*Using Python for scientific computing:
efficient and flexible evaluation of the statistical characteristics of functions with 
mutivariate random inputs, R. Chudoba, V. Sadilek, R. Rypl, and M. Vorechovsky, 
prepared for submission in CPC.*

Documentation of the package generated using sphinx
===================================================

http://mordred.imb.rwth-aachen.de/docs/spirrid/


Installation instructions 
=========================

Prerequisites
-------------

Windows, Linux and Mac
^^^^^^^^^^^^
The Enthought Python Distribution (EPD) is available in system independent form at

http://www.enthought.com/products/epd.php

*On windows, there is some Cython problem (pyximport). At this time, we don't 
have any simple solution. Due to this fact, it was removed from benchmark tests.*

*There is a commercial and academic version of EPD containing all required packages.
Free distribution of EPDFree does not contain all packages (mayavi, numexpr, cython).
These packages must be installed manually.*  
 
UBUNTU 10.04
^^^^^^^^^^^^

Enthought Tool Suite (ETS 3) and additional utilities can be installed using 
the standard package manager as::

	$ sudo apt-get install ipython python-traitsui python-scipy \
  		python-matplotlib mayavi2 cython
  		
*In order to make the comparison between numexpr and numpy efficiency
in the script examples.numexpr_test.numexpr_test
the python-numpexpr package must be installed separately as it is not
included in ubuntu 10.04 distribution.*

UBUNTU 11.04
^^^^^^^^^^^^
Enthought Tool Suite (ETS 4) and additional utilities are installed as::

    $ sudo apt-get install mayavi2 python-matplotlib \
        cython python-numexpr python-scipy

Other distributions
^^^^^^^^^^^^
For other systems and distributions use 
the description provided at and references there:

http://blog.enthought.com/open-source/ets-4-0-released/

Download and install
--------------------
Download and unzip the package from https://github.com/simvisage/spirrid.

Examples
========

To test spirrid package on prepared examples change to the top directory 
of the spirrid package  run::

	$ python examples/demo.py

you get the user interface to run one of examples described in the last
section this document.

In order to start the individual examples the top level directory of spirrid
package must be included in the PYTHONPATH environment 
variable or in the sys.path variable
of the executed script. 

Package structure
=================

spirrid/
--------

This folder contains tools for random variable domain sampling, code generation and
numerical multidimensional statistical integration.


spirrid/pdistrib (library of statistical distributions)
--------

The package provides a traited wrapper for the scipy distributions.

spirrid/docs
--------

Package generating the documentation from the source code 
and from the demonstration examples. 

spirrid/etsproxy
--------

Subsidiary package needed to support both ETS 3 and ETS 4 with changed import paths. 

spirrid/util
--------

This folder contains customized (extended) source code (enthought, scipy, numpy)
needed for running spirrid.


examples/
--------

The directories "fiber_*" provides the performance studies of the spirrid
integration tool. There are three types of response functions
tested:

* fiber_tt_2p/: fiber tensile test with 2 parameters 
  one strong discontinuity) 
* fiber_tt_5p/: fiber tensile test with 5 parameters
  one strong and one weak discontinuity
* fiber_po_8p/: fiber pullout test with 7 parameters
  one strong, one weak discontinuity 
  and nonlinear range within the response

There are two tests:

* masked_arrays/: testing of speeding up of evaluation of general function
  using numpy.ma.array
* numexpr/: testing of speeding up of evaluation of fiber_tt_5p fiber tensile 
  test with 5 parameters one strong and one weak discontinuity) using numexpr

And:

* script.py: simple python script, described in paper "Using Python for scientific
  computing: efficient and flexible evaluation of the statistical
  characteristics of functions with multivariate random inputs"

