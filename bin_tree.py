class Node:
    def __init__(self, data):
        self.value = data
        self.smaller = None
        self.equal_or_larger = None

    def __str__(self):
        return str(self.value)

    def get_ordered_string(self):
        '''
        in-order traversal.
        '''
        sequence = ''
        if self.smaller == None and self.equal_or_larger == None:
            return str(self.value)
        if self.smaller:
            sequence += self.smaller.get_ordered_string()
        sequence += str(self.value)
        if self.equal_or_larger:
            sequence += self.equal_or_larger.get_ordered_string()
        return sequence

    def clear(self):
        '''
        clear helper using a post-order traversal.
        will print each node as it is deleted.
        '''
        if self.smaller == None and self.equal_or_larger == None:
            print('Node {} deleted!'.format(self))
            self = None
            return
        if self.smaller:
            self.smaller.clear()
        if self.equal_or_larger:
            self.equal_or_larger.clear()
        # kill self
        print('Node {} deleted!'.format(self))
        self = None

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
            if V >= cur.value:
                cur = cur.equal_or_larger
            # if V is smaller, descend left
            else:
                cur = cur.smaller
        # add in the new node
        if V >= prev_cur.value:
            prev_cur.equal_or_larger = node
        else:
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
                cur = cur.equal_or_larger
            # if V is smaller, descend left
            else:
                cur = cur.smaller
        #if it reaches this point, it's not in the tree
        return False

    def get_ordered_string(self):
        # returns a list of all values in ordered sequence
        return [int(num) for num in self.start_node.get_ordered_string()]

    def clear(self):
        # clears the list of all nodes
        self.start_node.clear()

if __name__ == '__main__':
    tree = BinTree([4,5,6,3,7])
    print('Do tree has 7???: ', tree.has(7))
    print('Do tree has 3???: ', tree.has(3))
    print('Do tree has 104???: ', tree.has(104))
    print('Printing ordered list:', tree.get_ordered_string())
    print('Clearing tree....')
    tree.clear()
