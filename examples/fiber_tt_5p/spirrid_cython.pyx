import numpy as np
cimport numpy as np
ctypedef np.double_t DTYPE_t
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def mu_q(np.ndarray[DTYPE_t, ndim=1] e_arr,np.ndarray[DTYPE_t, ndim=1] E_mod_flat,np.ndarray[DTYPE_t, ndim=1] theta_flat,np.ndarray[DTYPE_t, ndim=1] lambd_flat,np.ndarray[DTYPE_t, ndim=1] xi_flat,np.ndarray[DTYPE_t, ndim=1] A_flat):
    cdef double mu_q
    cdef double lambd, xi, E_mod, theta, A, eps, dG, q
    cdef int i_lambd, i_xi, i_E_mod, i_theta, i_A
    cdef np.ndarray mu_q_arr = np.zeros_like( e_arr )
    for i_eps from 0 <= i_eps < 40:
        eps = e_arr[i_eps]
        mu_q = 0
        dG = 1.0000000000000000818030539140313095458623138256371021270751953125e-05
        for i from 0 <= i < 100000:
            lambd = lambd_flat[i]
            xi = xi_flat[i]
            E_mod = E_mod_flat[i]
            theta = theta_flat[i]
            A = A_flat[i]
            
            eps_ = ( eps - theta * ( 1 + lambd ) ) / ( ( 1 + theta ) * ( 1 + lambd ) )
            # Computation of the q( ... ) function
            if eps_ < 0 or eps_ > xi:
                q = 0.0
            else:
                q = E_mod * A * eps_
            
            mu_q += q * dG

        mu_q_arr[i_eps] = mu_q
    return mu_q_arr

