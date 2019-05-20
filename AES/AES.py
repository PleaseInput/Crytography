from tables import *

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

# ----- begin AES -----

# Sub() writen in key expansion

def ShiftRow(state):
	state[1], state[5], state[9], state[13] = state[5], state[9], state[13], state[1]
	state[2], state[6], state[10], state[14] = state[10], state[14], state[2], state[6]
	state[3], state[7], state[11], state[15] = state[15], state[3], state[7], state[11]
	return state

def MixCol(state):
	# mat = [0x2, 0x3, 0x1, 0x1,
	# 	   0x1, 0x2, 0x3, 0x1, 
	# 	   0x1, 0x1, 0x2, 0x3,
	# 	   0x3, 0x1, 0x1, 0x2]
	for i in range(4):
		new0 = mul_2[state[0+4*i]] ^ mul_3[state[1+4*i]] ^ state[2+4*i] ^ state[3+4*i]
		new1 = state[0+4*i] ^ mul_2[state[1+4*i]] ^ mul_3[state[2+4*i]] ^ state[3+4*i]
		new2 = state[0+4*i] ^ state[1+4*i] ^ mul_2[state[2+4*i]] ^ mul_3[state[3+4*i]]
		new3 = mul_3[state[0+4*i]] ^ state[1+4*i] ^ state[2+4*i] ^ mul_2[state[3+4*i]]
		state[0+4*i], state[1+4*i], state[2+4*i], state[3+4*i] = new0, new1, new2, new3
	return state

def AddKey(state, key):
	return [a^b for a,b in zip(state, key)]

def AES(state, keys):
	# become a block from a string
	state = get_block(state)

	# start AES
	state = AddKey(state, keys[0])

	for i in range(1, 10):
		state = AddKey(MixCol(ShiftRow(Sub(state))), keys[i])

	return AddKey(ShiftRow(Sub(state)), keys[Nr])

# ----- end AES -----

def main():
	key_str = '5468617473206D79204B756E67204675'
	keys = key_expansion(key_str)
	# for i in range(len(keys)):
	# 	print_hexword(keys[i])
	# 	if i%4 == 3:
	# 		print()
	
	state_str = '54776F204F6E65204E696E652054776F'
	# state_str = '001f0e543c4e08596e221b0b4774311a'
	# state = get_block(state_str)
	# state = MixCol(ShiftRow(Sub(state)))
	# print_hexword(state)
	# print()
	# # tmp_key = keys[4]+keys[5]+keys[6]+keys[7]
	# print_hexword(keys[1])
	# print()
	# print_hexword(AddKey(state, keys[1]))
	print_hexword(AES(state_str, keys))

main()
	