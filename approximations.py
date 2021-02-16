import numpy as np
from numpy import log, log2, sqrt, e, pi
import scipy
from scipy.special import binom

ln = np.log

def approx_fac(x) :
    second_correction = sqrt(2 * pi * x)
    return x**x * e**(-x) * second_correction


def close_enough(approx, exact, tol=0.01) :
    r = approx / exact
    assert(abs(1 - r) < tol)




# TODO: need to take logs to prevent zero division
def binary_entropy(x) :
    assert((x >= 0) & (x <= 1))
    if x == 0 or x == 1 :
        return 0

    compl = 1 - x
    return x * log2(1/x) + compl * log2( 1 / compl )


def approx_combin(r, N) :
    assert(r < N)

    xs = (N - r)
    logged = ln(N / xs) + r * ln(N/r)
    
    return e**(logged)



def approx_combin_entropy(r, N) :
    assert(r < N)
    
    h2 = binary_entropy(r/N)
    correction = 2 * np.pi * N * ((N - r)/N) * (r/N)
    logged = h2 * N - 0.5 * np.log2(correction)

    return 2**(logged)





if __name__ == '__main__':
    approx = approx_fac(100)
    exact = np.math.factorial(100) 
    close_enough(approx, exact) 

    approx = approx_combin(19, 40)
    exact = binom(40, 19)
    # Not that close....
    #assert( np.isclose(exact, approx) )
    print("approx binom:", '%.2E' % approx)
    print("exact binom:", '%.2E' % exact)