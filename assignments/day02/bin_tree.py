#! /usr/bin/python3

import math

class Node:
    def __init__(self, data):
        self.value = data
        self.smaller = None
        self.larger = None

    def __str__(self):
        return str(self.value)

class BinTree:
    def __init__(self, A = None):
        # A is an optional argument containing a list of values to be inserted into the binary tree just after cosntruction
        self.start_node = None
        if A:
          for value in A:
            self.insert(value)

    def insert(self, V):
        # inserts a new value
        node = Node(V)
        if self.start_node == None:
          self.start_node = node
          return
         # cycle to find the appropriate spot
        cur = self.start_node
        prev_cur = cur
        while cur:
            prev_cur = cur
            # if V is greater, descend right
            if V > cur.value:
                cur = cur.larger
            # if V is smaller, descend left
            elif V < cur.value:
                cur = cur.smaller
            # if V is equal to a current node, just drop it
            else:
                return
        # add in the new node
        if V > prev_cur.value:
            prev_cur.larger = node
        elif V < prev_cur.value:
            prev_cur.smaller = node

    def has(self, V):
        # returns True if V is in the list, else False
        cur = self.start_node
        prev_cur = cur
        while cur:
            prev_cur = cur
            # if V is greater, descend right
            if V == cur.value:
                return True
            elif V > cur.value:
                cur = cur.larger
            # if V is smaller, descend left
            else:
                cur = cur.smaller
        #if it reaches this point, it's not in the tree
        return False

    def get_ordered_list(self):
        # returns a list of all values in ordered sequence
        # return [int(num) for num in self.start_node.get_ordered_string()]
        def ordered_helper(node):
            '''
            in-order traversal.
            uses lists to make concatonation more efficient.
            list elements are joined at the end using extend().
            '''
            sequence_list = []
            if node.value == None:
                return []
            if node.smaller == None and node.larger == None:
                # print(node.value)
                return [node.value]
            if node.smaller:
                sequence_list.extend(ordered_helper(node.smaller))
            sequence_list.append(node.value)
            if node.larger:
                sequence_list.extend(ordered_helper(node.larger))
            return sequence_list

        return ordered_helper(self.start_node)

    def clear(self):
        # clears the list of all nodes
        def clear_helper(node):
            '''
            clear helper using a post-order traversal.
            will print each node as it is deleted.
            '''
            if node.smaller == None and node.larger == None:
                # print('Node {} deleted!'.format(node))
                node.smaller = None
                node.larger = None
                node.value = None
                return
            if node.smaller:
                clear_helper(node.smaller)
            if node.larger:
                clear_helper(node.larger)
            # kill self
            print('Node {} deleted!'.format(node))
            node.value = None
            node.smaller = None
            node.larger = None

        clear_helper(self.start_node)

    def has_depth(self, V):
        '''
        Finds V and returns the # of nodes traversed.
        '''
        total = 0
        cur = self.start_node
        prev_cur = cur
        while cur:
            total += 1
            prev_cur = cur
            # if V is greater, descend right
            if V == cur.value:
                return total
            elif V > cur.value:
                cur = cur.larger
            # if V is smaller, descend left
            else:
                cur = cur.smaller
        #if it reaches this point, it's not in the tree
        return total

def process(in_file_name, out_file_name):
    '''
    Takes in a file location, uses BinaryTree.has_depth on it, and inputs the new values into the out_file_name.
    '''
    f = open(in_file_name, 'r')
    lines = f.read().split('\n')
    words = lines[0].split(',')
    ints = [int(x) for x in words]
    tree = BinTree(ints)
    # second line ops
    second_words = lines[1].split(',')
    second_ints = [int(x) for x in second_words]
    depths = [tree.has_depth(x) for x in second_ints]
    print('Average:', sum(depths) / len(depths))
    print('Length of tree after log:', math.log(len(tree.get_ordered_list()),2))
    f.close()
    # write all depths into the second file
    f = open(out_file_name, 'w')
    depths = [str(x) for x in depths]
    string_depths = ','.join(depths)
    f.write(string_depths+'\n')
    f.close()

if __name__ == '__main__':
    import sys
    process(sys.argv[1], sys.argv[2])
