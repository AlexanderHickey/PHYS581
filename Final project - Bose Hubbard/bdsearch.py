# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 11:36:39 2019

@author: Alex Hickey

Boundary search algorithm
"""



def phase_boundary(mu_max,num_mu,dt):
    '''
    Calculate the phase-boundary in t-mu space
    '''
    
    #Dimension of truncated Fock space
    N = np.int(mu_max)+3
    
    mulist = np.linspace(0,mu_max,num_mu)
    tlist = np.zeros((num_mu))
    
    for j in range(num_mu):
        
        #Initialize
        t = E0 = E1 = 0.0
        
        #Break from loop when psi != 0
        while E0 <= E1: 
             
            t += dt
            E0 = ground_energy(0.0,t,mulist[j],N)
            E1 = ground_energy(0.01,t,mulist[j],N)
            
        tlist[j] = t
    
    return mulist, tlist