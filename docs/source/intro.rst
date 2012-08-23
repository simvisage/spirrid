============
Introduction
============

The package implements the integration of the function 
with parameters that can be prescribed random using arbitrary
probabilistic distributions.


Estimation of statistical moments of a function with independent random variables
--------------------

SPIRRID enables estimation of the statistical moments of a random
problem :math:`Q` given as a function of a control variable
:math:`\varepsilon` and of random variables :math:`\theta_1 \ldots \theta_m`
constituting the random domain :math:`\mathbf{\Theta}`:

.. math::
	Q  = q\left( {\varepsilon;{\theta_1},\ldots,{\theta_m}} \right).
	:label: generic_rf

The :math:`k`-th raw statistical moment of such a random problem is given as

.. math::
	\mu_k( \varepsilon ) =
	\displaystyle\int_{ \mathbf{\Theta}}^{}
	\left[
	q{\left( \varepsilon;{\mathbf \theta} \right)}
	\right]^k
	g( \mathbf{\theta} ) \, \mathrm{d}
	\mathbf{\theta}.
	:label:  mu_i1
	
	
Since only independent random variables are considered here, 
the joint probability density function :math:`g(\mathbf{\theta})` 
(PDF) of the random vector :math:`\mathbf{\theta}` can be replaced 
with the product of univariate marginal densities

.. math::
	\mu_k( \varepsilon ) =
	\displaystyle\int_{\Theta_1}^{} \ldots
	\displaystyle\int_{\Theta_{m}}^{}
	\left[
	q{\left( \varepsilon;{\mathbf \theta} \right)}
	\right]^k
	g_1(\theta_1) \ldots g_{m}( \theta_m )
	\;
	\mathrm{d}{\theta_1} \ldots \mathrm{d}{\theta_{m}}.
	:label: mu_i2
	
The integration is to be performed numerically as a summation of discrete values
distributed over the discretized random domain

.. math::
    \mu_k(\varepsilon)  =  
    \displaystyle\sum_{\Theta_1}^{}\,  \ldots
	\displaystyle\sum_{\Theta_m}^{}\,
	{\underbrace{
	\left[ q\left( \varepsilon;{\theta_1 \ldots \theta_m} \right)
	\right]^k
	}_{Q^k}
	\underbrace{
	{\Delta G_1(\theta_1)} \ldots {\Delta G_{m}(\theta_m)}
	}_{\Delta G}},
    :label: mu_i3
	
where :math:`\Delta G_i(\theta_i)` denote the weighting factors
that depend on the particular type of sampling as specified below.
The distribution of the integration points :math:`\Theta_m` within
the random domain can be expressed as

.. math::
	\Theta_i = [\theta_{ij}, j \in 1\ldots n_i], \; i \in 1\ldots m,
	:label: sampling_points
	
where :math:`n_i` is the number of discretization points 
for the :math:`i`-th variable and :math:`j` counts the 
disretization point along a variable.


Illustrative example
--------------------

Given a function with two random parameters with normal probabilistic distribution, 
the task is to evaluate the average response of an ensemble of function instantiations.

Let us consider the function

.. math::
	q( \varepsilon; \lambda, \xi) = \lambda \;\varepsilon
	\cdot
	H\left( \xi - \varepsilon \right).
	:label: eq_response_func

.. index:: examples; SPIRRID features

where the variables :math:`\lambda` and :math:`\xi` are considered random and normally distributed.
The function :math:`H(\eta)` represents the Heaviside function with values 0 for :math:`\eta < 0`
and 1 for :math:`\eta > 0`.
The mean response of the function is obtained using Eq. :eq:`mu_i3` as

.. math::
	    \mu_{q}(\varepsilon)  =  \sum_{\Theta_\lambda}^{}  \sum_{ \Theta_\xi }^{}
	{\underbrace
	    {q\left( \varepsilon; \lambda, \xi \right)}_Q}
	\;{
	\underbrace {
	g_\lambda g_\xi
	    \;
	   \Delta{\theta_\lambda} \Delta{\theta_\xi}
	  }_{\Delta G}
	} 
	:label: eq_mu_q

Graphically, the task can be displayed using the function with the indicated
random parameters on the left. The mean response and random samples of the function
are shown in the right diagram of the Figure.

The corresponding code delivering the mean estimates using the spirrid package
is constructed as follows:  
::

    from simvisage.spirrid import SPIRRID, RV, Heaviside
    import numpy as np
    import pylab as p

    def fiber_tt_2p(e, la, xi):
        ''' Response function of a single fiber '''
        return la * e * Heaviside(xi - e)

    # Construct the integration object
    s = SPIRRID(q = fiber_tt_2p, 
                e_arr = np.linspace(0, 0.1, 50),
                tvars = dict(la = RV('norm', 10.0, 1.0),
                             xi = RV('norm', 1.0, 0.1)))

    # plot the mean response against the control variable e_arr
    p.plot(s.e_arr, s.mu_q_arr)
    p.show()

.. index:: intro; SPIRRID features

Features
--------
The implementation of the SPIRRID is highly configurable and provides the following features:

*  The class SPIRRID can be configured for an arbitrary response function 
   q(e = [], theta = []). The function q(e, theta) must be a "callable" object and 
   must have one or more control variables e and one or more parameters theta.
 
*  The parameters and randomization are specified using the tvars trait attribute. 
   They are instances of the RV class representing a random variable that can be 
   associated with probabilistic distribution from scipy.stats.distribution package.
   
*  There are four sampling schemes that can be specified using the sampling_type
   trait attribute (see examples below). 

*  The execution of the integration may be done using the numpy implementation 
   or using a compiled C-code implementation that gets generated on demand for 
   the current response function and randomization scheme (see examples below). 

*  The control variable e can be n-dimensional, the range of the input array 
   is specified using the evars parameter of the SPIRRID class. The statistical 
   evaluation is performed for each combination of the entries contained in the range 
   of the control variables. 

*  The class SPIRRID can also calculate the variance along with the mean value. 
   It can be easily extended with the evaluation of further characteristics like 
   covariance or skewness. 

*  State dependency between the attributes of the SPIRRID object is maintained 
   automatically: If the input values and the configuration of the SPIRRID 
   have been modified, the results get modified on demand upon the next access 
   to the output values. 
