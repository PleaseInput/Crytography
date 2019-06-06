import sys
import math
from commonly_used import *
from Huffman import *
from RSA import *
from Rabin import *
import time
from random import randint
# import RSA
# import Rabin

sys.setrecursionlimit(4096)

def arsa(length, output_file_name):
    # ===== begin A-RSA encryption =====
    # 1.read a message
    encode_start = time.time()
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

    # r < 2**1024, due to the modulus of Rabin encryption
    r = bin(2)[2:]
    
    b_xor_r = str_xor(b_text, r)
    b_base64_bin2chr = base64_bin2chr(b_xor_r)
    print('b_text xor r: ', time.time()-rc)
    rc = time.time()

    # 3.encrypt H by RSA
    # cut h_text to many pieces, because h_text could be larger than the modulus of RSA 
    h_text_hex = hexify(h_text)
    h_pieces_bfRSA = [] # in hex str
    piece_size = 250    # 250 * 4 = 1000 < 1024
    num_of_piece = len(h_text_hex)//piece_size
    for i in range(num_of_piece):
        h_pieces_bfRSA += [h_text_hex[0+i*piece_size:piece_size+i*piece_size]]
    h_pieces_bfRSA += [h_text_hex[0+num_of_piece*piece_size:]]
    print('cut h_text in encode: ', time.time()-rc)
    rc = time.time()

    # encrypt each piece
    h_pieces_RSA_enc = [] # in package [c, d, n], all in int
    for i in h_pieces_bfRSA:
        h_text_int = int(i, 16)
        h_pieces_RSA_enc += [RSA_enc(h_text_int)]
    print('rsa h_text in encode: ', time.time()-rc)
    rc = time.time()

    # (c, d, n)
    # h_text_xor = ''
    # int->bin_str
    h_piece_af_1xor = []    # '10010'
    for i in h_pieces_RSA_enc:
        c_rsa_enc = i[0]
        h_piece_af_1xor += [str_xor(bin(c_rsa_enc)[2:], r)]
    print('xor h_text in encode: ', time.time()-rc)
    rc = time.time()

    # 4.encrypt r by Rabin
    r_int = int(r, 2)
    pad = int(1.0e4)
    m_pad = r_int * pad

    # enc:c, p, q, n
    enc = Rabin_enc(m_pad)
    print('rabin r in encode: ', time.time()-rc)
    rc = time.time()
    encode_end = time.time()
    encode_time = (encode_end-encode_start)
    # ===== end A-RSA encryption =====

    # ===== begin A-RSA decryption =====
    decode_start = time.time()
    rc = time.time()
    # 1.decrypt r by Rabin
    dec = Rabin_dec(enc)
    r_rabin_dec = 0
    for i in dec:
        if i%pad == 0:
            r_rabin_dec = i//pad
            break
    r_rabin_dec = bin(r_rabin_dec)[2:]
    print('rabin r in decode: ', time.time()-rc)
    rc = time.time()

    # 2.xor H and B
    # bin_str->int
    h_piece_af_2xor = []
    for i in h_piece_af_1xor:
        h_piece_af_2xor += [int(str_xor(i, r_rabin_dec),2)]
    print('xor h_text in decode: ', time.time()-rc)
    rc = time.time()

    b_text_dexor = str_xor(b_xor_r, r_rabin_dec)
    print('recover b_text in decode: ', time.time()-rc)
    rc = time.time()

    # 3.decrypt H by RSA
    h_pieces_RSA_dec = []   # in '10010'
    for i,j in zip(h_piece_af_2xor, h_pieces_RSA_enc):
        tmp = [i] + [j[1]] + [j[2]]
        h_pieces_RSA_dec += [hex(RSA_dec(tmp))[2:]]

    h_text_merge = ''
    for i in h_pieces_RSA_dec:
        h_text_merge += i

    h_text_dec = unhexify(h_text_merge)
    print('rsa h_text in decode: ', time.time()-rc)
    rc = time.time()

    # 4.decompression
    cut_ch = '/'
    code_book = {}
    text_tmp = ''
    for i in range(len(h_text_dec)):
        if (h_text_dec[i]==cut_ch) and (h_text_dec[i-1]!=cut_ch): 
            code_book[text_tmp[1:]] = text_tmp[0]
            text_tmp = ''
        else:
            text_tmp += h_text_dec[i]
    # print('code_book: ', code_book)
    print('recover h_text in decode: ', time.time()-rc)
    rc = time.time()

    # recover
    m = ''
    text_tmp = ''
    for i in b_text_dexor:
        text_tmp += i
        if text_tmp in code_book:
            m += code_book[text_tmp]
            text_tmp = ''
    print('recover text in decode: ', time.time()-rc)
    rc = time.time()

    decode_end = time.time()
    decode_time = decode_end - decode_start

    if text != m:
        input('error')

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
                    , 2**23:'8MB', 2**21*5:'10MB'}#, 2**24:'16MB'}
    # input_length = (64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 
    #                 2**15, 2**16, 2**17, 2**18, 2**19, 2**20, 2**21, 
    #                 2**22, 2**23, 2**21*5)#, 2**24)
    
    input_length = (2**22,)

    output_file_name = 'arsa_const.txt'

    test_times = 1
    record_encode_time = []
    record_decode_time = []
    for i in input_length:
        total_encode_time = 0.0
        total_decode_time = 0.0
        for j in range(test_times):
            tmp = arsa(i, output_file_name)
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
