#! /usr/bin/python3

class Stack:
    def __init__(self):
        self.array = []

    def push(self, data):
        self.array.append(data)

    def pop(self):
        return self.array.pop(-1)

class State:
    def __init__(self, position=None, board=None, possible_nums=None):
        self.position = position
        self.board = board
        self.possible_nums = possible_nums

games = {}

def process(infile, outfile, board_to_solve = None):
    global games
    game = []
    current_game = ''
    f = open(infile, 'r')
    lines = f.read().split('\n')
    for line in lines:
        if line == '':
            games[current_game] = game
            game = []
        elif line.find('A') == -1:
            line = line.split(',')
            for element in line:
                if element != '_':
                    element = int(element)
                game.append(element)
        else:
            current_game = line
    if board_to_solve:
        if board_to_solve in games.keys():
            solved_board, num_backtracks = sudoku(games[board_to_solve])
            g = open(outfile, 'w')
            g.write(string_board(solved_board))
        else:
            raise Exception('Invalid board!')

cliques=[[0,1,2,3,4,5,6,7,8],\
[9,10,11,12,13,14,15,16,17],\
[18,19,20,21,22,23,24,25,26],\
[27,28,29,30,31,32,33,34,35],\
[36,37,38,39,40,41,42,43,44],\
[45,46,47,48,49,50,51,52,53],\
[54,55,56,57,58,59,60,61,62],\
[63,64,65,66,67,68,69,70,71],\
[72,73,74,75,76,77,78,79,80],\
[0,9,18,27,36,45,54,63,72],\
[1,10,19,28,37,46,55,64,73],\
[2,11,20,29,38,47,56,65,74],\
[3,12,21,30,39,48,57,66,75],\
[4,13,22,31,40,49,58,67,76],\
[5,14,23,32,41,50,59,68,77],\
[6,15,24,33,42,51,60,69,78],\
[7,16,25,34,43,52,61,70,79],\
[8,17,26,35,44,53,62,71,80],\
[0,1,2,9,10,11,18,19,20],\
[3,4,5,12,13,14,21,22,23],\
[6,7,8,15,16,17,24,25,26],\
[27,28,29,36,37,38,45,46,47],\
[30,31,32,39,40,41,48,49,50],\
[33,34,35,42,43,44,51,52,53],\
[54,55,56,63,64,65,72,73,74],\
[57,58,59,66,67,68,75,76,77],\
[60,61,62,69,70,71,78,79,80]\
]

indexed_cliques = {num:[] for num in range(81)}
for num in range(81):
    for clique in cliques:
        if num in clique:
            indexed_cliques[num].append(clique)

# print( games)

def get_possible_moves(position, board):
    '''
    Gives all possible numbers that a position could be.
    '''
    possible_numbers = set([1,2,3,4,5,6,7,8,9])
    cliques = indexed_cliques[position] #subset of cliques with the position in them
    # check rows
    for clique in cliques:
        for element in clique:
            if board[element] != '_' and board[element] in possible_numbers:
                # print('ele: {} at pos {}'.format(board[element],element))
                possible_numbers.remove(board[element])
    possible_numbers = list(possible_numbers)
    possible_numbers.reverse()
    return possible_numbers


def is_valid(position, board, number):
    '''
    Checks if every number is valid.
    '''
    for clique in cliques:
        if position in clique:
            for element in clique:
                if board[element] == number:
                    return False
    return True

def next_position(position, board):
    '''
    finds the next open slot and returns the index.
    if no open positions, return -1.
    '''
    current_index = position + 1
    while current_index < len(board):
        if board[current_index] == '_':
            # print(current_index)
            return current_index
        current_index += 1
    return -1

def sudoku(board):
    '''
    Solves a board using naive search.
    '''
    stack = Stack()
    current_position = next_position(-1, board)
    current_board = board
    num_backtracks = 0
    # stack.push(State(0, board, get_possible_moves(0, board)))

    while current_position != -1:
        moves = get_possible_moves(current_position, current_board)
        # if the board is no longer solvable
        if moves == []:
            state = stack.pop()
            num_backtracks += 1
            # possibility that states could have empty possible_nums lists; account for that
            while len(state.possible_nums) == 0:
                state = stack.pop()
                num_backtracks += 1
            current_position = state.position
            state.board[current_position] = state.possible_nums.pop(-1) #use last item on list
            current_board = state.board[:]
            stack.push(state)
        else:
            state = State(current_position, current_board, moves)
            state.board[current_position] = state.possible_nums.pop(-1) #use last item on list
            current_board = state.board[:]
            stack.push(state)
        current_position = next_position(current_position, current_board)
    # if you get here, you done it
    return stack.pop().board, num_backtracks

def string_board(board):
    '''
    stringifies the board.
    '''
    index = 0
    returned_list = []
    while index < len(board):
        returned_list.append(','.join([str(x) for x in board[index:index+9]]))
        index += 9
    return '\n'.join(returned_list)

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 4:
        process(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        process(sys.argv[1], sys.argv[2])
        for board in ['A1-1,Easy-NYTimes,unsolved', 'A2-1,Medium-NYTimes,unsolved', 'A3-1,Hard-NYTimes,unsolved']:
            solved_board, num_backtracks = sudoku(games[board])
            print('The algorithm backtracked {} times for {}.\n'.format(num_backtracks, board))

    # print_board(games[9])
    # print_board(sudoku(games['A7-1,Hardest,unsolved']))
    # print(games['A1-2,Easy-NYTimes,solved'] == sudoku(games['A1-1,Easy-NYTimes,unsolved']))
    # solution = sudoku(games['A2-1,Medium-NYTimes,unsolved'])
    # print(games['A2-2,Medium-NYTimes,solved'] == solution)
    # # print_board(solution)
    # # print_board(games[3])
    # print(games['A3-2,Hard-NYTimes,solved'] == sudoku(games['A3-1,Hard-NYTimes,unsolved']))
