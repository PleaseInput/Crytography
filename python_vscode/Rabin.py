from Miller_prime_test import *
def Rabin_enc(m):
    # key generation
    # p = Rabin_prime_test_64(510)
    # q = Rabin_prime_test_64(510)
    p = 23
    q = 31
    n = p * q

    # encryption
    c = ex_mod(m, 2, n)
    return c, p, q, n

def Rabin_dec(c, p, q, n):
    r = ex_mod(c, (p+1)/4, p)
    s = ex_mod(c, (q+1)/4, q)

    # res = r, s, t. where p*s + q*t = r
    res = ex_Eu(p, q)

    # aps:a*p*s. bqr:b*q*r
    aps = (res[1]*p*s)%n
    bqr = (res[2]*q*r)%n

    m1 = (aps+bqr)%n
    m2 = n-m1
    m3 = (aps-bqr)%n
    m4 = n-m3

    return [m1, m2, m3, m4]

# def main():
#     # enc:c, p, q, n
#     enc = Rabin_enc(100)
#     print(enc[0])
#     dec = Rabin_dec(enc[0], enc[1], enc[2], enc[3])
#     print(dec)

# main()