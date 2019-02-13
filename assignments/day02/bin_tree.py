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

    def get_ordered_string(self):
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

if __name__ == '__main__':
    tree = BinTree([4,5,6,3,3,7])
    print('Do tree has 7???:', tree.has_depth(7))
    print('Do tree has 3???:', tree.has_depth(3))
    print('Do tree has 104???:', tree.has_depth(104))
    # print('Printing ordered list:', tree.get_ordered_string())
    # print('Clearing tree....')
    # tree.clear()
    # print('Printing ordered list:', tree.get_ordered_string())
