import random

def byte2str(b) :
	return chr(int(b, 2))

def str2byte(x) :
	return format(ord(x), 'b')

def encode(s) :
	return ''.join(str2byte(x) for x in s.replace(" ", ""))

def decode(b, n=7) :
	r = range(0, len(b), n)
	bytes_ = [ b[i : i+n] for i in r ]
	
	return ''.join( byte2str(b) for b in bytes_ )

def flip(bit) :
	return bit.replace('1', '2') \
				.replace('0', '1') \
				.replace('2', '0')



class BinarySymmetric() :

	def __init__(self, p) :
		assert((p >= 0) & (p<=1))
		if p > 0.5 :
			print("WARNING: channel is unusable")
		self.noise = p

	def trans_bit(self, bit) :
		return flip(bit) if random.random() <= self.noise \
				else bit

	def transmit(self, b) :
		return ''.join([self.trans_bit(bit) for bit in b])


def rep_encode(s, r=3) :
	# Want tie-breaking so odd
	assert(r % 2 != 0)

	b = encode(s)
	return ''.join(bit * r for bit in b)


def majority(t) :
	return max(set(t), key=t.count)


def get_repeats(b, r) :
	domain = range(0, len(b), r)
	return [ b[i : i+r] for i in domain ]

def rep_decode(b, r=3) :
	votes = ''.join(majority(t) for t in get_repeats(b, r))
	
	return decode(votes)


if __name__ == '__main__':
	noise = 0.1
	print("with noise level", noise)

	channel = BinarySymmetric(p=noise)

	s = "would be a shame if anything got flipped"

	b = encode(s)
	print("Original: ", decode(b))
	print("Raw: ", decode(channel.transmit(b)))

	r3 = rep_encode(s)	
	received = channel.transmit(r3)
	print("R3: ", rep_decode(received))

	r9 = rep_encode(s, r=9)	
	received = channel.transmit(r9)
	print("R9: ", rep_decode(received, r=9))
	