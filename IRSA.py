import sys
import math
import time
import commonly_used

from random import randint
from Huffman import *
from AES import *
from RSA import *
from OAEP import *

sys.setrecursionlimit(4096)

'''
input:
    text_bf: 16 bytes in ascii. e.g. 'g101' just between 0x0 to 0xf
    key_str: a string in hex. e.g. '54...0e'
output:
    text_af: in base64
encrypt a text by AES
1. convert text_bf into hexidecimal as an input of AES. e.g. 'g101'(ascii)->'67313031'(hex)
2. encrypt by AES and get a encrypted output in ascii
3. deal with the last remaining bytes according to PKCS#7's padding
4. convert this output into base64 for non printable characters
'''
def AES_enc_text(text_bf, key_str):
    keys = key_expansion(key_str)

    jump = 16
    # c: how many 16 bytes there are?
    c = len(text_bf)//jump
    text_af = ''
    for i in range(c):
        # ----- step 1 -----
        # e.g. 'a101'
        state_str = text_bf[0+jump*i:jump+jump*i]
        # e.g. 'a101' -> '61313031' (base=16) due to 'a'=0x61, '1'=0x31, and '0'=0x30 
        state_str = hexify(state_str)
        
        # ----- step 2 -----
        # here, text_af is in hex.
        text_af += AES_enc(state_str, keys)
    
    # ----- step 3 -----
    '''
    ... + 'last_bytes' + 'need_bytes'. 
    need_bytes: a string in hex
    1. if last_bytes is just 16 bytes, need_bytes should be '00...00' (base=16)
    2. if last_bytes is not, pad some bytes. e.g. '0102...0e' in hex just 15 bytes.
       it needs 1 byte, so we pad 01. '0102...0e'->'0102...0e01' is our last_bytes.
       and need_bytes is '01'
    this method guarantees the last byte must be a padding.
    '''
    if len(text_bf)%jump == 0:
        need_bytes = '00'*16
        # here, text_af is in hex.
        text_af += AES_enc(need_bytes, keys)
    else:
        # last_bytes: e.g. '0Z*...&'(ascii) just 15 bytes
        last_bytes = text_bf[0+jump*c:]

        # e.g. dif: 1
        dif = jump - len(last_bytes)
        # e.g. need_bytes: 1->'01'
        need_bytes = hex(dif)[2:].rjust(2, '0')
        # e.g. need_bytes: '01'*1
        need_bytes *= dif

        # last_bytes: e.g. '0Z*...&'(ascii)->'0102...0e'(hex)
        last_bytes = hexify(last_bytes)
        # last_bytes: e.g. '0102...0e'->'0102...0e01'
        last_bytes += need_bytes

        # encrypt last_bytes and add to text_af
        # here, text_af is in hex.
        text_af += AES_enc(last_bytes, keys)
    
    # ----- step 4 -----
    # hex->ascii
    text_af = unhexify(text_af)
    text_af = ascii_chr2bin(text_af)
    text_af = base64_bin2chr(text_af)

    return text_af

'''
input:
    text_bf: in base64
    key_str: in hex
output:
    text_af: in ascii
'''
def AES_dec_text(text_bf, key_str):
    keys = key_expansion(key_str)

    # text_dec_in: hex
    text_dec_in = ''
    for i in text_bf:
        text_dec_in += Base64_chr2bin[i]
    # cut padding
    pad = text_dec_in[-6:]
    len_pad = int(pad, 2)
    if len_pad==0:
        text_dec_in = text_dec_in[:-6]
    else:
        text_dec_in = text_dec_in[:-6-len_pad]
    text_dec_in = ascii_bin2chr(text_dec_in)
    text_dec_in = hexify(text_dec_in)

    # text_dec_out: hex
    text_dec_out = ''
    for i in range(0, len(text_dec_in), 32):
        text_dec_out += AES_dec(text_dec_in[i:i+32], keys)

    len_pad = int(text_dec_out[-2:], 16)
    if len_pad==0:
        return unhexify(text_dec_out[:-32])
    else:
        return unhexify(text_dec_out[:-len_pad*2])

'''
comment 1.file 2.print
'''
def irsa(length, output_file_name):
    # ===== begin I-RSA encryption =====
    encode_start = time.time()
    # 1.read a message
    rc = time.time()
    text = ''
    for i in range(length):
        text += chr(randint(32, 126))
    print('get text: ', time.time()-rc)
    rc = time.time()
    # 2.Huffman coding
    h_text, b_text = Huffman(text)
    print('huffman text: ', time.time()-rc)
    rc = time.time()

    r = bin(2)[2:]
    b_xor_r = str_xor(b_text, r)
    print('b_text xor r in encode: ', time.time()-rc)
    rc = time.time()
    
    b_base64_bin2chr = base64_bin2chr(b_xor_r)
    print('b_text to base64: ', time.time()-rc)
    rc = time.time()

    # 3.encrypt H and r by AES
    cut_ch = '/'
    h_r_ascii = h_text + r + cut_ch

    key_str = '5468617473206D79204B756E67204675'
    h_r_aes_enc = AES_enc_text(h_r_ascii, key_str)
    print('aes h_r_text in encode: ', time.time()-rc)
    rc = time.time()

    # 4.encrypt AES key by RSA and OAEP
    key_int = int(key_str, 16)
    key_bits = bin(key_int)[2:].rjust(128, '0')
    key_str_oaep_enc = OAEP_enc(key_bits)
    print('oaep key in encode: ', time.time()-rc)
    rc = time.time()

    key_int_oaep_enc = int(key_str_oaep_enc, 2)
    key_rsa_enc = RSA_enc(key_int_oaep_enc)
    print('rsa key in encode: ', time.time()-rc)

    encode_end = time.time()
    encode_time = (encode_end-encode_start)
    # ===== end I-RSA encryption =====

    # ===== begin I-RSA decryption =====
    decode_start = time.time()
    # 1.decrypt AES key by RSA and OAEP
    rc = time.time()
    key_int_rsa_dec = RSA_dec(key_rsa_enc)
    print('rsa key in decode: ', time.time()-rc)
    rc = time.time()

    key_str_rsa_dec = bin(key_int_rsa_dec)[2:].rjust(1000, '0')
    key_str_oaep_dec = OAEP_dec(key_str_rsa_dec)
    key_int_oaep_dec = int(key_str_oaep_dec, 2)
    key_str_dec = hex(key_int_oaep_dec)[2:] 
    print('oaep key in decode: ', time.time()-rc)
    rc = time.time()

    if key_int!=key_int_oaep_dec:
        print('AES key is not correct.')
        return

    # 2.decrypt H and r by AES in ascii
    h_r_aes_dec = AES_dec_text(h_r_aes_enc, key_str)
    print('aes h_r_text in decode: ', time.time()-rc)
    rc = time.time()

    # 3.decompression
    # h and r
    # .../r/
    # left '/' index
    r_index = h_r_aes_dec.rfind(cut_ch, 0, len(h_r_aes_dec)-1)
    r = h_r_aes_dec[r_index+1:len(h_r_aes_dec)-1]
    h = h_r_aes_dec[:r_index+1]

    code_book = {}
    text_tmp = ''
    for i in range(len(h)):
        if (h[i]==cut_ch) and (h[i-1]!=cut_ch): 
            code_book[text_tmp[1:]] = text_tmp[0]
            text_tmp = ''
        else:
            text_tmp += h[i]
    print('recover h_text and r in decode: ', time.time()-rc)
    rc = time.time()

    # b
    b = str_xor(b_xor_r, r)
    print('recover b_text in decode: ', time.time()-rc)
    rc = time.time()
    # recover
    m = ''
    text_tmp = ''
    for i in b:
        text_tmp += i
        if text_tmp in code_book:
            m += code_book[text_tmp]
            text_tmp = ''
    print('recover text in decode: ', time.time()-rc)
    rc = time.time()

    if text!=m:
        print("error %d, %s"%(length, output_file_name))
        input('error')

    decode_end = time.time()
    decode_time = decode_end - decode_start
    # ===== end I-RSA decryption =====

    # fout = open(output_file_name, 'a', encoding='utf-8')
    # t = time.strftime("%Y-%m-%d %H:%M:%S\n", time.localtime())
    # fout.write('%d, %s: ' % (length, output_file_name)
    # fout.write('record date: ' + t + '\n')
    # fout.write('encode time: %f\n'%encode_time)
    # fout.write('decode time: %f\n'%decode_time)
    # fout.write('=============================================================\n')
    # fout.close()

    return encode_time, decode_time

def main():
    # 64, 128, 256, 512, 1024(1k), 2048(2k), 4096(4k), 8192(8k),
    # 16384(16k), 2**15(32k), 2**16(64k), 2**17(128k), 2**18(256k),
    # 2**19(512k), 2**20(1m), 2**21(2m), 2**22(4m), 2**23(8m), 2**24(16m)
    convert_name = {64:'64B', 128:'128B', 256:'256B', 512:'512B', 
                    1024:'1KB', 2048:'2KB', 4096:'4KB', 8192:'8KB', 
                    16384:'16KB', 2**15:'32KB', 2**16:'64KB', 
                    2**17:'128KB', 2**18:'256KB', 2**19:'512KB', 
                    2**20:'1MB', 2**21:'2MB', 2**22:'4MB', 2**21*3:'6MB'
                    , 2**23:'8MB', 2**21*5:'10MB', 2**24:'16MB'}

    # input_length = (64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 
    #                 2**15, 2**16, 2**17, 2**18, 2**19, 2**20, 2**21, 
    #                 2**22, 2*21*3, 2**23, 2**21*5, 2**24)
    input_length = (2**22,)

    output_file_name = 'irsa_not_const.txt'

    test_times = 2
    record_encode_time = []
    record_decode_time = []
    for i in input_length:
        total_encode_time = 0.0
        total_decode_time = 0.0
        for j in range(test_times):
            tmp = irsa(i, output_file_name)
            total_encode_time += tmp[0]
            total_decode_time += tmp[1]
            print('%s in %d times'%(convert_name[i], j))
            print('total encode time: ', total_encode_time)
            print('total decode time: ', total_decode_time)
        record_encode_time += [total_encode_time]
        record_decode_time += [total_decode_time]

    # fout = open(output_file_name, 'a', encoding='utf-8')
    # index = 0
    # for i in input_length:
    #     fout.write('encode %s: %f \n'%(convert_name[i], record_encode_time[index]/test_times))
    #     fout.write('decode %s: %f \n'%(convert_name[i], record_decode_time[index]/test_times))
    #     fout.write('======================================================= \n')
    #     index += 1
    # fout.close()

main()

    # input_length = (64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 
    #                 2**15, 2**16, 2**17, 2**18, 2**19)
    # output_file_name = ('irsa_64b.txt', 'irsa_128b.txt', 'irsa_256b.txt', 
    #                     'irsa_512b.txt', 'irsa_1kb.txt','irsa_2k.txt', 
    #                     'irsa_4k.txt', 'irsa_8k.txt', 'irsa_16k.txt', 
    #                     'irsa_32k.txt', 'irsa_64k.txt', 'irsa_128k.txt', 
    #                     'irsa_256k.txt', 'irsa_512k.txt')
    
    # input_length = (2**19,)
    # output_file_name = ('irsa_512k.txt')

    # test_times = 5
    # record_encode_time = []
    # record_decode_time = []
    # for i in range(len(input_length)):
    #     total_encode_time = 0.0
    #     total_decode_time = 0.0
    #     for j in range(test_times):
    #         tmp = irsa(input_length[i], output_file_name[i])
    #         total_encode_time += tmp[0]
    #         total_decode_time += tmp[1]
    #         print('%d in %d times'%(input_length[i], j))
    #     record_encode_time += [total_encode_time]
    #     record_decode_time += [total_decode_time]
    # # # print('1m encode total/avg: %f/%f\n'%(total_encode_time, total_encode_time/test_times))
    # # # print('1m decode total/avg: %f/%f\n'%(total_decode_time, total_decode_time/test_times))
    # for i in range(len(input_length)):
    #     print('encode %d: %f'%(i+1, record_encode_time[i]/test_times))
    #     print('decode %d: %f'%(i+1, record_decode_time[i]/test_times))
    #     print('=======================================================')

    # input_file_name = ('test_1m.txt', 'test_2m.txt', 'test_4m.txt', 
    #                    'test_8m.txt', 'test_10m.txt',)
    # output_file_name = ('irsa_1m.txt', 'irsa_2m.txt', 'irsa_4m.txt', 
    #                     'irsa_8m.txt', 'irsa_10m.txt', )
    # test_times = 2
    # record_encode_time = []
    # record_decode_time = []
    # for i in range(5):
    #     total_encode_time = 0.0
    #     total_decode_time = 0.0
    #     for j in range(test_times):
    #         tmp = irsa(input_file_name[i], output_file_name[i])
    #         total_encode_time += tmp[0]
    #         total_decode_time += tmp[1]
    #         print('1m %d times'%j)
    #     record_encode_time += [total_encode_time]
    #     record_decode_time += [total_decode_time]
    # # print('1m encode total/avg: %f/%f\n'%(total_encode_time, total_encode_time/test_times))
    # # print('1m decode total/avg: %f/%f\n'%(total_decode_time, total_decode_time/test_times))
    # for i in range(5):
    #     print('encode %d: %f'%(i+1, record_encode_time[i]/test_times))
    #     print('decode %d: %f'%(i+1, record_decode_time[i]/test_times))
    #     print('=======================================================')
# main()