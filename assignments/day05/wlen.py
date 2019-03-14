import sys

def wlen(filename):
    '''
    returns a list of the words seen.
    '''
    f, count = open(filename, 'r'), [0] * 25
    for word in f:
        count[len(word)-1] += 1
    return count

if __name__ == '__main__':
    print(wlen(sys.argv[1]))
