#! /usr/bin/python3

import sys

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

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
        if self.size <= 1:
            return popped_element
        # print('size: {} {}'.format(self.size, self.list))
        current_index = 1

        while current_index < self.size and 2 * current_index < self.size and 2 * current_index + 1 < self.size:
            # print(current_index)
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
            else:
                break
            # print('current_index:', current_index, 'current value:', self.list[current_index])

        # print(self.list[current_index])
        # print(self.list)
        # if one of the nodes don't exist
        if not 2 * current_index + 1 < self.size and 2 * current_index < self.size:
            if self.cmpfunc(self.list[current_index], self.list[2 * current_index]) == 1:
                self.list[current_index], self.list[2 * current_index] = self.list[2 * current_index], self.list[current_index]
        elif not 2 * current_index < self.size and 2 * current_index + 1 < self.size:
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
        ordered_list = [self.pop() for i in range(size)]
        return ordered_list

    def internal_list(self):
        '''
        returns all valid elements of the list.
        '''
        return self.list[1:self.size+1]

    def push_all(self, push_list):
        '''
        pushes all elements into the queue.
        '''
        for element in push_list:
            self.push(element)


def setup(len_word):
    '''
    Based on the # of characters given, returns a set of all the words with that # of characters in dictall.
    '''
    words = open('dictall.txt', 'r').read().splitlines()
    data = set()
    for word in words:
        if len(word) == 4:
            data.add(word)
    return data

def get_neighbors(word, data):
    '''
    Finds the closest neighbors.
    '''
    global letters
    neighbors = []
    for index in range(4):
        for letter in letters:
            if index == 0:
                new_word = letter + word[1:]
            elif index == 1:
                new_word = word[0:1] + letter + word[2:]
            elif index == 2:
                new_word = word[0:2] + letter + word[3:]
            else:
                new_word = word[:3] + letter
            # print(new_word)
            if new_word in data and new_word != word:
                neighbors.append(new_word)
    return neighbors

def num_transformations(curr_word, target):
    '''
    Finds min # of characters from current word to target.
    '''
    different_chars = 0
    length = len(target)
    for index in range(length):
        if curr_word[index] != target[index]:
            different_chars += 1
    return different_chars

def search(start, target):
    '''
    uses A* search to find the smallest sequence of steps to the target.
    returns a list of steps.
    '''
    explored = set()
    frontier = Pqueue(NumberComparison)
    data = setup(len(target))
    # route = {}
    traversal_cost = 0
    # previous_node = (0 ,'START', [])

    frontier.push((num_transformations(start, target), start, [start]))

    while frontier.size != 0:
        current_node = frontier.pop()
        # print(current_node)
    # print(previous_node, current_node)
        traversal_cost += 1
    # print(current_node)
        if current_node[1] == target:
            # route[current_node[1]] = previous_node[1]
            break
        elif current_node[1] not in explored:
            explored.add(current_node[1])
            neighbors = get_neighbors(current_node[1], data)
            # route[current_node[1]] = previous_node[1]
            # previous_node = (current_node[0], current_node[1])
            # print(neighbors)
            for neighbor in neighbors:
                # print(neighbor, neighbor not in explored)
                if neighbor not in explored:
                    # print(current_node == previous_node)
                    curr_path = current_node[2][:]
                    # print(curr_path, current_node[2], '\n\n')
                    curr_path.append(neighbor)
                    node = (num_transformations(neighbor, target) + traversal_cost, neighbor, curr_path)
                    #print(node)
                    frontier.push(node)
    if frontier.size == 0:
        return [start,target]
    # post processing
    # print(frontier.list)
    # route_list = []
    # # print(route)
    # current_word = current_node[1]
    # while current_word != 'START':
    #     route_list.append(current_word)
    #     # print(current_word == route[current_word], current_word, route[current_word])
    #     current_word = route[current_word]
    #     # print(route)
    # route_list.reverse()
    # return route_list, len(route_list)
    return current_node[2]


if __name__ == '__main__':
    print(search('head','tail'))
    print(search('hazy','frog'))
    print(search('read', 'head'))
    print(search('head','ache'))
    # search('head','tail')
