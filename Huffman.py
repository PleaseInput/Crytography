import os
import random
class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.left = None
        self.right = None

# wiki example: ffoooggggrrrreeeeettttttt
# I have an apple.
def Huffman(text):
    dic = {}
    for i in text:
        if i in dic:
            dic[i] += 1
        else:
            dic[i] = 1
    # print(dic)

    # construct a forest composed of nodes
    forest = []
    for i in dic:
        forest.append(Node(i, dic[i]))

    # construct a Huffman tree
    for i in range(len(forest)-1):
        forest = sorted(forest, key=lambda n:n.val)
        min_1 = forest.pop(0)
        min_2 = forest.pop(0)
        ptr = Node('', min_1.val+min_2.val)
        ptr.left = min_1
        ptr.right = min_2
        forest.insert(0, ptr)
    
    s = ''
    visit_node(s, forest[0], dic)
    # print(dic)

    # write the header file
    h_text = ''
    for i in dic:
        h_text += (i + dic[i] + '/')
    # print('h_text: ', h_text)
    h_name = 'header_file.txt'
    h_fout = open(h_name, 'w', encoding='utf-8')
    h_fout.write(h_text)
    h_fout.close()
    # write the binary file
    b_text = ''
    for i in text:
        b_text += dic[i]
    # print('b_text: ', b_text)
    b_name = 'binary_file.txt'
    b_fout = open(b_name, 'w', encoding='utf-8')
    b_fout.write(b_text)
    b_fout.close()

    return h_text, b_text

def visit_node(s, node, dic):
    if node==None:
        return
    if (node.left is None) & (node.right is None):
        # print(node.key, node.val, s)
        dic[node.key] = s
        return
    # print(node.val, s)
    visit_node(s+'0', node.left, dic)
    visit_node(s+'1', node.right, dic)

# def main():
#     # name = input('enter file name: ')
#     name = 'input.txt'
#     fin = open(name, 'r', encoding='utf-8')
#     if not fin:
#         print('fail to open', name)
#     else:
#         print('success to open', name)
#     text = fin.read()
#     fin.close()
#     print(text)
#     Huffman(text)

#     # name = 'output.txt'
#     # fout = open(name, 'w', encoding='utf-8')
#     # for i in range(10**6):
#     #     fout.write('ABCDEFGHIK')
#     # fout.close()
#     # fin = open(name, 'r', encoding='utf-8')
#     # text = fin.read()
#     # print(len(text))
#     # fin.close()
# main()