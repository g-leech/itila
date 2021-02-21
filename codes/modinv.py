import numpy as np
from math import gcd 

# If det A is coprime to m, then you can be sure that A is invertible modm.

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


def inv(A) :
	return A

def inverse_mod(A, m) :
	d = det(A)
	print(d)
	assert( coprime(d, m) )

	gcd, dinv, _ = egcd(d, m)
	if gcd == -1 :
		dinv *= -1
	print(dinv)

	Ainv = inv(A)
	Ainv = dinv * Ainv

	return Ainv % m

A = np.matrix([[1, 5], 
			  [3, 4]])
m = 26

Amodinv = inverse_mod_2x2(A, m)
check = Amodinv * A % m
I = np.identity(2)
assert(np.all(check == I))


A = np.matrix( [[17, 17, 5], \
				[21, 18, 21], \
				[2, 2, 19]] )
m = 26

print(inverse_mod(A, m))

solution = np.matrix( [[4, 9, 15], \
						[15, 17, 6], \
						[24, 0, 17]] )


print(egcd(a, b))
