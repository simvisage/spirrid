========
SPIRRID
========

The **SPIRRID** package is the part of the project SIMVISAGE 
(https://github.com/simvisage/spirrid).

Documentation of the package generated using sphinx
===================================================

http://mordred.imb.rwth-aachen.de/docs/spirrid/

This project is developed on Linux (Kubuntu, Suse) ETS version < 4.0.
note for ets >= 4.0: 
http://blog.enthought.com/open-source/ets-4-0-released/

Installation instructions 
=========================

WINDOWS
-------

install the Enthought Python Distribution (EPD) following
the instructions at

http://www.enthought.com/products/epd.php

UBUNTU
------

install Enthought Tool Suite (ETS) and additional utilities::

	$ sudo apt-get install ipython python-traitsgui python-scipy \
  		python-matplotlib mayavi2 cython python-numexpr


spirrid/examples/demo.py
========================
 
To test spirrid package on prepared examples run::

	$ python demo.py

you get the user interface to run one of examples described in the last
section this document.


spirrid/
========

This folder contains tools for random variable domain sampling, code generation and
numerical multidimensional statistical integration.


spirrid/pdistrib (library of statistical distributions)
================

The package provides a traited wrapper for the scipy distributions.


spirrid/util
============

This folder contains customized (extended) source code (enthought, scipy, numpy)
needed for running spirrid.


spirrid/examples/
=================

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

