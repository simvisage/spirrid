=========
Examples
=========

The subdirectories "fiber_*" provides the performance studies of the spirrid
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

* script.py: simple python script, demonstrating several possible ways 
  how to implement the estimation of mean value of a multi-variate 
  random function. The script uses a two-parametric function with 
  a discontinuity (stress-strain response of a fiber loaded in tension). 
  Both parameters of the function are considered randomly distributed.
  
  The script shows a figure containing two diagrams stored in this directory
  with the name script_output.png:
   
  The left diagram 
  displays the obtained mean response of the random process for four 
  implemented sampling techniques indluding regular grids and Monte-Carlo 
  types of sampling. The right diagram visualizes the coverage of the random 
  domain with two random variables for the four applied sampling techniques.

  More detailed issues concerning the efficiency of the covered 
  sampling and implementation techniques are described in paper 
  *Using Python for scientific
  computing: efficient and flexible evaluation of the statistical
  characteristics of functions with multivariate random inputs*
  prepared for submission in CPC.

