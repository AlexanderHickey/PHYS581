"""
exact_diag.py
@author: Alex Hickey

This module aims to compute the ground state of the Bose-Hubbard model
by iterating through an exact diagonalization process until self-consistency
is obtained. The parameter t corresponds to the hopping amplitude and the 
parameter mu corresponds to the chemical potential. Each of these parameters
are in units of the on-site interaction energy.
"""

#Import modules
import numpy as np
import bdsearch

#Set maximum number of bosons per site
N = 10


def construct_hamiltonian(psi,t,mu):
    '''
    Construct MF Hamiltonian in the occupation number basis.
    
    Args:
        psi: Superfluid order parameter
        t: Hopping amplitude
        mu: Chemical potential
        
    Return:
        H: mean field Hamiltonian matrix 
    '''
    
    H = np.zeros((N+1, N+1))

    for i in range(0, N+1):
        
        #Diagonal components
        H[i, i] = (i*(i-1)/2-mu*i+t*psi*psi)/2.0
        
        #Upper-diagonal components
        if i != N:
            
            H[i,i+1] = -t*psi*np.sqrt(i+1)
        
    return H+H.T

def groundstate(H):
    '''
    Calculate the minimum eigenvalue and corresponding eigenvector of a 
    Hermitian matrix.
    
    Args:
        H: Hermitian matrix
        
    Return:
        E0: Lowest eigenvalue
        state: Corresponding eigenvector
    '''
    
    #Compute spectrum
    eigvals, eigvecs = np.linalg.eigh(H)
    
    return eigvals[0], eigvecs[:,0]


def compute_psi(state):
    '''
    Compute the superfluid order parameter <a> for a given state.

    Args:
        State: Array of coefficients in the occupation number basis
        
    Return:
        psi: Superfluid order parameter
    '''
    
    return np.sum([state[j]*state[j+1]*np.sqrt(j+1) for j in range(N)])
    


def find_psi(t,mu,tol = 1e-13):
    '''
    Find the value of the superfluid order parameter by iterating the
    exact-diaganilization process.

    Args:
        t: Hopping amplitude
        mu: Chemical potential
        tol: Tolerance for convergence
        
    Return:
        psi: Superfluid order parameter
    '''
    
    
    #Initial guess for psi
    psi0 = 1e-3
    
    #Compute ground state given initial guess
    E, state = groundstate(construct_hamiltonian(psi0,t,mu))
    
    #Update psi
    psi = compute_psi(state)
    
    #Iterate through process until self-consistent
    while np.abs(psi - psi0) > tol:

        #Update psi
        psi0 = psi
        
        #Compute updated ground state
        E, state = groundstate(construct_hamiltonian(psi0,t,mu))
        
        #Compute psi for new state
        psi = compute_psi(state)
        
    return psi

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

class TestExactDiag(unittest.TestCase):
    '''
    Unit testing class for functions in the exact_diag.py module
    '''
    
    def test_insulator(self):
        '''
        Test that the order parameter is zero for a known insulating ground
        state in the paramater space (t=0.05,mu=0.5).
        '''
        
        #Set system parameters for a known insulator
        t, mu = 0.05, 0.5
        
        #Set tolerance
        tol = 1e-13
        
        #Compute order parameter
        psi = find_psi(t,mu,tol=tol)
        
        self.assertTrue(np.abs(psi) < tol) 
    

#Run tests if in main namespace
if __name__ == '__main__':
    unittest.main(argv=[''],verbosity=2,exit=False)





