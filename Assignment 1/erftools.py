"""
Author: Alexander Hickey

This python library contains functions used to compute the complex
error function. A testing framework is built in, and can be run 
by loading this file into the __main__ namespace.
"""

import numpy as np

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
    
    terms = np.zeros((nterms,)+z.shape, dtype=np.complex128)
    terms[0] = z
    z2 = -z*z  # move math outside loop
    for n in range(1,nterms):
        terms[n] = terms[n-1] * z2 / n * (2*n-1)/(2*n+1)
    
    return np.sum(terms, axis=0) * 2.0 / np.sqrt(np.pi)