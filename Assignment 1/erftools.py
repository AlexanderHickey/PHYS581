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
    
    #Array to keep track of terms in series
    terms = np.zeros((nterms,)+z.shape, dtype=np.complex128)
    
    #Generate terms in series
    terms[0] = z
    z2 = -z*z
    for n in range(1,nterms):
        terms[n] = terms[n-1] * z2 / n * (2*n-1)/(2*n+1)
    
    #Sum over array of terms
    return np.sum(terms, axis=0) * 2.0 / np.sqrt(np.pi)



def wQ1(z):
    '''
    Compute the Faddeeva function in the first quadrant of the complex plane.
    Algorithm is garunteed an accuracy of at least 10 significant figures,
    see: https://dl.acm.org/citation.cfm?id=363618
    
    Args:
        z: Single complex number in the first quadrant (Re >= 0 and Im >=0)
        
    Return:
        w(z): Faddeeva function at z
    '''
    
    #Separate real and imaginary parts
    x, y = np.real(z), np.imag(z)
    
    #The remainder of the algorithm is described in:
    # https://dl.acm.org/citation.cfm?id=363618
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
    
    


def wQ1_vec(z):
    '''
    Compute the Faddeeva function in the first quadrant of the complex plane.
    Algorithm is garunteed an accuracy of at least 10 significant figures,
    see: https://dl.acm.org/citation.cfm?id=363618. Modified to handle vector
    input.
    
    Args:
        z: Array of complex numbers in the first quadrant (Re >= 0 and Im >=0)
        
    Return:
        w(z): Faddeeva function at z
    '''
    
    #Separate real and imaginary parts
    x, y = np.real(z), np.imag(z)
    
    #The remainder of the algorithm is based on the algorithm:
    #https://dl.acm.org/citation.cfm?id=363618
    #Several modifications are made to use numpy array algebra
    
    #Mask inner and outer regions of algorithm
    inner = np.logical_and(y<4.29,x<5.33)*1.
    outer = np.logical_not(inner)*1.
    
    s= (1-y/4.29)*np.abs(np.sqrt(1-x*x/28.41+0.0j))*inner
    h= (1.6*s)*inner
    h2 = 2*h
    capn = ((6+23*s)*inner+0*outer).astype(int)
    nu = ((9+21*s)*inner +8*outer).astype(int)
    
    lamb = (h2**capn)*((h>0)*1)
    
    b = np.logical_or(h==0,lamb==0)
    
    r1 = np.zeros(z.shape)
    r2, s1, s2 = r1.copy(), r1.copy(), r1.copy()
    t1, t2, c = r1.copy(), r1.copy(), r1.copy()
    
    nustart = np.max(nu)
    
    for n in range(nustart,-1,-1):
        
        #Update counter
        np1 = n+1
        
        #Only act on elements with positive counters
        mask_act = (nu>0)*1
        
        #Negate mask
        mask_ignore = np.logical_not(mask_act)*1
        
        #Branch needed to avoid using variable without assignment
        t1 = (y+h+np1*r1)*mask_act + t1*mask_ignore
        t2 = (x-np1*r2)*mask_act + t2*mask_ignore
        c= .5/(t1*t1+t2*t2)*mask_act + c*mask_ignore
        
        r1 = (c*t1)*mask_act + r1*mask_ignore
        r2 = (c*t2)*mask_act+ r2*mask_ignore
        
        mask2 = np.logical_and(n<=capn,h>0)*1
        mask2not = np.logical_not(mask2)*1
            
        t1 = (lamb + s1)*mask2 + t1*mask2not
        s1 = (r1*t1-r2*s2)*mask2+ s1*mask2not
        s2 = (r2*t1+r1*s2)*mask2+ s1*mask2not
        lamb = (lamb/(h2+mask2not))*mask2+ lamb*mask2not
    
    re =np.exp(-x*x)*(y==0)+1.12837916709551*(r1*b+s1*np.logical_not(b))*(y!=0)
    im = 1.12837916709551*(r2*b+s2*np.logical_not(b))
    
    return re+im*1.0j
    


def w(z):
    '''
    Compute the Faddeeva function in any quadrant of the complex plane, by
    mapping it to the first quadrant with symmetry properties.
    
    Args:
        z: Single complex number
        
    Return:
        w(z): Faddeeva function at z
    '''
    
    #Real and imaginary parts
    re, im = np.real(z), np.imag(z)
    
    #z in first quadrant
    if re >= 0 and im >= 0:
        
        return wQ1(z)
    
    #z in second quadrant
    elif re < 0 and im > 0:
        
        return np.conj(wQ1(-np.conj(z)))
    
    #z in third quadrant
    elif re <=0 and im <= 0:
        
        return 2*np.exp(-z*z)-wQ1(-z)
    
    #z in fourth quadrant
    else:
        
        return 2*np.exp(-z*z)-np.conj(wQ1(np.conj(z)))
    
    
    
    
def w_vec(z):
    '''
    Compute the Faddeeva function in any quadrant of the complex plane, by
    mapping it to the first quadrant with symmetry properties. 
    Modified to handle vector input.
    
    Args:
        z: Array of complex numbers
        
    Return:
        w(z): Faddeeva function at z
    '''
    
    #Real and imaginary parts
    re, im = np.real(z), np.imag(z)
    
    #Masks corresponding to each quadrant
    m1 = np.logical_and(re > 0,im >= 0)
    m2 = np.logical_and(re <= 0,im > 0)
    m3 = np.logical_and(re < 0,im <= 0)
    m4 = np.logical_and(re >= 0,im < 0)
    m0 = np.logical_and(re == 0,im == 0) #Don't forget origin!
    
    #Compute the result for each quadrant using symmetry properties
    resQ1 = wQ1_vec(z)
    resQ2 = np.conj(wQ1_vec(-np.conj(z)))
    resQ3 = 2*np.exp(-z*z)-wQ1_vec(-z)
    resQ4 = 2*np.exp(-z*z)-np.conj(wQ1_vec(np.conj(z)))
    
    return resQ1*m1+resQ2*m2+resQ3*m3+resQ4*m4+1.0*m0


def erf(z):
    '''
    Compute the error function in the complex plane.
    Algorithm is garunteed an accuracy of at least 10 significant figures,
    see: https://dl.acm.org/citation.cfm?id=363618
    
    Args:
        z: Single complex number
        
    Return:
        erf(z): Error function at z
    '''
    
    return 1-np.exp(-z*z)*w(1.0j*z)


def erf_vec(z):
    '''
    Compute the error function in complex plane.
    Algorithm is garunteed an accuracy of at least 10 significant figures,
    see: https://dl.acm.org/citation.cfm?id=363618. Modified to handle vector
    input.
    
    Args:
        z: Array of complex numbers
        
    Return:
        erf(z): Error function at z
    '''

    return 1.0-np.exp(-z*z)*w_vec(1.0j*z)




########################################################
#Testing framework
    
import unittest
import scipy.special as special

class TestErf(unittest.TestCase):
    '''
    Unit testing class for functions in the erftools.py library
    '''
    
    def test_ErfTaylor(self):
        '''
        Test that the Maclaurin series converges to the error function
        within the unit disk. Tolerance is set to 1e-10 for n=19 terms.
        '''
        #Generate random array of 19 numbers in the unit disk.
        xr, yr = np.random.random(19), np.random.random(19) 
        zr = xr + 1.0j*yr 
        
        #Compare to special.erf
        diff = np.abs(erf_taylor(zr)-special.erf(zr))
        
        self.assertTrue( np.any(diff<1e-10) )
    
    def test_ErfZeroes(self):
        '''
        Test that the first 19 zeroes of the erf function correspond
        with the zeroes generated by the scipy.special.erf_zeros
        function.
        '''
        #Compute first 19 zeroes
        z0 = special.erf_zeros(19)
        erf0 = np.abs([erf(z0[j]) for j in range(len(z0))])
        
        #Assert that |erf(z0)-0| < 1e-10 for all z0
        #This is the tolerance garunteed by the
        #Gautschi algorithm.
        self.assertTrue( np.any(erf0<1e-10) )

    def test_ErfVecZeroes(self):
        '''
        Test that the first 19 zeroes of the erf_vec function correspond
        with the zeroes generated by the scipy.special.erf_zeros
        function.
        '''
        #Compute first 19 zeroes
        z0 = special.erf_zeros(19)
        erf0 = np.abs(erf_vec(z0))
        
        #Assert that |erf(z0)-0| < 1e-10 for all z0
        #This is the tolerance garunteed by the
        #Gautschi algorithm.
        self.assertTrue( np.any(erf0<1e-10) )


#Run tests if in main namespace
if __name__ == '__main__':
    unittest.main(argv=[''],verbosity=2,exit=False)

    
    
    
    
    
    
    
    
    
    
    
    
    
