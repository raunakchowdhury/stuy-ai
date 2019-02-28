#! /usr/bin/python3

def OrdinaryComparison(a,b):
    if len(a) < len(b): return -1
    if len(a) == len(b): return 0
    return 1

def NumberComparison(a,b):
    if a < b: return -1
    if a == b: return 0
    return 1


class Pqueue:

    def __init__(self, comparator = OrdinaryComparison):
        self.list = [None]
        self.size = 0
        self.cmpfunc = comparator


    def push(self,data):
        '''
        Will push data into the queue.
        '''
        if self.size == len(self.list) - 1:
            self.list.append(data)
        else:
            # if the list has already been allocated
            if self.size == 0:
                self.list[1] = data
            else:
                self.list[self.size + 1] = data
        self.size += 1
        if self.size == 1:
            return
        # "bubble" the value up
        current_index = self.size
        if current_index % 2 == 0:
            parent_index = self.size // 2
        else:
            parent_index = (self.size - 1) // 2

        # keep swapping until the parent is less than the child
        while self.cmpfunc(self.list[parent_index], self.list[current_index]) == 1:
            self.list[parent_index], self.list[current_index] = self.list[current_index], self.list[parent_index]
            current_index = parent_index
            # alt exit condition for loop if the min is reached
            if current_index == 0:
                break

            if current_index % 2 == 0:
                parent_index = current_index // 2
            else:
                parent_index = (current_index - 1) // 2
            if parent_index == 0 or current_index == 1:
                break

    def pop(self):
        '''
        Will pop the minimum value off the queue.
        '''
        # swap front element with last element, then "pop" the last element
        if self.size != 1:
            self.list[1], self.list[self.size] = self.list[self.size], self.list[1]
        popped_element, self.list[self.size] = self.list[self.size], None
        self.size -= 1
        # if there is one element remaining
        if self.size == 1:
            return popped_element
        current_index = 1

        while current_index < self.size and self.list[2 * current_index] and self.list[2 * current_index + 1]:
            # checks if current element > either child node
            if self.cmpfunc(self.list[current_index], self.list[2 * current_index]) == 1 or self.cmpfunc(self.list[current_index], self.list[2 * current_index + 1]) == 1:
                comparison = self.cmpfunc(self.list[2 * current_index], self.list[2 * current_index + 1])
                # if left child > right child
                if comparison == 1:
                    self.list[current_index], self.list[2 * current_index + 1] = self.list[2 * current_index + 1], self.list[current_index]
                    current_index = 2 * current_index + 1
                # if left child = right child
                elif comparison == 0:
                    self.list[current_index], self.list[2 * current_index] = self.list[2 * current_index], self.list[current_index]
                    current_index = 2 * current_index
                # if left child < right child
                else:
                    self.list[current_index], self.list[2 * current_index] = self.list[2 * current_index], self.list[current_index]
                    current_index = 2 * current_index
            # print('current_index:', current_index, 'current value:', self.list[current_index], queue.list)

        # if one of the nodes don't exist
        if not self.list[2 * current_index + 1] and self.list[2 * current_index]:
            if self.cmpfunc(self.list[current_index], self.list[2 * current_index]) == 1:
                self.list[current_index], self.list[2 * current_index] = self.list[2 * current_index], self.list[current_index]
        elif not self.list[2 * current_index] and self.list[2 * current_index + 1]:
            if self.cmpfunc(self.list[current_index], self.list[2 * current_index + 1]) == 1:
                self.list[current_index], self.list[2 * current_index + 1] = self.list[2 * current_index + 1], self.list[current_index]
        return popped_element

    def peek(self):
        '''
        Will return the minimum item in the list.
        '''
        return self.list[1]

    def to_list(self):
        '''
        will pop() every element off the queue into a list (in order) that it returns.
        If the queue was empty, it returns an empty list.
        Once this function returns, the queue is empty.
        '''
        if len(self.list) == 0:
            return []
        size = self.size
        ordered_list = []
        for i in range(size):
            ordered_list.append(self.pop())
        return ordered_list


if __name__ == '__main__':
    queue = Pqueue(NumberComparison)
    print('Inserting into queue...')
    for num in range(1000,0,-1):
        queue.push(num)
        # print(queue.list)
    queue.push(1)
    print('Current list:', queue.list)
    print('Printing pop and queue after pop:', queue.pop(), queue.list)
    returned_list = queue.to_list()
    try:
        print('Checking if it\'s sorted...')
        assert sorted(returned_list) == returned_list
        print('It\'s sorted!\n')
    except:
        print('Oops, something went wrong with to_list()! Printing the list now:\n')
    print('Printing returned list:', returned_list)
    print('Printing to_list() again for giggles:', queue.to_list())
    print('Pushing again to test...')
    for num in range(100,0,-1):
        queue.push(num)
    print('Printing queue.list:', queue.list)
