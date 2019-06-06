from tables import *
from time import time
from random import randint

# ----- begin key expansion -----
def key_expansion(key_str):
	# initialization
	key_list = get_block(key_str)
	# w0 to w3
	keys = [key_list[i:i+4] for i in range(0, 13, 4)]

	# main loop
	for i in range(4, 4*(Nr+1)):
		if i%4 == 0:
			tmp = RCon(Sub(RotWord(keys[i-1])), i//4)
		else:
			tmp = keys[i-1]
		keys += [xor(keys[i-4], tmp)]

	return [keys[0+4*i]+keys[1+4*i]+keys[2+4*i]+keys[3+4*i] for i in range(Nr+1)]

def RotWord(word):
	return word[1:]+word[:1]

# lis could be a 32-bit word or a 128-bit state
def Sub(lis):
	return [Sbox[i] for i in lis]

def RCon(word, run):
	word[0] ^= Rcon[run]
	return word

# two word do xor
def xor(w1, w2):
	return [a^b for a,b in zip(w1,w2)]

# from string '1234' in hexadecimal to int list [18 = 16*1+1*2, 52 = 16*3+1*4] in decimal
# get a string of key or state, and return a column major block
def get_block(s):
	# key_list = []
	# for i in range(0, 16, 2):
	# 	key_list += [s[i:i+2]]
	# return key_list
	return [int(s[i:i+2], 16) for i in range(0, 32, 2)]

# lis could be a 32-bit word or a 128-bit state
def print_hexword(lis):
	print([hex(i) for i in lis], end=' ')
# ----- end key expansion -----

# ----- begin AES encryption -----

# Sub() writen in key expansion

def ShiftRow(state):
	state[1], state[5], state[9], state[13] = state[5], state[9], state[13], state[1]
	state[2], state[6], state[10], state[14] = state[10], state[14], state[2], state[6]
	state[3], state[7], state[11], state[15] = state[15], state[3], state[7], state[11]
	return state

def MixCol(state):
	# mat = [
	# 0x02, 0x03, 0x01, 0x01,
	# 0x01, 0x02, 0x03, 0x01, 
	# 0x01, 0x01, 0x02, 0x03,
	# 0x03, 0x01, 0x01, 0x02
	# ]
	for i in range(4):
		new0 = mul_2[state[0+4*i]] ^ mul_3[state[1+4*i]] ^ state[2+4*i] ^ state[3+4*i]
		new1 = state[0+4*i] ^ mul_2[state[1+4*i]] ^ mul_3[state[2+4*i]] ^ state[3+4*i]
		new2 = state[0+4*i] ^ state[1+4*i] ^ mul_2[state[2+4*i]] ^ mul_3[state[3+4*i]]
		new3 = mul_3[state[0+4*i]] ^ state[1+4*i] ^ state[2+4*i] ^ mul_2[state[3+4*i]]
		state[0+4*i], state[1+4*i], state[2+4*i], state[3+4*i] = new0, new1, new2, new3
	return state

def AddKey(state, key):
	return [a^b for a,b in zip(state, key)]

'''
input:
	state_str: e.g. '54776F204F6E65204E696E652054776F'
	keys: a list contains all keys 
output:
	state_str : hex e.g. '29c3505f571420f6402299b31a02d73a'
	# state_str: ascii e.g. ')ÃP_W ö@"³╗×:'
'''
def AES_enc(state_str, keys):
	# become a block from a string
	state_lis = get_block(state_str)

	# start AES
	state_lis = AddKey(state_lis, keys[0])

	for i in range(1, 10):
		state_lis = AddKey(MixCol(ShiftRow(Sub(state_lis))), keys[i])

	state_lis = AddKey(ShiftRow(Sub(state_lis)), keys[Nr])
	
	state_str = ''
	for i in state_lis:
		state_str += hex(i)[2:].rjust(2, '0')
	return state_str
	
	## string is immutable, so state_str is a copy.
	# state_str = ''
	# for i in state_lis:
	# 	state_str += chr(i)
	# return state_str

# ----- end AES encryption -----
# ----- begin AES decryption -----
def inv_Sub(lis):
	return [inv_Sbox[i] for i in lis]

def inv_ShiftRow(state):
	state[1], state[5], state[9], state[13] = state[13], state[1], state[5], state[9]
	state[2], state[6], state[10], state[14] = state[10], state[14], state[2], state[6]
	state[3], state[7], state[11], state[15] = state[7], state[11], state[15], state[3]
	return state

def inv_MixCol(state):
	# mat = [
	# 0x0e, 0x0b, 0x0d, 0x09,
	# 0x09, 0x0e, 0x0b, 0x0d, 
	# 0x0d, 0x09, 0x0e, 0x0b,
	# 0x0b, 0x0d, 0x09, 0x0e
	# ]
	for i in range(4):
		new0 = mul_14[state[0+4*i]] ^ mul_11[state[1+4*i]] ^ mul_13[state[2+4*i]] ^ mul_9[state[3+4*i]]
		new1 = mul_9[state[0+4*i]] ^ mul_14[state[1+4*i]] ^ mul_11[state[2+4*i]] ^ mul_13[state[3+4*i]]
		new2 = mul_13[state[0+4*i]] ^ mul_9[state[1+4*i]] ^ mul_14[state[2+4*i]] ^ mul_11[state[3+4*i]]
		new3 = mul_11[state[0+4*i]] ^ mul_13[state[1+4*i]] ^ mul_9[state[2+4*i]] ^ mul_14[state[3+4*i]]
		state[0+4*i], state[1+4*i], state[2+4*i], state[3+4*i] = new0, new1, new2, new3
	return state

# AddKey() writen in AES encryption.

def AES_dec(state_str, keys):
	# become a block from a string
	state_lis = get_block(state_str)

	# start AES
	state_lis = AddKey(state_lis, keys[10])
	state_lis = inv_ShiftRow(state_lis)
	state_lis = inv_Sub(state_lis)

	for i in range(9, 0, -1):
		state_lis = AddKey(state_lis, keys[i])
		state_lis = inv_MixCol(state_lis)
		state_lis = inv_ShiftRow(state_lis)
		state_lis = inv_Sub(state_lis)

	state_lis = AddKey(state_lis, keys[0])

	state_str = ''
	for i in state_lis:
		state_str += hex(i)[2:].rjust(2, '0')
	return state_str

	# # string is immutable, so state_str is a copy.
	# state_str = ''
	# for i in state_lis:
	# 	state_str += chr(i)
	# return state_str

# ----- end AES decryption -----

# # 10**4 times average: 0.0013656543970108031 (sec)
# def main():
# 	key_str = '5468617473206D79204B756E67204675'
# 	keys = key_expansion(key_str)
	
# 	# state_str = '54776F204F6E65204E696E652054776F'
# 	start = time()
# 	for i in range(10**4):
# 		state_str = ''
# 		for i in range(32):
# 			state_str += hex(randint(0, 15))[2]
# 		state_enc = AES_enc(state_str, keys)
# 		state_dec = AES_dec(state_enc, keys)
# 		if state_str!=state_dec:
# 			print(state_str, state_dec)
# 			return
# 	end = time()
# 	print((end-start)/10**4)

# main()