# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 11:37:12 2019

@author: Alex Hickey
"""

import numpy as np

#Fix maximum number of bosons per site
N = 10

#Define arrays to call in functions
n_arr = np.arange(N+1)
sqr_arr = np.sqrt(n_arr)


def a(state):
    '''
    Act with the annihilation operator in the occupation number basis
    '''
    
    return np.roll(state*sqr_arr,-1)


def a_dag(state):
    '''
    Act with the creation operator in the occupation number basis
    '''
    
    return  sqr_arr*np.roll(state,1)


def compute_psi(state):
    '''
    Compute the superfluid order parameter <a>
    '''
    
    return np.sum(state*a(state))


def H(state,psi,t,mu):
    '''
    Takes a state in the occupation number basis of the form
    [c0,c1,...,cN] and acts with the Hamiltonian operator.
    '''
    
    newstate = -t*psi*(a(state)+a_dag(state))
    newstate += (0.5*n_arr*(n_arr-1.0)-mu*n_arr+t*psi*psi)*state
    
    return newstate



def RK45step(y,psi,t,mu,h=.08):
      
        
    #RK5 coefficients        
    k1 = -h*H(y,psi,t,mu)
    k2 = -h*H(y+k1/4.0,psi,t,mu)
    k3 = -h*H(y+(3/32)*k1+(9/32)*k2,psi,t,mu)
    k4 = -h*H(y+(1932/2197)*k1-(7200/2197)*k2+(7296/2197)*k3,psi,t,mu)
    k5 = -h*H(y+(439/216)*k1-8*k2+(3680/513)*k3-(845/4104)*k4,psi,t,mu)
    k6 = -h*H(y-(8/27)*k1+2*k2-(3544/2565)*k3+(1859/4104)*k4-(11/40)*k5,psi,t,mu)
    
    #Take timestep
    y5 = y+(16/135)*k1+(6656/12825)*k3+(28561/56430)*k4-(9/50)*k5+(2/55)*k6
    
    return y5/np.linalg.norm(y5)



def find_gnd(t,mu,tol = 1e-11,max_it=100000):
    

    #Initial guess is a uniform superposition
    y0 = np.ones(N+1)/np.sqrt(N+1)
    psi0 = compute_psi(y0)

    y = RK45step(y0,psi0,t,mu)
    psi = compute_psi(y)
    
    cnt = 1

    #Iterate until psi and psi0 are within tolerance
    while np.abs(psi-psi0) > tol:
       
        #Update counter
        cnt += 1
        
        #State before timestep
        y0 = y
        psi0 = compute_psi(y0)
        
        #State after timestep
        y = RK45step(y0,psi0,t,mu)
        psi = compute_psi(y)
        
        
        print(psi)
        
        if cnt> max_it:
            print('Did not converge after '+str(max_it)+' iterations')
            break
    
    
    return y, psi 


def find_psi(t,mu):
    
    
    state, psi = find_gnd(t,mu)
    
    return psi



