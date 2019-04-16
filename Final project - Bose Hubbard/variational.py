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

def groundstate(H):
    '''
    Calculate the minimum eigenvalue and corresponding eigenvector of a 
    Hermitian matrix
    '''
    
    eigvals, eigvecs = np.linalg.eigh(H)
    
    return eigvals[0], eigvecs[:,0]



def ground_energy(psi,t,mu,N,groundstate = False):
    '''
    Calculate the ground state energy for given parameters.
    Return ground state if True.
    '''
    
    H = construct_hamiltonian(psi,t,mu,N)
    
    if groundstate:
        
        return groundstate(H)
        
    else:
        
        return np.linalg.eigvalsh(H)[0]
    

    
def find_psi(t,mu,N,groundE = False):
    '''
    Calculate order parameter which minimizes the free energy.
    Return ground state energy if groundE = True.
    '''
    
    psi = scipy.optimize.minimize(ground_energy,0.1,args = (t,mu,N),
                                  method='Nelder-Mead', tol=1e-13)
    
    if groundE:
        return psi['x'][0], psi['fun']
    
    else:
        return psi['x'][0]
    

print(find_psi(0.3,0.5,5))



