from Huffman import *

def str_xor(str1: b_text, str2: r) -> str3:
    pass

def main():
    name = 'input.txt'
    fin = open(name, 'r', encoding='utf-8')
    if not fin:
        print('fail to open', name)
    else:
        print('success to open', name)
    text = fin.read()
    fin.close()
    print(text)

    b_text = Huffman(text)
    r = bin(2)[2:]

main()
