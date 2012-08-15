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
from scipy.stats.distributions import norm
import numpy as np
import pylab as p # import matplotlib with matlab interface
import platform
import time

if platform.system() == 'Linux':
    sysclock = time.time
elif platform.system() == 'Windows':
    sysclock = time.clock

def main():
    # set the mean and standard deviation of la and xi
    m_la, std_la = 10.0, 1.0
    m_xi, std_xi = 1.0, 0.1
    # construct objects representing normal distributions
    pdistrib_la = norm(loc=m_la, scale=std_la)
    pdistrib_xi = norm(loc=m_xi, scale=std_xi)
    # get operators for probability density functions
    g_la = pdistrib_la.pdf
    g_xi = pdistrib_xi.pdf
    # number of integration points set equal for both variables
    n_i = 10
    # generate midpoints of n_i intervals in the range (-1,1)
    theta_arr = np.linspace(-(1.0 - 1.0 / n_i),
                              1.0 - 1.0 / n_i , n_i)
    # scale up theta_arr to cover the random domains
    theta_la = m_la + 4 * std_la * theta_arr
    theta_xi = m_xi + 4 * std_xi * theta_arr
    # get the size of the integration cells
    d_la = (8 * std_la) / n_i
    d_xi = (8 * std_xi) / n_i

    def Heaviside(x):
        """Heaviside function."""
        return x >= 0.0

    def q_eq13(eps, la, xi):
        """Response function of a single fiber."""
        return la * eps * Heaviside(xi - eps)

    def mu_q_eq13_loops(eps_arr):
        """Loop-based calculation of mean values."""
        mu_q_arr = np.zeros_like(eps_arr)
        for i, eps in enumerate(eps_arr):
            mu_q = 0.0
            for la in theta_la:
                for xi in theta_xi:
                    dG = g_la(la) * g_xi(xi) * d_la * d_xi
                    mu_q += q_eq13(eps, la, xi) * dG
            mu_q_arr[i] = mu_q
        return mu_q_arr

    # construct an array of control strains
    eps_arr = np.linspace(0, 1.2, 80)

    # construct an array of control strains
    eps_arr = np.linspace(0, 1.2, 80)

    start_time = sysclock()
    mu_q_arr = mu_q_eq13_loops(eps_arr)
    print 'loop-based: elapsed time', sysclock() - start_time


    dG_la = g_la(theta_la) * d_la
    dG_xi = g_xi(theta_xi) * d_xi
    dG_grid = dG_la[:, np.newaxis] * dG_xi[np.newaxis, :]

    def mu_q_eq13(eps):
        """Loopless calculation of mean value."""
        q_grid = q_eq13(eps,
                         theta_la[:, np.newaxis],
                         theta_xi[np.newaxis, :])
        q_dG_grid = q_grid * dG_grid
        return np.sum(q_dG_grid)

    mu_q_eq13_vct = np.vectorize(mu_q_eq13)
    # eps_arr from line reused here
    start_time = sysclock()
    mu_q_arr = mu_q_eq13_vct(eps_arr)
    print 'Regular grid of random variables: elapsed time', sysclock() - start_time

    p.subplot(121)
    p.plot(eps_arr, mu_q_arr, color='blue', label='Tgrid')
    p.subplot(122)
    expander = np.ones((n_i, n_i), dtype=int)
    p.plot((theta_la[np.newaxis, :] * expander).flatten(),
            (theta_xi[:, np.newaxis] * expander).flatten(),
            'b.', label='Tgrid')


    def get_mu_q_fn(q, dG, *theta):
        """Return a method evaluating the mean of q()."""
        def mu_q(eps):
            Q_dG = q(eps, *theta) * dG
            return np.sum(Q_dG)
        return np.vectorize(mu_q)

    # SAMPLING: (*\label{line:TGrid_example_start}*)
    # ... reuse dG_grid and theta (lines (*\ref{line:theta_la}*), (*\ref{line:theta_xi}*) and (*\ref{line:g_la}*)-(*\ref{line:dG_grid}*))

    # INSTANTIATION:
    mu_q_fn = get_mu_q_fn(q_eq13, dG_grid,
                          theta_la[:, np.newaxis],
                          theta_xi[np.newaxis, :])

    # CALCULATION:
    mu_q_arr = mu_q_fn(eps_arr)

    # SAMPLING:
    # equidistant sampling probabilities (see Eq. (*\ref{eq:p_grid_sampling}*))
    j_arr = np.arange(1, n_i + 1)
    pi_arr = (j_arr - 0.5) / n_i
    # use ppf (percent point function) to get sampling points
    # (pdistrib_la and pdistrib_xi was defined at lines (*\ref{line:pdistrib_la}*), (*\ref{line:pdistrib_xi}*))
    theta_la = pdistrib_la.ppf(pi_arr)
    theta_xi = pdistrib_xi.ppf(pi_arr)
    # get the total number of integration points
    # for 2 random variaables with equal n_i
    n_sim = n_i ** 2

    # INSTANTIATION:
    mu_q_fn = get_mu_q_fn(q_eq13, 1.0 / n_sim,
                          theta_la[:, np.newaxis],
                          theta_xi[np.newaxis, :])

    start_time = sysclock()
    # CALCULATION:
    mu_q_arr = mu_q_fn(eps_arr)
    print 'Grid of constant probabilities: elapsed time', sysclock() - start_time

    p.subplot(121)
    p.plot(eps_arr, mu_q_arr, color='cyan', label='Pgrid')
    p.subplot(122)
    p.plot((theta_la[np.newaxis, :] * expander).flatten(),
            (theta_xi[:, np.newaxis] * expander).flatten(),
            'co', label='Pgrid')


    # SAMPLING:
    # generate n_sim random realizations
    # using pdistrib objects (lines (*\ref{line:pdistrib_la}*), (*\ref{line:pdistrib_xi}*))
    theta_la_rvs = pdistrib_la.rvs(n_sim)
    theta_xi_rvs = pdistrib_xi.rvs(n_sim)

    # INSTANTIATION:
    mu_q_fn = get_mu_q_fn(q_eq13, 1.0 / n_sim,
                          theta_la_rvs, theta_xi_rvs)
    start_time = sysclock()
    # CALCULATION:
    mu_q_arr = mu_q_fn(eps_arr)
    print 'Monte-Carlo: elapsed time', sysclock() - start_time

    p.subplot(121)
    p.plot(eps_arr, mu_q_arr, color='red', label='Monte-Carlo')
    p.subplot(122)
    p.plot(theta_la_rvs, theta_xi_rvs, 'rD', label='Monte-Carlo')


    # SAMPLING: (*\label{line:LHS_example_start}*)
    # sampling probabilities (see Eq. (*\ref{eq:LHS_sampling}*)), n_sim as above
    j_arr = np.arange(1, n_sim + 1)
    pi_arr = (j_arr - 0.5) / n_sim
    # get the ppf values (percent point function)
    # using pdistrib objects defined at lines (*\ref{line:pdistrib_la}*), (*\ref{line:pdistrib_xi}*)
    theta_la_ppf = pdistrib_la.ppf(pi_arr)
    theta_xi_ppf = pdistrib_xi.ppf(pi_arr)
    # make random permutations of both arrays to diminish
    # correlation (not necessary for one of the random variables)
    theta_la = np.random.permutation(theta_la_ppf)
    theta_xi = theta_xi_ppf

    # INSTANTIATION:
    mu_q_fn = get_mu_q_fn(q_eq13, 1.0 / n_sim,
                          theta_la, theta_xi)
    start_time = sysclock()
    # CALCULATION:
    mu_q_arr = mu_q_fn(eps_arr)
    print 'Grid of constant probabilities: elapsed time', sysclock() - start_time

    p.subplot(121)
    p.plot(eps_arr, mu_q_arr, color='green', label='LHS')
    p.subplot(122)
    p.plot(theta_la, theta_xi, 'go', label='LHS')

    p.subplot(121)
    p.legend()
    p.xlabel('$\\varepsilon$', fontsize=24)
    p.ylabel('$q$', fontsize=24)


    ############################## Discretization grids ########################
    p.subplot(122)
    p.ylabel('$\\theta_{\\xi}$', fontsize=24)
    p.ylim(0.5, 1.5)
    p.xlim(5, 15)
    p.xlabel('$\\theta_{\lambda}$', fontsize=24)
    p.legend()

    p.show()

if __name__ == '__main__':
    main()
