"""
variational.py
@author: Alex Hickey

This module aims to compute the ground state of the Bose-Hubbard model
by using the variational principle. The parameter t corresponds to the hopping 
amplitude and the parameter mu corresponds to the chemical potential. Each of 
these parameters are in units of the on-site interaction energy.
"""

#Import modules
import numpy as np
import scipy.optimize
import bdsearch

#Set the maximum number of bosons per site
N = 10

#Define arrays to call in functions
n_arr = np.arange(N+1)
nC2_arr = 0.5*n_arr*(n_arr-1.0)
sqr_arr = np.sqrt(n_arr)


def compute_psi(state):
    '''
    Compute the superfluid order parameter <a> for a given state.

    Args:
        state: Array of coefficients in the occupation number basis
        
    Return:
        psi: Superfluid order parameter
    '''
    
    #Note that result must be normalized as minimization routine does
    #not preserve norm.
    return np.sum(state*np.roll(state*sqr_arr,-1))/np.sum(state*state)


def expH(state,t,mu):
    '''
    Compute the expectation value of the mean-field Hamiltonian for a given
    state.
    
    Args:
        State: Array of coefficients in the occupation number basis
        t: Hopping amplitude
        mu: Chemical potential
        
    Return:
        <H>: Expected value of the Hamiltonian in the given state
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
    Calculate order parameter which minimizes the free energy using the
    scipy.optimize.minimize function.
    
    Args:
        t: Hopping amplitude
        mu: Chemical potential
        tol: Tolerance for convergence
        
    Return:
        state: State that minimizes <H>
    
    '''
    
    #Initial guess is uniform superposition
    y0 = np.ones(N+1)/np.sqrt(N+1)
    
    #Minimize <H>
    res = scipy.optimize.minimize(expH,y0,args = (t,mu),tol=tol)
    
    return res.x



def find_psi(t,mu,tol = 1e-13):
    '''
    Find the value of the superfluid order parameter using the
    variational principle.

    Args:
        t: Hopping amplitude
        mu: Chemical potential
        tol: Tolerance for convergence
        
    Return:
        psi: Superfluid order parameter
    '''
    
    groundstate = ground(t,mu,tol=tol)
        
    return compute_psi(groundstate)


#List of hopping amplitudes to iterate over
tlist = np.linspace(0.001,0.2,999)

def bd(mu):
    '''
    Search for the phase boundary for a given mu, by iterating throught
    hopping amplitudes.
    
    Args:
        mu: Chemical potential
        
    Return:
        bd_point: Critical hopping amplitude
        
    '''
    
    
    return bdsearch.bd(mu,tlist,find_psi)

###############################################################################
#Testing framework
    
import unittest

class TestVariational(unittest.TestCase):
    '''
    Unit testing class for functions in the variational.py module
    '''
    
    def test_insulator(self):
        '''
        Test that the order parameter is zero for a known insulating ground
        state in the paramater space (t=0.05,mu=0.5).
        '''
        
        #Set system parameters for a known insulator
        t, mu = 0.05, 0.5
        
        #Set tolerance
        tol = 1e-7
        
        #Compute order parameter
        psi = find_psi(t,mu)
        
        self.assertTrue(np.abs(psi) < tol) 
    

#Run tests if in main namespace
if __name__ == '__main__':
    unittest.main(argv=[''],verbosity=2,exit=False)
    