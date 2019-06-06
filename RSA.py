import sys
import time
from Miller_prime_test import *
from random import randint


sys.setrecursionlimit(4096)

def RSA_enc(m):
    # key generation
    rc = time.time()
    p = prime_test_64(512)
    q = prime_test_64(512)
    print('get two primes: ', time.time()-rc)
    rc = time.time()
    # p, q = 23, 29
    # p = 24633088797815626894744467597591692738458191121581872928857868615310538505501364675862227464736783085011419890682019688797040663923056161612976437245908367
    # q = 5251060522592118834507896972399916957927010388603361706098560584987018569117274203988445818079020886437228860780059260735237998404068429533191966434826371
    n = p * q
    phi_n = (p-1) * (q-1)
    e = 65537    # commonly used e
    # e = 97
    d = ex_Eu(phi_n, e)[2]
    if d<0:
        d += phi_n
    
    # encryption
    c = ex_mod(m, e, n)
    print('ex_mod c^e mod n: ', time.time()-rc)
    rc = time.time()
    return c, d, n

# pak: [c, d, n]
def RSA_dec(pak):
    # decrption
    return ex_mod(pak[0], pak[1], pak[2])

'''
if keep the p and q in the sender, the sender can decrypt the message by CRT as follows
http://jianiau.blogspot.com/2014/05/rsa-decrypt-with-crt.html
'''
def RSA_enc_keep(m):
    # key generation
    # p = prime_test_64(512)
    # q = prime_test_64(512)
    p, q = 23, 29
    n = p * q
    phi_n = (p-1) * (q-1)
    # e = 65537    # commonly used e
    e = 97
    d = ex_Eu(phi_n, e)[2]
    if d<0:
        d += phi_n
    
    # encryption
    c = ex_mod(m, e, n)
    
    # preparation of decryption by CRT
    dp = d%(p-1)
    dq = d%(q-1)
    qinv = ex_Eu(p, q)[2]
    if qinv<0:
        qinv += p

    return c, p, q, dp, dq, qinv

def RSA_dec_keep(c, p, q, dp, dq, qinv):
    # decrption
    m1 = ex_mod(c, dp, p)
    m2 = ex_mod(c, dq, q)
    k = (qinv*(m1-m2))%p
    return m2+k*q

'''
2**2 <= m <= 2**1024-1
average 10 times RSA encode and decode time: 5.72 (sec)
'''
# def main():
#     start = time.time()
#     for i in range(10):
#         m = randint(2**2, (2**1024)-1)
#         m_rsa_enc = RSA_enc(m)
#         m_rsa_dec = RSA_dec(m_rsa_enc)
#         if m != m_rsa_dec:
#             print(m, m_rsa_enc, m_rsa_dec)
#             input('error: ')
#     end = time.time()
#     print((end-start)/10)

# main()