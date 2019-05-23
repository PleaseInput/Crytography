import random
# ===== 1.exponentail modulus =====
# a^e mod n. a, e, and n are integers. where a>0, e>=0, and n>0 
def ex_mod(a, e, n):
	if e == 0:
		return 1
	elif e == 1:
		return a%n
	elif e == 2:
		return (a**2)%n
	elif e%2 == 1:
		return (ex_mod(a, (e-1)//2, n)**2 * a)%n
	else:
		return (ex_mod(a, (e//2), n)**2)%n

# def main():
# 	for i in range(10):
# 		a = random.randint(1, 100)
# 		e = random.randint(1, 100)
# 		n = random.randint(2, 100)
# 		ans = ex_mod(a, e, n)
# 		print(a, e, n, ans)

# main()

# ===== 2.extended Euclidean algorithm =====
def ex_Eu(a, b):
    r0, s0, t0 = a, 1, 0
    r1, s1, t1 = b, 0, 1
    while True:
        if r1 == 0:
            return r0, s0, t0
        if r1 == 1:
            return r1, s1, t1
        q = r0 // r1
        r2, s2, t2 = r0-q*r1, s0-q*s1, t0-q*t1
        r0, s0, t0 = r1, s1, t1
        r1, s1, t1 = r2, s2, t2

# def main():
#     a = int(input('enter a: '))
#     b = int(input('enter b: '))
#     res = ex_Eu(a, b)
#     print('%d*%d + %d*%d = %d'%(a, res[1], b, res[2], res[0]))

# main()