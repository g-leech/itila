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
		plt.plot(x, posterior(x))
		plt.title(f"nH={n}, N={N}")
		plt.show()
		
		print(f"nH={n}, N={N}:", p_next_heads(n, N))


	# Ex 2.10
	A = ["B", "W", "W"]
	B = ["B", "B", "W"]
	p = 1/2
