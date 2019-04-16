# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 11:36:39 2019

@author: Alex Hickey

Boundary search algorithm
"""



def bd(tlist,mu,V,Nmax, minsteps = 12, tol = 1e-9):
    '''
    Calculate the value of t required to transition out of an insulator state
    by recursively halving a provided list.
    '''
    
    #Return value once list is irreducible
    if len(tlist) <= 2:
        
        return tlist[0]
    
    else:
        
        indx = len(tlist) // 2
        t = tlist[indx]
        thA, thB = theta_tight(mu,V)
        mfparams = np.array([thA*1.0,thB*1.0,tol,2*tol])
        
        #Step forward in minimization routine
        for count in range(minsteps):
         
            mfparams = minimize_routine(mfparams,t,mu,V,Nmax)
            
        #Chosen t corresponds to insulator
        if np.max(mfparams[2:]) < 2*tol:
            
            return insulator_bd(tlist[indx:],mu,V,Nmax)
        
        #Chosen t corresponds to superfluid
        else:
            
            return insulator_bd(tlist[:indx],mu,V,Nmax)