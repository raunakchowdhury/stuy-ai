#! /usr/bin/python3

import sys

words = open('dictall.txt', 'r').read().split('\n')
words = words[:len(words)-1]

data = set()

for word in words:
    if len(word) == 4:
        data.add(word)

def process(infile, outfile):
    words = open(infile, 'r').read().split('\n')
    words = words[:len(words)-1]
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    ans_dict = {}
    for word in words:
        ans_dict[word] = []
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
                print(new_word)
                if new_word in data and new_word != word:
                    ans_dict[word].append(new_word)
    print(ans_dict['cake'])
    write_str = ''
    for key,value in ans_dict.items():
        write_str += key + ',' + str(len(value)) + '\n'
    print(write_str)
    g = open(outfile,'w')
    g.write(write_str)

if __name__ == '__main__':
    process(sys.argv[1], sys.argv[2])
