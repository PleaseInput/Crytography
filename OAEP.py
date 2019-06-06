import hashlib
# from mgf1 import mgf1
from binascii import hexlify
# from hashlib import sha256
from random import getrandbits

def i2osp(integer, size=4):
    # s = ''
    # for i in reversed(range(size)):
    #     s += chr((integer >> (8 * i)) & 0xFF)
    # return s
    return ''.join([chr((integer >> (8 * i)) & 0xFF) for i in reversed(range(size))])

'''
input: as hex
length: in bytes
output: in hex
'''
def mgf1(input, length):
    counter = 0
    output = ''
    while (len(output) < length):
        C = i2osp(counter, 4)
        # output += hash(input + C).encode('utf-8').digest()
        output += hashlib.sha256((input+C).encode('utf-8')).hexdigest()
        counter += 1
    return output[:length]

def bit2hex(input, length):
    return hex(int(input, 2))[2:].rjust(length, '0')

def hex2bit(input, length):
    return bin(int(input, 16))[2:].rjust(length, '0')

# in the same length
def bit_xor_bit(bits1, bits2):
    output = ''
    for i, j in zip(bits1, bits2):
        output += str(int(i)^int(j))
    return output

def get_bits(length):
    return bin(getrandbits(length))[2:].rjust(length, '0')

'''
input: bits e.g. '1011'
output: bits e.g. '11001001'
m + '0'(k1) + r(k0) 
'''
# input, r
def OAEP_enc(m):
    # n = 1024
    # len_m = 128
    # k0 = 512
    # n = 16
    # len_m = 4
    # k0 = 8
    n = 1000
    len_m = 128
    k0 = 500
    k1 = n-k0-len_m
    # m_0 = get_bits(len_m) + ('0'*k1)
    m_0 = m + ('0'*k1)
    r = get_bits(k0)

    # encode
    Gr = hex2bit(mgf1(r, (n-k0)//4), n-k0)
    X = bit_xor_bit(m_0, Gr)
    Hx = hex2bit(mgf1(X, k0//4), k0)
    Y = bit_xor_bit(Hx, r)
    m_enc = X + Y
    return m_enc

def OAEP_dec(m_enc):
    # n = 1024
    # len_m = 128
    # k0 = 512
    # n = 16
    # len_m = 4
    # k0 = 8
    n = 1000
    len_m = 128
    k0 = 500
    # k1: length of zeros
    k1 = n-k0-len_m

    # decode
    X = m_enc[:n-k0]
    Y = m_enc[n-k0:]
    Hx = hex2bit(mgf1(X, k0//4), k0)
    r = bit_xor_bit(Hx, Y)
    Gr = hex2bit(mgf1(r, (n-k0)//4), n-k0)
    m_0 = bit_xor_bit(X, Gr)
    
    return m_0[:-k1]

# def main():
#     m = get_bits(4)
#     m_enc = OAEP_enc(m)
#     m_dec = OAEP_dec(m_enc)
#     print(m, m_enc, m_dec)
    
# main()
