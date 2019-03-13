# CW for 2/28

def perm(perm_list):
    '''
    Generates all possible permuations of perm_list.
    '''
    returned_list = [perm_list]
    for first in range(len(perm_list)):
        second = first + 1
        while second < len(perm_list):
            perm_list[first], perm_list[second] = perm_list[second], perm_list[first]
            returned_list.append(perm_list)
            # switch back
            perm_list[first], perm_list[second] = perm_list[second], perm_list[first]
            second += 1
    return returned_list

if __name__ == '__main__':
    import sys
    file = '2019-02-11.md'
    if len(sys.argv) >= 2:
        file = sys.argv[1]
    f = open(file, 'r')
    g = open('smpl.md', 'w')
    lines = f.read().split('\n')
    for line in lines:
        g.write(line + '\n')
    f.close()
    g.close()
    # print(perm([0,1,2]))



# r/w csv files
# write methods for classes
# algorithms for wokring with a Pqueue in heap form
