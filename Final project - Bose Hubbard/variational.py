"""
variational.py
@author: Alex Hickey

This module aims to compute the ground state of the Bose-Hubbard model
by using the variational principle. The parameter t corresponds to the hopping 
amplitude and the parameter mu corresponds to the chemical potential. Each of 
these parameters are in units of the on-site interaction energy.
"""

import numpy as np
import scipy.optimize


#Set the maximum number of bosons per site
N = 10

#Define arrays to call in functions
n_arr = np.arange(N+1)
nC2_arr = 0.5*n_arr*(n_arr-1.0)
sqr_arr = np.sqrt(n_arr)


def compute_psi(state):
    '''
    Compute the superfluid order parameter <a>
    '''
    
    #return np.sum(state*np.roll(state,-1)*sqr_arr)/np.sum(state*state)
    return np.sum(state*np.roll(state*sqr_arr,-1))/np.sum(state*state)


def expH(state,t,mu):
    '''
    Compute the expectation value of the mean-field Hamiltonian for a given
    state.
    '''
    
    #Compute order parameter for given state
    psi = compute_psi(state)
    
    #Compute hopping contribution
    hop = -t*psi*psi
    
    #Compute on-site interaction contribution
    onsite = np.sum(state*state*nC2_arr)/np.sum(state*state)
    
    #Compute chemical potential contribution
    chem = -mu*np.sum(state*state*n_arr)/np.sum(state*state)
    
    return hop+onsite+chem



    
def ground(t,mu,tol = 1e-13):
    '''
    Calculate order parameter which minimizes the free energy.
    
    '''
    
    #Initial guess is uniform superposition
    y0 = np.ones(N+1)/np.sqrt(N+1)
    
    res = scipy.optimize.minimize(expH,y0,args = (t,mu),tol=tol)
    
    
    return res.x



def find_psi(t,mu,tol = 1e-13):
    '''
    Find the value of the superfluid order parameter through by
    exact-diaganilization iteration.
    
    
    '''
    
    groundstate = ground(t,mu,tol=tol)
        
    return compute_psi(groundstate)
    

print(find_psi(0.1,0.5))



