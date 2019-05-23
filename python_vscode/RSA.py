from Miller_prime_test import *
def RSA_enc(m):
    # key generation
    p = prime_test_64(512)
    q = prime_test_64(512)
    n = p * q
    phi_n = (p-1) * (q-1)
    e = 65537    # commonly used e
    d = ex_Eu(phi_n, e)[2]
    if d<0:
        d += phi_n
    
    # encryption
    c = ex_mod(m, e, n)
    
    return c, d, n

def RSA_dec(c, d, n):
    # decrption
    return ex_mod(c, d, n)

# def main():
#     ans = RSA(100)
#     print(ans)

# main()