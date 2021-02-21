import numpy as np
from math import gcd 

# If detA is coprime to m, then you can be sure that A is invertible modm.

m = 26

def det(A) :
	d = np.linalg.det(A)
	return round(d) 

def coprime(a, b):
    return gcd(a, b) == 1

def egcd(a, b):
	if a == 0:
		return (b, 0, 1)
	else:
		gcd, x, y = egcd(b % a, a)
		return (gcd, y - (b//a) * x, x)



A = np.matrix([[1, 5], 
			  [3, 4]])


def basic_2x2_inv(A) :
	Ainv = np.ones(A.shape)
	Ainv[0,0] = A[1,1]
	Ainv[1,1] = A[0,0]
	Ainv[1,0] = -A[1,0]
	Ainv[0,1] = -A[0,1]

	return Ainv

def inverse_mod_2x2(A, m) :
	d = det(A)
	assert( coprime(d, m) )

	gcd, dinv, _ = egcd(d, m)
	if gcd == -1 :
		dinv *= -1

	Ainv = basic_2x2_inv(A)
	inv = dinv * Ainv
	return inv % m



print(inverse_mod_2x2(A, m))

