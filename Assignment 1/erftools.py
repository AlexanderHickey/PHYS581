"""
Author: Alexander Hickey

This python library contains functions used to compute the complex
error function. A testing framework is built in, and can be run 
by loading this file into the __main__ namespace.
"""

import numpy as np
import scipy.special as special

def erf_taylor(z, nterms=19):
    '''
    Compute the standard error function using a Laurent series about z=0.
    
    Args:
        z: Array-like, collection of complex numbers
        nterms: Number of terms in the Taylor series to use
        
    Return:
        erf_z: Error function evaluated at each number
    '''
    
    #Cast to numpy array
    z = np.array(z)
    
    #Array to keep track of terms in series
    terms = np.zeros((nterms,)+z.shape, dtype=np.complex128)
    
    #Generate terms in series
    terms[0] = z
    z2 = -z*z
    for n in range(1,nterms):
        terms[n] = terms[n-1] * z2 / n * (2*n-1)/(2*n+1)
    
    #Sum over array of terms
    return np.sum(terms, axis=0) * 2.0 / np.sqrt(np.pi)


def estimate_nterms(z, sig_digs = 10):
    '''
    Compute the number of terms needed in the Laurent series expansion of the
    standard error function to obtain a desired relative precision.
    
    Args:
        z: Array-like, collection of complex numbers
        sig_digs: Integer, specify the desired number of significant digits
        
    Return:
        erf_z: Array consisting of the number of terms needed to obtain a
        desired number of significant digits.
    '''
    
    #Initialize counter
    n, term = 1, z
    
    while np.abs(term) > 10**(-sig_digs):
        
        n += 1
        term = (-1)**n * z**(2*n+1)/(special.factorial(n)*(2*n+1))
    
    return n



    












def w(z):
    #Works in first quadrant only
    x, y = np.real(z), np.imag(z)
    
    if y<4.29 and x<5.33:
        s=(1-y/4.29)*np.sqrt(1-x*x/28.41)
        h=1.6*s
        h2 = 2*h
        capn = int(6+23*s)
        nu = int(9+21*s)
        
    else:
        h, capn, nu = 0,0,8
        
    if h>0:
        lamb = h2**capn
    
    b = h==0 or lamb==0
    r1, r2, s1, s2 = 0,0,0,0
    for n in range(nu,-1,-1):
        np1 = n+1
        t1 = y+h+np1*r1
        t2 = x-np1*r2
        c= .5/(t1*t1+t2*t2)
        r1 = c*t1
        r2 = c*t2
        
        if h>0 and n<=capn:
            t1 = lamb + s1
            s1 = r1*t1-r2*s2
            s2 = r2*t1+r1*s2
            lamb = lamb/h2
    
    if y==0:
        re = np.exp(-x*x)
    else:
        re = 1.12837916709551*(r1*b+s1*(not b))
    
    im = 1.12837916709551*(r2*b+s2*(not b))
    
    return re+im*1.0j
    
    


def w_vec(z):
    
    #Map to numpy array
    z = np.array(z,dtype = np.complex128)
    
    #Works in first quadrant only
    x, y = np.real(z), np.imag(z)
    
    inner = np.logical_and(y<4.29,x<5.33)*1
    outer = np.logical_not(inner)*1
    
    s= (1-y/4.29)*np.sqrt(1-x*x/28.41)*inner+0*outer
    h= (1.6*s)*inner + 0*outer
    h2 = 2*h
    capn = ((6+23*s)*inner+0*outer).astype(int)
    nu = ((9+21*s)*inner +8*outer).astype(int)
    
    hpos = (h>0)*1
    hneg = np.logical_not(hpos)
    
    lamb = (h2**capn)*(hpos)
    
    b = np.logical_or(h==0,lamb==0)
    
    r1 = np.zeros(z.shape)
    r2, s1, s2 = r1.copy(), r1.copy(), r1.copy()
    
    nustart = np.max(nu)
    
    for n in range(nustart,-1,-1):
        
        #Loop updates t1,t2,c,r1,r2
        mask_act = (nu>0)*1 #Only act on elements with positive counters
        mask_ignore = np.logical_not(mask_act)*1
        
        np1 = n+1
        
        #Branch needed to avoid using variable without assignment
        if n != nustart:
            t1 = (y+h+np1*r1)*mask_act + t1*mask_ignore
            t2 = (x-np1*r2)*mask_act + t2*mask_ignore
            c= .5/(t1*t1+t2*t2)*mask_act + c*mask_ignore
        
        else:
            t1 = (y+h+np1*r1)*mask_act 
            t2 = (x-np1*r2)*mask_act 
            c= .5/(t1*t1+t2*t2)*mask_act
            
            
        r1 = (c*t1)*mask_act + r1*mask_ignore
        r2 = (c*t2)*mask_act+ r2*mask_ignore
        
        mask2 = np.logical_and(n<=capn,h>0)*1
        mask2not = np.logical_not(mask2)*1
            
        t1 = (lamb + s1)*mask2 + t1*mask2not
        s1 = (r1*t1-r2*s2)*mask2+ s1*mask2not
        s2 = (r2*t1+r1*s2)*mask2+ s1*mask2not
        lamb = (lamb/h2)*mask2+ lamb*mask2not
    
    re = np.exp(-x*x)*(y==0)+1.12837916709551*(r1*b+s1*np.logical_not(b))*(y!=0)
    im = 1.12837916709551*(r2*b+s2*np.logical_not(b))
    
    return re+im*1.0j
    
    
