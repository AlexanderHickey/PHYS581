# -*- coding: utf-8 -*-
"""
bdsearch.py
@author: Alex Hickey

This module aims to search through the the parameter space and find the value 
of t that lies on the insulator-superfluid phase boundary for a given mu.
"""

#Import modules
import numpy as np


def isSF(psi, tol = 1e-3):
    '''
    Check if computed order parameter corresponds to a superfluid phase.
    
    Args:
        psi: Computed order parameter
        tol: Tolerance, below tol the order parameter is assumed to be zero.
        
    Return:
        isSF: Boolean, True if in superfluid phase 
    '''
    
    return np.abs(psi) > tol 


def bd(mu,tlist,find_psi):
    '''
    Calculate the value of t required to transition out of an insulator state
    by recursively halving a provided list.
    
    Args:
        tlist: List of values of t to iterate through reursively
        mu: Value of mu
        find_psi: Function used to compute the order parameter
        
    Return:
        t: Value of t on the phase boundary
    '''
    
    #Return value once list is irreducible
    if len(tlist) <= 2:
        
        return tlist[0]
    
    #Otherwise divide list in half
    else:
        
        indx = len(tlist) // 2
        t = tlist[indx]
        
        #Compute psi with given function
        psi = find_psi(t,mu)
        
        #Chosen t corresponds to superfluid
        if isSF(psi):
            
            return bd(mu,tlist[:indx],find_psi)
        
        #Chosen t corresponds to insulator
        else:
            
            return bd(mu,tlist[indx:],find_psi)
    
