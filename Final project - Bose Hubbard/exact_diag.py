"""
Created on Sun Apr 14 11:37:10 2019

@author: Alex Hickey
"""

import numpy as np



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


def compute_psi(state):
    '''
    Compute the superfluid order parameter
    '''
    N = len(state)
    
    return np.sum([state[j]*state[j+1]*np.sqrt(j+1) for j in range(N-1)])
    


def find_psi(t,mu,N,tol = 1e-13):
    '''
    Find the value of the superfluid order parameter through by
    exact-diaganilization iteration.
    
    
    '''
    
    #Initial guess for psi
    psi0 = 1e-3
    
    E, state = groundstate(construct_hamiltonian(psi0,t,mu,N))
    psi = compute_psi(state)
    
    while np.abs(psi - psi0) > tol:
        print(psi)
        psi0 = psi
        E, state = groundstate(construct_hamiltonian(psi0,t,mu,N))
        psi = compute_psi(state)
        
    return psi
        

    
#find_psi(0.1,0.5,10)




