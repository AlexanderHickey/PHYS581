# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 11:37:13 2019

@author: Alex Hickey
"""


import numpy as np
import scipy.optimize



def construct_hamiltonian(psi,t,mu,N):
    '''
    Construct MF Hamiltonian in the occupation number basis.
    '''
    
    H = np.zeros((N+1, N+1))

    for i in range(0, N+1):
        
        #Diagonal components
        H[i, i] = (i*(i-1)/2-mu*i+t*psi*psi)/2.0
        
        #Upper-diagonal components
        if i != N:
            
            H[i,i+1] = -t*psi*np.sqrt(i+1)
        
    return H+H.T

def spectrum(H):
    '''
    Calculate spectrum and eigenvectors of a Hermitian matrix.
    '''
    
    spec = np.linalg.eigh(H)
    
    return spec[0], spec[1]
    

def ground_energy(psi,t,mu,N,groundstate = False):
    '''
    Calculate the ground state energy for given parameters.
    Return ground state if True.
    '''
    
    H = construct_hamiltonian(psi,t,mu,N)
    
    if groundstate:
        
        eigvals, eigvecs = spectrum(H)
        
        return eigvals[0], eigvecs[:,0]
        
    else:
        
        return np.linalg.eigvalsh(H)[0]
    

    
def find_psi(t,mu,N,groundE = False):
    '''
    Calculate order parameter which minimizes the free energy.
    Return ground state energy if groundE = True.
    '''
    
    psi = scipy.optimize.minimize(ground_energy,0.1,args = (t,mu,N),method='Nelder-Mead',tol=1e-14)
    
    if groundE:
        return psi['x'][0], psi['fun']
    
    else:
        return psi['x'][0]

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