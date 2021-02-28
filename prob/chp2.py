import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt
import numpy
from math import factorial as fac


# For binary vars
# a = Jo's health
# b = test result
def BT(d) :
	d["P(¬A)"] = 1 - d["P(A)"]
	d["P(B|¬A)"] = 1 - d["P(B|A)"]
	d["P(¬B|A)"] = 1 - d["P(¬B|¬A)"]
	d["P(B)"] = d["P(B|A)"] * d["P(A)"] + d["P(B|¬A)"] * d["P(¬A)"]

	d["P(A|B)"] = d["P(B|A)"] * d["P(A)"] / d["P(B)"]
	return d["P(A|B)"]


# surprisal; shannons
# Strictly speaking, outcomes have information, not probs 
def info(p):
	return - np.log2(p) 


# uncertainty; average surprisal per draw
def entropy(ps):
	return sum( p * info(p) \
				if p != 0 else 0 \
				 for p in ps )

# A = alphabet of outcomes
def maxent(A) :
	return np.log2(A)


def joint_entropy(joint) :
	return sum(
			joint(x,y) * info(joint(x,y))
			if p != 0 else 0 \
			for x,y in joint 	
		)

# for disjoint events. 
# Split the ensemble into two subensembles a and b
# Take H(\sumA, \sumB)
# + normalised H(a) + normalised H(b) 
def recursive_entropy(ps, m) :
	ps = np.array(ps)
	pa = sum(ps[:m])
	pb = sum(ps[m:])

	return entropy([pa,pb]) \
			+ pa * entropy(ps[:m] / pa) \
			+ pb * entropy(ps[m:] / pb) 




k = 6
A = range(k)
uniform = [1/len(A) for a in A]
assert(entropy(uniform) == maxent(k))


if __name__ == '__main__':
	# Ex 2.3
	d = {"P(A)": 0.01, 
		"P(B|A)": 0.95,
		"P(¬B|¬A)": 0.95
		}
	print("2.3.  P of disease given test", BT(d))

	# Ex 2.5. P(z < 1)
	N = 5
	p = 0.2
	z = lambda n : (n - N*p)**2 / (N*p*(1-p))
	#for i in range(6) :
	#	print( z(i), binom.pmf(k=i, p=p, n=N) )
	print("2.5: ", z(1), binom.pmf(k=1, p=p, n=N) )

	# Ex 2.6. P(u | nB)
	U = 11
	N = 10
	nB = 3
	p_u = 1/U # prior
	likelihood = lambda u : binom.pmf(n=N, k=nB, p=u/N) # p_b_given_a
	evidence = sum(p_u * likelihood(u) for u in range(U)) # p_not_b_given_not_a

	margs = []
	for u in range(U) :
		posterior = (p_u * likelihood(u)) / evidence # B's T
		margs += [posterior]
	assert(round(sum(margs)) == 1)
	#print(margs)

	# P(B | 3, 10) = sum
	marg = sum([margs[u] * u/N for u in range(U) ])
	print("2.6: ", round(marg, 3) )
	print("Silly frequentist answer:", round(max(margs), 3) )

	# Ex 2.7
	def p_next_heads(n, N) :
		return (n+1) / (N+2)
	
	prior = 1 # uniform???
	likelihood = lambda p, n, N : p**n * (1 -p)**(N-n)
	evidence = lambda n, N : (fac(n) * fac(N-n)) / fac(N+1)

	settings = [{"n": 0, "N": 3},
				{"n": 2, "N": 3},
				{"n": 3, "N": 10},
				{"n": 29, "N": 300}]
	for d in settings:
		n = d["n"]
		N = d["N"]
		p = prior
		posterior = lambda p : likelihood(p, n, N) / evidence(n, N)
		x = np.linspace(0, 1, 200)
		#plt.plot(x, posterior(x))
		#plt.title(f"nH={n}, N={N}")
		
		print(f"nH={n}, N={N}:", p_next_heads(n, N))

	plt.show()

	# Ex 2.10
	p = 1/2
	p1 = 1/3 # P(B|U1)
	p2 = 2/3 # P(B|U2)

	# P(U = A | X = B) 
	d = {
		"P(U1)" : p,
		"P(¬U1)" : 1 - p,
		"P(B|U1)" : p1,
		"P(B|¬U1)" : p2
	}
	# P(B)
	evidence = lambda d : d["P(B|U1)"] * d["P(U1)"] + d["P(B|¬U1)"] * d["P(¬U1)"]
	# P(U1|B)
	posterior = lambda d : (d["P(B|U1)"] * d["P(U1)"]) / evidence(d)
	print("Ex2.10:  ", posterior(d))

	# Ex 2.11
	p = 1/2
	p1 = 1/5 # P(B|U1)
	p2 = 2/5 # P(B|U2)
	# P(U = A | X = B) 
	d = {
		"P(U1)" : p,
		"P(¬U1)" : 1 - p,
		"P(B|U1)" : p1,
		"P(B|¬U1)" : p2
	}
	evidence = lambda d : d["P(B|U1)"] * d["P(U1)"] + d["P(B|¬U1)"] * d["P(¬U1)"]
	posterior = lambda d : (d["P(B|U1)"] * d["P(U1)"]) / evidence(d)
	print("Ex2.11:  ", posterior(d))

	#x = np.linspace(0, 1, 1000)
	#plt.plot(x, info(x))
	#plt.show()
	
	
	A = list(filter(str.isalnum,map(chr,range(97))))
	pIsNum = 1/3
	pIsConsonant = 1/3
	pIsVowel = 1/3
	pNum = 1/10
	H = np.log2(3) + pIsNum * np.log2(10) \
					+ pIsConsonant * np.log2(26) \
					 + pIsVowel * np.log2(5)
	print("Ex2.13:  ", H)

	print(entropy([0.5, 0.25, 0.25]))
	print(recursive_entropy([0.5, 0.25, 0.25], 1))