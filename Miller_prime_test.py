import random
from commonly_used import *
import time

def miller_rabin(n):
	if n<2:
		return False
	a = random.randint(2,n-1)
	# a = 137
	u,t = n-1,0
	# a^(u*2^t)
	while u%2==0:
		u >>= 1	# u is odd
		t += 1
	x = ex_mod(a, u, n)
	# 2^0
	if x==1 or x==n-1:
		return True
	# 2^1 to 2^t-1
	for i in range(1, t):
		x = ex_mod(x, 2, n)
		if x==1:
			return False
		if x==n-1:
			return True
	return False

'''
length = 2
2**2(10) == 4(10) == 100(2) == 1<<2 == 3 bits
so, length -> (length+1) bits

if we would like to do length -> length bits,
1<<(length-1)
'''
def prime_test_64(length):
	test_time = 1	# i-th test
	# n = random.randint(2**length, 2**(length+1)-1)
	n = random.randint(1<<)
	while test_time<=64:
		if miller_rabin(n):
			test_time += 1
		else:
			test_time = 1	# i-th test
			n = random.randint(2**length, 2**(length+1)-1)
	return n

def Rabin_prime_test_64(length):
	test_time = 1	# i-th test
	# k:510 bits
	n = random.randint(2**length, 2**(length+1)-1)
	
	# n = 4*k + 3
	# 512 bits
	n <<= 2
	n += 3
	gate = 64
	while test_time<=gate:
		if miller_rabin(n):
			test_time += 1
		else:
			test_time = 1	# i-th test
			n = random.randint(2**length, 2**(length+1)-1)
	return n
	
# after running 100 times. 
# gate: 64
# max:14.37(sec)
# min:0.20(sec)
# avg after deleting max and min:2.52(sec)

# after running 100 times. 
# gate: 64
# max:10.92(sec)
# min:0.1988(sec)
# avg after deleting max and min:2.5252(sec)
# avg w/ del: 2.58588(sec)

# after running 100 times. 
# gate: 8
# avg af del max and min: 2.257(sec)

def main():
	total_time = []
	for i in range(100):
		start = time.time()
		prime_test_64(510)
		# print(prime_test_64())
		end = time.time()
		print(i)
		# print(end-start)
		total_time += [end-start]
	print(max(total_time), min(total_time))
	total_time.pop(total_time.index(max(total_time)))
	total_time.pop(total_time.index(min(total_time)))
	print(sum(total_time)/98)

# main()

