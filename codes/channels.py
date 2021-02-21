import random
import numpy as np


# Uses strings for channel

def byte2str(b) :
    return chr(int(b, 2))

def str2byte(x) :
    return format(ord(x), 'b')

def bit_encode(s) :
    return ''.join(str2byte(x) for x in s.replace(" ", ""))

def bit_decode(b, n=7) :
    domain = range(0, len(b), n)
    bytes_ = [ b[i : i+n] for i in domain ]
    
    return ''.join( byte2str(b) for b in bytes_ )

def flip(bit) :
    return bit.replace('1', '2') \
                .replace('0', '1') \
                .replace('2', '0')

def arr2str(arr) :
    st = [str(block) for block in arr] 
    st = [s.replace("]", "") \
      .replace("[", "") \
      .replace(" ", "") for s in st]
    return ''.join(st)


class BinarySymmetricChannel() :
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


class RepCode() :
    def __init__(self, r=3) :
        # Want tie-breaking so odd
        assert(r % 2 != 0)
        self.r = r


    def encode(self, s) :
        b = bit_encode(s)
        return ''.join(bit * self.r for bit in b)


    def majority(self, t) :
        return max(set(t), key=t.count)


    def get_repeats(self, b) :
        r = self.r
        domain = range(0, len(b), r)
        return [ b[i : i+r] for i in domain ]


    def decode(self, b) :
        reps = self.get_repeats(b)
        votes = ''.join(self.majority(t) for t in reps)
        
        return bit_decode(votes)


class HammingCode() :
    def __init__(self, n=7, k=4) :
        self.n = n
        self.k = k
        self.H = self.checker(n, k)
        self.G = self.generator(self.H)

    # P
    def parity_submatrix(self, n, k) :
        j = n - k
        P = np.zeros((j, k), dtype=int)

        num2bin = lambda i : str(bin(i))[2:]
        isPowerOf2 = lambda n : (n & (n - 1)) == 0

        domain = range(n, 2, -1)
        domain = [i for i in domain if not isPowerOf2(i)]
        c = 0
        for i in domain:
            s = num2bin(i).zfill(j)
            P[:,c] = list(s)
            c += 1

        return P

    # H
    def checker(self, n, k):
        j = n - k
        P = self.parity_submatrix(n, k)
        I = np.identity(j)
        h = np.concatenate((P, I), axis=1)

        return h.astype(int)

    # G
    def generator(self, H):
        j, n = H.shape
        k = n - j
        I = np.identity(k)
        P = H[:, :-(n-k)]
        G = np.concatenate((I, P.T), axis=1)

        return G.astype(int)

    def get_repeats(self, b) :
        n = self.n
        domain = range(0, len(b), n)

        return [ b[i : i+n] for i in domain ]

    def nested_int(self, ll) :
        return [list(map(int, l)) for l in ll]

    def pad(self, block) :
        padlen = (self.k - len(block))
        padding = [0] * padlen

        return block + padding

    def split_into_blocks(self, b) :
        domain = range(0, len(b), self.k)
        blocks = [ list(b[i : i+self.k]) for i in domain ]
        blocks = self.nested_int(blocks)

        return np.array(blocks, dtype='object')

    def encode(self, s) :
        b = bit_encode(s)
        blocks = self.split_into_blocks(b)

        # handle ragged (non-k) lengths
        if len(blocks[-1]) != self.k :
           blocks[-1] = self.pad(blocks[-1])

        G = self.G
        t = [block @ G % 2 \
                for block in blocks]
        return arr2str(t)


    def correction(self, w, z) :
        H = self.H
        # Get syndrome
        position = np.where(np.all(z == H, axis=0))[0]
        if position.shape == (0,) :
            # uncorrectable
            return None 

        # else correctable
        idx = np.squeeze(position[0])
        w[idx] = int(not w[idx])

        return w

    def decode(self, r) :
        words = h.get_repeats(r)
        words = [list(w) for w in words]
        s_hat = ''.join([self.decode_word(word) for word in words])
        
        return bit_decode(s_hat)


    def decode_word(self, word) :
        H = self.H
        w = np.array([word]).astype(int).T
        z = H @ w % 2
        errorFree = np.count_nonzero(z) == 0

        if not errorFree:
            w = self.correction(w, z)

        s = w[:self.k].flatten() \
            if w is not None else ""

        return ''.join([str(a) for a in s])


if __name__ == '__main__':
    noise = 0.1
    print("with noise level", noise)

    channel = BinarySymmetricChannel(p=noise)

    s = "would be a shame if anything got flipped"

    t = bit_encode(s)
    print("Original: ", bit_decode(t))
    r = channel.transmit(t)
    print("Raw ", bit_decode(r))

    r3 = RepCode(r=3)
    t = r3.encode(s)    
    r = channel.transmit(t)
    print("R3: ", r3.decode(r))

    r7 = RepCode(r=7)
    t = r7.encode(s)    
    r = channel.transmit(t)
    print("R7: ", r7.decode(r))

    h = HammingCode(n=7, k=4)
    t = h.encode(s)
    r = channel.transmit(t)
    shat = h.decode(r)
    # Has an extra null byte if len(b) !mod k
    print("H7,4", shat[:-1])

    h = HammingCode(n=15, k=11)
    t = h.encode(s)
    r = channel.transmit(t)
    shat = h.decode(r)
    # Has an extra null byte if len(b) !mod k
    print("H15,11", shat[:-1])
