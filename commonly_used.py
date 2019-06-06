import random
from tables import Base64_bin2chr, Base64_chr2bin
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

# ===== 3.ascii <-> hex =====
# ascii -> int -> hex: 'a' -> 97 (base=10) -> 61 (base=16)
def hexify(ascii_str):
    hex_str = ''
    for i in ascii_str:
        hex_str += hex(ord(i))[2:].rjust(2, '0')
    return hex_str

'''
input:
    hex_str: a string in hex. e.g. '0f5a' between 0x0 to 0xf
output:
    ascii_str: a string in ascii. e.g. 'a*Z)'
hex -> int -> ascii: 61 (base=16) -> 97 (base=10) -> 'a'
'''
def unhexify(hex_str):
    ascii_str = ''
    for i in range(0, len(hex_str), 2):
        ascii_str += chr(int(hex_str[i:i+2], 16))
    return ascii_str

# def main():
#     ans = hexify('worker')
#     print(ans)
#     ans = unhexify(ans)
#     print(ans)
# #     a = int(input('enter a: '))
# #     b = int(input('enter b: '))
# #     res = ex_Eu(a, b)
# #     print('%d*%d + %d*%d = %d'%(a, res[1], b, res[2], res[0]))

# main()

# ===== others =====
# str1: b_text. str2: r. str3: output
def str_xor(str1, str2):
    str3 = ''
    tag = 0
    str2_len = len(str2)
    for i in str1:
        str3 += str(int(i, 2)^int(str2[tag], 2))
        # if str1 <= str2, then 'tag = (tag+1)%str2_len' doesn't matter.
        # if str1 > str2, then 'tag' will cycle. e.g. str1: '011'. str2: '10'
        tag = (tag+1)%str2_len
    return str3

'''
base64_bin2chr: e.g. '100100' -> 'g' It may not be correct, just an instance.
if not a multiple of 6 bits, pad zeros and pad a length information.
e.g. '10101'(bin)->'101010'(pad a zero)->'101010 000001'(pad a length information: we pad 1 zero)
if it is a multiple of 6 bits, pad 0's 0  and pad '000000' as the length informatiom
text_bf: text before base64
text_af: text after base64
'''
def base64_bin2chr(text_bf):
    # name = 'binary_file.txt'
    # fout = open(name, 'w', encoding='utf-8')
    jump = 6
    c = len(text_bf)//jump
    text_af = ''
    for i in range(c):
        key = text_bf[0+jump*i:jump+jump*i]
        text_af += Base64_bin2chr[key]
    # ... + 'last_bits' + 'need_bits'. if last_bits is just 6 bits, need_bits should be '000000'->'A'
    if len(text_bf)%jump == 0:
        text_af += 'A'
    else:
        # last_bits: '101'
        last_bits = text_bf[0+jump*c:]
        need_bits = bin(jump - len(last_bits))[2:]
        # last_bits: '101' -> '101000'
        last_bits = last_bits.ljust(jump, '0')
        
        # need_bits: '000011'. in last_bits, we add '000' (three zero), so need_bits is 3 ('11'->'000011'). 
        need_bits = need_bits.rjust(jump, '0')

        # add the last_bits to text_af
        text_af += Base64_bin2chr[last_bits]
        # add the need_bits to text_af
        text_af += Base64_bin2chr[need_bits]
    return text_af

'''
base64_chr2bin: inverse base64_bin2chr and cut the padding. e.g. 'A' = '000000'
it works with padded text_bf
'''
def base64_chr2bin(text_bf):
    text_af = ''
    for i in text_bf:
        text_af += Base64_chr2bin[i]
    # ... + last + need
    need = text_af[-6:]
    last = text_af[-12:-6]

    # the length of the original text is a multiple of 6.
    if need == '000000':
        return text_af[:-6]
    else:
        len_pad = int(need, 2)
        return text_af[:-6-len_pad]

def ascii_chr2bin(text_bf):
    text_af = ''
    for i in text_bf:
        text_af += bin(ord(i))[2:].rjust(8, '0')
    return text_af

def ascii_bin2chr(text_bf):
    jump = 8
    if (len(text_bf)%jump) != 0:
        print('the number of bits of ascii_bin2chr must be a multiple of %d.'%jump)
        return

    text_af = ''
    c = len(text_bf) // jump
    for i in range(c):
        order = int(text_bf[0+jump*i:jump+jump*i], 2)
        text_af += chr(order)
    return text_af

'''
tranfer a string from hex to base64 just for AES
e.g. '1a' (base=16) -> '0011000101100001' (ascii) '1': 0x31. 'a': 0x61 ->  MWEC (base64 by base64_bin2chr(text_bf))
text_bf: 16 bytes = 128 bits = 6*21 + 2
'''
# def AES_hex2base64(text_bf):
#     text_tmp = ascii_chr2bin(text_bf)
#     text_tmp = base64_bin2chr(text_tmp)