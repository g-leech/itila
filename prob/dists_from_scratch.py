import numpy as np


class DiscreteProbDist() :

	def __init__(self, alphabet, marginals):
		assert( len(marginals) == len(alphabet) )
		assert( sum(marginals) == 1 )

		self.a = np.array(alphabet)
		self.ps = np.array(marginals)
		self.dist = {k: v for k,v in zip(self.a, self.ps)}

	def __str__(self) :
		return self.dist 


# Could do as a dataframe...
class BivariateDist() :
	def __init__(self, x, y, x_given_y):
		assert( sum(x.ps) == 1)	
		assert( sum(y.ps) == 1)	

		self.x = x
		self.y = y
		self.condXY = x_given_y

	def joint(self) :
		nx, ny = len(self.x.ps), len(self.y.ps)
		xy = np.ones((nx, ny))
		return xy * self.y.ps * self.condXY.ps


	def marginal(self, outcome) :
		matches = [p for a, p in self.joint \
					if a == outcome]
		return sum( matches )


englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, \
					'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, \
					'Q': 0.10, 'Z': 0.07}



if __name__ == '__main__':
	englishP = {k:v/100 for k,v in englishLetterFreq.items() }

	k = 5
	margs = [1/k]*k
	X = DiscreteProbDist(range(1,k+1), margs)
	print(X.dist)


	Y = X
	# independent
	cond = X
	xy = BivariateDist(X, Y, cond)
	print(xy.joint())
