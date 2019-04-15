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
        if len(word) == len_word:
            data.add(word)
    return data

def get_neighbors(word, data):
    '''
    Finds the closest neighbors.
    '''
    global letters
    neighbors = []
    for index in range(len(word)):
        for letter in letters:
            if index == 0:
                new_word = letter + word[1:]
            elif index == len(word) - 1:
                new_word = word[:index] + letter
            else:
                new_word = word[0:index] + letter + word[index+1:]
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

def search(start, target, data):
    '''
    uses A* search to find the smallest sequence of steps to the target.
    returns a list of steps.
    '''
    explored = set()
    frontier = Pqueue(NumberComparison)
    frontier.push((num_transformations(start, target), start, [start]))
    # search ops; len(curr_path) - 1 is the traversal_cost
    while frontier.size != 0:
        current_node = frontier.pop()
        if current_node[1] == target:
            break
        elif current_node[1] not in explored:
            explored.add(current_node[1])
            neighbors = get_neighbors(current_node[1], data)
            for neighbor in neighbors:
                if neighbor not in explored:
                    curr_path = current_node[2][:]
                    curr_path.append(neighbor)
                    node = (num_transformations(neighbor, target) + len(curr_path) - 1, neighbor, curr_path)
                    frontier.push(node)
    if frontier.size == 0:
        return [start,target]
    return current_node[2]

def extended_search(start, target, data):
    '''
    uses a wack A* search to find the largest sequence of steps to the target.
    returns a list of steps.
    '''
    explored = set()
    frontier = Pqueue(NumberComparison)
    frontier.push((num_transformations(start, target), start, [start]))
    # search ops; len(curr_path) - 1 is the traversal_cost
    while frontier.size != 0:
        current_node = frontier.pop()
        if current_node[1] == target:
            break
        elif current_node[1] not in explored:
            explored.add(current_node[1])
            neighbors = get_neighbors(current_node[1], data)
            for neighbor in neighbors:
                if neighbor not in explored:
                    curr_path = current_node[2][:]
                    curr_path.append(neighbor)
                    node = ((len(curr_path) - 1) * -1 + num_transformations(neighbor, target) * -1, neighbor, curr_path)
                    # print(node[0])
                    frontier.push(node)
    if frontier.size == 0:
        return [start,target]
    print(len(current_node[2]))
    # verify all stings are unique
    check_set = set()
    for string in current_node[2]:
        if string not in check_set:
            check_set.add(string)
        else:
            raise ValueException('Not unique!')
    return current_node[2]


def process(infile, outfile, algorithm = search):
    '''
    Takes in a file of doublets and returns the path if possible.
    '''
    words = open(infile, 'r').read().splitlines()
    words = [word.split(',') for word in words]
    data = setup(len(words[0][0]))
    words = [algorithm(word[0], word[1], data) for word in words]
    write_str = ''
    for solved_list in words:
        # solved_list.append('\n')
        write_str += ','.join(solved_list) + '\n'
    writefile = open(outfile, 'w')
    writefile.write(write_str)

def search_for_longest_path(length):
    '''
    searches for longest path
    '''
    def inner_setup(len_word):
        '''
        Based on the # of characters given, returns a set of all the words with that # of characters in dictall.
        '''
        all_words = []
        words = open('dictall.txt', 'r').read().splitlines()
        data = set()
        for word in words:
            if len(word) == len_word:
                data.add(word)
                all_words.append(word)
        return data, all_words

    data, all_words = inner_setup(length)
    longest_path = 0
    for index in range(len(all_words)):
        for second_index in range(len(all_words)):
            curr_path = len(search(all_words[index], all_words[second_index], data))
            if curr_path > longest_path:
                print('New longest path!: {} for word pair {},{}'.format(curr_path, all_words[index], all_words[second_index]))
                longest_path = curr_path
    return longest_path

def vowel_consonant_ratio(word):
    '''
    returns vowel-consonant ratio of a word
    '''
    

if __name__ == '__main__':
    process(sys.argv[1], sys.argv[2], extended_search)
    # print(search_for_longest_path(4))
