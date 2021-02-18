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
        # Want tie-breaking so odd
        assert(n % 2 != 0)
        self.n = n
        self.k = k

    # TODO: generalise by building this from H
    def generator(self) :
        Gstring = ["1000",
                    "0100",
                    "0010",
                    "0001",
                    "1110",
                    "0111",
                    "1011"]
        G = [list(r) for r in Gstring]
        return np.array(G).astype(int).T

    def checker(self):
        Hstring = ["1110100",
                    "1101010",
                    "1011001"]
        H = [list(r) for r in Hstring]
        return np.array(H).astype(int).T

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

        if self.n == 7 and self.k == 4 :
            G = self.generator()
            t = [block @ G % 2 \
                    for block in blocks]
            return arr2str(t)
        else :
            raise NotImplementedError()


    def decode(self, r) :
        return [self.decode_word(word) for word in r]


    def decode_word(self, word) :
        if self.n == 7 and self.k == 4 :
            H = self.checker()
            z = H.T @ np.array([word]) # % 2
            s_is_zero = np.count_nonzero(z) == 0

            if not s_is_zero:
                print("Error!")

            return s[:self.k-1]
        else :
            raise NotImplementedError()


if __name__ == '__main__':
    noise = 0.1
    print("with noise level", noise)

    channel = BinarySymmetricChannel(p=noise)

    s = "would be a shame if anything got flipped"

    t = bit_encode(s)
    print("Original: ", bit_decode(t))
    r = channel.transmit(t)
    print("Raw: ", bit_decode(r))

    r3 = RepCode(r=3)
    t = r3.encode(s)    
    r = channel.transmit(t)
    print("R3: ", r3.decode(r))

    r9 = RepCode(r=9)
    t = r9.encode(s)    
    r = channel.transmit(t)
    print("R9: ", r9.decode(r))

    # h = HammingCode() 
    # t = h.encode(s)
    # r = channel.transmit(t)
    # print("H7,4: ", h.decode(r))
    