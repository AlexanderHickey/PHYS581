"""
imag_time.py
@author: Alex Hickey

This module aims to compute the ground state of the Bose-Hubbard model
by using imaginary-time propagation. The parameter t corresponds to the hopping 
amplitude and the parameter mu corresponds to the chemical potential. Each of 
these parameters are in units of the on-site interaction energy.
"""

#Import modules
import numpy as np
import bdsearch

#Fix maximum number of bosons per site
N = 10

#Define arrays to call in functions
n_arr = np.arange(N+1)
sqr_arr = np.sqrt(n_arr)


def a(state):
    '''
    Act with the annihilation operator in the occupation number basis
    
    Args:
        state: Array of coefficients in the occupation number basis
        
    Return:
        a(state): Array of coefficients after acting with the annihilation
                  operator
    '''
    
    return np.roll(state*sqr_arr,-1)


def a_dag(state):
    '''
    Act with the creation operator in the occupation number basis
    
    Args:
        state: Array of coefficients in the occupation number basis
        
    Return:
        a(state): Array of coefficients after acting with the creation
                  operator
    '''
    
    return  sqr_arr*np.roll(state,1)


def compute_psi(state):
    '''
    Compute the superfluid order parameter <a> for a given state.

    Args:
        State: Array of coefficients in the occupation number basis
        
    Return:
        psi: Superfluid order parameter
    '''
    
    return np.sum(state*a(state))


def H(state,psi,t,mu):
    '''
    Takes a state in the occupation number basis of the form
    [c0,c1,...,cN] and acts with the Hamiltonian operator.
    
    Args:
        State: Array of coefficients in the occupation number basis
        psi: Superfluid order parameter
        t: Hopping amplitude
        mu: Chemical potential
        
    Return:
        H(state): Array of coefficients after acting with the Hamiltonian
                  operator
    '''
    
    #Hopping contribution
    newstate = -t*psi*(a(state)+a_dag(state))
    
    #Everything else
    newstate += (0.5*n_arr*(n_arr-1.0)-mu*n_arr+t*psi*psi)*state
    
    return newstate


def RK5step(y,psi,t,mu,h=.07):
    '''
    Takes a step forward in the RK5 routine for the imaginary-time
    Schrodinger equation.
    
    Args:
        y: Array of coefficients in the occupation number basis
        psi: Superfluid order parameter
        t: Hopping amplitude
        mu: Chemical potential
        h: Time step
        
    Return:
        newstate: Array of coefficients after taking a timestep h
    '''
        
    #Compute RK5 coefficients        
    k1 = -h*H(y,psi,t,mu)
    k2 = -h*H(y+k1/4.0,psi,t,mu)
    k3 = -h*H(y+(3/32)*k1+(9/32)*k2,psi,t,mu)
    k4 = -h*H(y+(1932/2197)*k1-(7200/2197)*k2+(7296/2197)*k3,psi,t,mu)
    k5 = -h*H(y+(439/216)*k1-8*k2+(3680/513)*k3-(845/4104)*k4,psi,t,mu)
    k6 = -h*H(y-(8/27)*k1+2*k2-(3544/2565)*k3+(1859/4104)*k4-(11/40)*k5,psi,t,mu)
    
    #Take timestep
    y5 = y+(16/135)*k1+(6656/12825)*k3+(28561/56430)*k4-(9/50)*k5+(2/55)*k6
    
    #Result must be re-normalized!
    return y5/np.linalg.norm(y5)



def find_gnd(t,mu,tol = 1e-6,max_it=300000):
    '''
    Compute the ground state using imaginary time propagation by iterating 
    the RK5 step function.
    
    Args:
        t: Hopping amplitude
        mu: Chemical potential
        tol: Tolerance for convergence
        max_it: Maximum number of iterations before breaking from loop.
        
    Return:
        groundstate: Ground state for the given parameters
    '''

    #Initial guess is a uniform superposition
    y0 = np.ones(N+1)/np.sqrt(N+1)
    psi0 = compute_psi(y0)
    
    #Take one timestep and recalculate psi
    y = RK5step(y0,psi0,t,mu)
    psi = compute_psi(y)
    
    #Initialize counter
    cnt = 1

    #Iterate until psi and psi0 are within tolerance
    while np.abs(psi-psi0) > tol:
       
        #Update counter
        cnt += 1
        
        #State before timestep
        y0 = y
        psi0 = compute_psi(y0)
        
        #State after timestep
        y = RK5step(y0,psi0,t,mu)
        psi = compute_psi(y)
        
        #Break from loop if max number of iterations is reached
        if cnt> max_it:
            print('Did not converge after '+str(max_it)+' iterations')
            break
        

    return y, psi 


def find_psi(t,mu):
    '''
    Find the value of the superfluid order parameter using imaginary
    time propagation.
    
    Args:
        t: Hopping amplitude
        mu: Chemical potential
        
    Return:
        psi: Superfluid order parameter
    '''
    
    state, psi = find_gnd(t,mu)
    
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

class TestImagtime(unittest.TestCase):
    '''
    Unit testing class for functions in the imag_time.py module
    '''
    
    def test_insulator(self):
        '''
        Test that the order parameter is zero for a known insulating ground
        state in the paramater space (t=0.05,mu=0.5).
        '''
        
        #Set system parameters for a known insulator
        t, mu = 0.05, 0.5
        
        #Set tolerance
        tol = 1e-4
        
        #Compute order parameter
        psi = find_psi(t,mu)
        
        self.assertTrue(np.abs(psi) < tol) 
    

#Run tests if in main namespace
if __name__ == '__main__':
    unittest.main(argv=[''],verbosity=2,exit=False)
