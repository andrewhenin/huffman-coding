"""
This is an implementation of Huffman Coding
Written by: Andrew Henin (with the exception of the Node class)
Story:
    - Written by: Jorge Luis Borges
    - Translated by: Andrew Hurley
    - Provided by: Professor Neil Lutz
"""

import heapq

class Node:
    # This class is written by Professor Neil Lutz
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data  
        
def main():
    
    counter = 0
    result = ""
    
    #### open file and count symbols
    occ = {}
    f = open("./babel.txt", "r")
    f_content = f.read()
    f.close()
    f_len = len(f_content)
    f = open("./babel.txt", "r")
    for line in f:
        for c in line:
            if c in occ:
                occ[c] += 1
            else:
                occ[c] = 1           
    freq = {}
    for key in occ:
        freq[key] = occ[key]/f_len     
    f.close()
        
    #### occ, freq, f_len, f_conent are ready
    #### make and populate the priority queue
    pq = []
    for key in freq:
        new_node = Node(key)
        heapq.heappush(pq, ((freq[key], counter), new_node))
        counter += 1

    while len(pq) > 1:
        (x_tup, x) = heapq.heappop(pq)
        (y_tup, y) = heapq.heappop(pq)
        ## x_tup contains (freq, counter) and x contains Node(data)
        freq_x = x_tup[0]
        freq_y = y_tup[0]
        
        freq_xy = freq_x + freq_y
        data_xy = x.data + y.data
        
        new_node = Node(data_xy)
        new_node.left = x
        new_node.right = y
        
        heapq.heappush(pq, ((freq_xy, counter), new_node))
        counter += 1 
    
    tree_root = pq[0][1]

    binary_encodings = {}
    
    def dfs(node, running_encoding):
        if len(node.data) > 1:
            if node.left:
                dfs(node.left, running_encoding+"0")
            if node.right:
                dfs(node.right, running_encoding+"1")
        else:
            binary_encodings[node.data] = running_encoding
            return ""
    
    dfs(tree_root, "")

    result = ""
    f = open("./babel.txt", "r")
    for line in f:
        for c in line:
            result += binary_encodings[c]
    f.close()

    ## encoding done. now decoding
    decoded_str = ""
    ptr = 0
    curr_node = tree_root
    
    for b in result:
        if b == "1":
            curr_node = curr_node.right
        else:  # b == "0"
            curr_node = curr_node.left

        if curr_node.left is None and curr_node.right is None:
            decoded_str += curr_node.data
            curr_node = tree_root

    print(decoded_str) # this is the original story after encoding.
    
if __name__=="__main__":
    main()
