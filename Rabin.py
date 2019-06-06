from Miller_prime_test import *
def Rabin_enc(m):
    # key generation
    # p = Rabin_prime_test_64(510)
    # q = Rabin_prime_test_64(510)
    # p = 7
    # q = 11
    length = 510
    p = Rabin_prime_test_64(length)
    q = Rabin_prime_test_64(length)
    # p = 24633088797815626894744467597591692738458191121581872928857868615310538505501364675862227464736783085011419890682019688797040663923056161612976437245908367
    # q = 5251060522592118834507896972399916957927010388603361706098560584987018569117274203988445818079020886437228860780059260735237998404068429533191966434826371
    n = p * q

    # encryption
    c = ex_mod(m, 2, n)
    return c, p, q, n

# pak: c, p, q, n
def Rabin_dec(pak):
    c, p, q, n = pak[0], pak[1], pak[2], pak[3]

    r = ex_mod(c, (p+1)//4, p)
    s = ex_mod(c, (q+1)//
    4, q)

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

def main():
    m = 100
    # pad = 1
    pad = int(1.0e4)
    m_pad = m * pad
    print('m_pad: ', m_pad)

    # enc:c, p, q, n
    enc = Rabin_enc(m_pad)
    print('encrypted output: ', enc[0])
    # dec = Rabin_dec(enc[0], enc[1], enc[2], enc[3])
    dec = Rabin_dec(enc)
    for i in dec:
        if i%pad == 0:
            print('decrypted output: ', i//pad)
            break
    # for i in dec:
    #     if i%pad == 0:
    #         print(i%pad)

# main()