#! /usr/bin/python3

def process(infile, outfile):
    ret = []
    f = open(infile, 'r')
    lines = f.read().split('\n')
    for line in lines:
        line.split(',')
        for ele in line:
            if ele == '':
                line.remove(ele)
        if len(line) > 1:
            ret.append(line)
    dic = {ele[0]:sorted(ele[1:]) for ele in ret }
    titles = sorted([key for key in dic.keys()])
    ret_list = [','.join([title] + dic[title]) for title in titles]
    ret_list = '\n'.join(ret_list)
    g = open(outfile, 'w')
    g.write(ret_list)

class Node: # these contain only data, so
    # only __init__() is necessary
    # self.next and self.previous will be used as
    # pointers in the linked list
    def __init__(self,value):
        self.value = value
        self.next = None
        self.previous = None

class Dlist:
    def __init__(self):
        # your glorious code here
        self.first = Node(None)
        self.last = Node(None)

    def insert(self, value):
        if self.first.value == None:
            self.first.value = value
            return
        n_node = Node(value)
        node = self.first
        prev_node = node
        while node:
            # print(node.value)
            if node.value >= value:
                if node.previous == None and node.next == None:
                    node.previous = n_node
                    n_node.next = node
                    self.first = n_node
                    self.last = node
                    return
                elif node.previous == None:
                    node.previous = n_node
                    n_node.next = node
                    self.first = n_node
                n_node.previous = node.previous
                n_node.next = node
                node.previous.next = n_node
                node.previous = n_node
                return
            prev_node = node
            node = node.next

    def delete(self, value):
        # you code to remove the first occurrence of
        # value in the list and return True, or return False if not found
        node = self.first
        while node:
            print(node.value)
            if value == node.value:
                # forgot first edge case where first is only node
                if node.previous == None and node.next == None:
                    node.value = None
                    return True
                # forgot case where the matching element is the first node
                elif node.previous == None:
                    self.first = node.next
                    node.next.previous = None
                    node.value = None
                    node.next = None
                    return True
                # forgot last case as well
                if node.next:
                    node.previous.next, node.next.previous = node.next.previous, node.previous.next
                node.previous = None
                node.next = None
                node.value = None
                return True
            node = node.next
        return False


    def tolist(self):
        # your code to return a list of the values in order,
        # and remove all nodes in Dlist (return empty list if no nodes)
        node = self.first
        ret_list = []
        while node:
            val = node.value
            node = node.next
            self.delete(val)
            ret_list.append(val)
        return ret_list

    def __str__(self):
        node = self.first
        ret_str = ''
        while node:
            print(node)
            ret_str += str(node.value) + ' '
            node = node.next
        return ret_str

def insert_all(the_dlist, the_input_list):
  for element in the_input_list:
    the_dlist.insert(element)
        
if __name__ == '__main__':
    import sys
    process(sys.argv[1], sys.argv[2])
    a = Dlist()
    insert_all(a,[4,5,2,3,2,7])
    print(a.tolist())
