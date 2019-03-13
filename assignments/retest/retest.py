#! usr/bin/python3

import sys

def process(infile, outfile):
    f = open(infile, 'r').read()
    lines = f.split('\n')
    insert_list = []
    # split on commas,  decide if you need to add the strings
    for line in lines: #forgot line was a str
        line = line.split(',')
        for element in line:
            if element == '':
                line.remove('')
        if len(line) > 1: #empty str
            insert_list.append(line)
    # sort the other values, concat lists, and add it
    insert_list = [','.join([line[0]] + sorted(line[1:])) for line in insert_list]
    # for index in range(len(insert_list)):
    #     temp = sorted(insert_list[index][1:])
    #     insert_list[index] = [insert_list[index][0]] + temp
    #     insert_list[index] = ','.join(insert_list[index])
    insert_list = '\n'.join(insert_list)
    g = open(outfile, 'w')
    g.write(insert_list)

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
        self.start_node = Node(None)

    def insert(self, value):
        # not so secretly written by Guido Van Rossum
        node = self.start_node
        prev_node = node
        # 1st node case
        if node.value == None:
            node.value = value
            return

        new_node = Node(value)
        while node:
            # print('Val: {}'.format(node.value))
            if node.value >= value:
                # print('triggered on {}'.format(value))
                if node.previous == None:
                    node.previous = new_node
                    new_node.next = node
                    self.start_node = new_node
                    return
                new_node.next = node
                new_node.previous = node.previous
                node.previous.next = new_node
                node.previous = new_node
                return
            prev_node = node
            node = node.next
        prev_node.next = new_node
        new_node.previous = prev_node
        print(self)
        # print('End', prev_node.value, new_node.value)
        # print(new_node.value)

    def delete(self, value):
        # you code to remove the first occurrence of
        # value in the list and return True, or return False if not found
        node = self.start_node
        while node:
            print(node.value)
            if value == node.value:
                # forgot first edge case where first is only node
                if node.previous == None and node.next == None:
                    node.value = None
                    return True
                # forgot case where the matching element is the first node
                elif node.previous == None:
                    self.start_node = node.next
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
        node = self.start_node
        ret_list = []
        while node:
            val = node.value
            node = node.next
            self.delete(val)
            ret_list.append(val)
        return ret_list

    def __str__(self):
        node = self.start_node
        ret_str = ''
        while node:
            ret_str += str(node.value) + ' '
            node = node.next
        return ret_str

if __name__ == '__main__':
    process(sys.argv[1], sys.argv[2])
    dlist = Dlist()
    for x in range(5,0,-1):
        # print(x)
        dlist.insert(x)
        print(dlist)
    dlist.insert(5)
    print(dlist)
    dlist.insert(7)
    print(dlist.tolist())
    print(dlist)
    dlist.insert(3)
    dlist.delete(3)
