#! /usr/bin/python3

import time

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
        elif line.find('name') == -1:
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
    if board[position] != '_':
        return []
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

def next_priority_position(board):
    """Finds the position with the lowest moves and returns that pos and its moves"""
    positions_and_moves = set()
    current_position = next_position(-1, board)
    while current_position != -1:
        moves = get_possible_moves(current_position, board)
        positions_and_moves.add((len(moves), tuple(moves), current_position))
        current_position = next_position(current_position, board)
    if not positions_and_moves:
        return -1, []
    min_pos_moves = min(positions_and_moves)
    return min_pos_moves[2], list(min_pos_moves[1])

def solve_obvious(board):
    """Plugs in the obvious solutions for the board until it can't find any more."""
    changed, board = solve_obvious_helper(board)
    while changed:
        changed, board = solve_obvious_helper(board)
    return board

def solve_obvious_helper(board):
    """solve_obvious helper"""
    position = next_position(-1, board)
    changed = False
    while position != -1:
        moves = get_possible_moves(position, board)
        # if there exists only one move, plug it in
        if len(moves) == 1:
            board[position] = moves[0]
            changed = True
        position = next_position(position, board)
    return changed, board

def clique_solve(board, pos):
    """
    Solves using the following heuristic: if one cell has vals 1,2, and 3 and two other cells have vals 1 and 2, the first cell must be 3
    Creds to Jonathan Singer
    """
    if pos == -1:
        return board
    changed, board = clique_solve_helper(board, pos)
    while changed:
        changed, board = clique_solve_helper(board, pos)
    return board

def clique_solve_helper(board, pos):
    changed = False
    cliques = indexed_cliques[pos]
    for clique in cliques:
        possible_positions = [[], [], [], [], [], [], [], [], [], []] #each index+1 is a possible number; nested lists store positions
        for position in clique:
            for move in get_possible_moves(position, board):
                possible_positions[move].append(position)
        for index in range(9):
            # if there's exaclty one possibility at each position, then that's it
            if possible_positions[index]:
                if len(possible_positions[index]) == 1:
                    board[possible_positions[index][0]] = index
                    changed = True
    return changed, board

def naive_sudoku(board):
    '''
    Solves a board using naive search.
    states are expressed as (current_position, current_board, possible_moves)
    '''
    stack = []
    current_position = next_position(-1, board)
    current_board = board
    num_backtracks = 0
    # stack.push(State(0, board, get_possible_moves(0, board)))

    while current_position != -1:
        moves = get_possible_moves(current_position, current_board)
        # if the board is no longer solvable
        if moves == []:
            state = stack.pop(-1)
            num_backtracks += 1
            # possibility that states could have empty possible_nums lists; account for that
            while len(state[2]) == 0:
                state = stack.pop(-1)
                num_backtracks += 1
            current_position = state[0]
            state[1][current_position] = state[2].pop(-1) #use last item on list
            current_board = state[1][:]
            stack.append(state)
        else:
            state = (current_position, current_board, moves)
            state[1][current_position] = state[2].pop(-1) #use last item on list
            current_board = state[1][:]
            stack.append(state)
        current_position = next_position(current_position, current_board)
    # if you get here, you done it
    return stack.pop(-1)[1], num_backtracks

def smarter_sudoku(board):
    '''
    Solves a board using smarter search.
    '''
    stack = []
    current_board = solve_obvious(board)
    current_position = next_position(-1, board)
    num_backtracks = 0
    # stack.push(State(0, board, get_possible_moves(0, board)))

    while current_position != -1:
        moves = get_possible_moves(current_position, current_board)
        # print(string_board(current_board), current_position, moves, '\n\n')
        # if the board is no longer solvable
        if moves == []:
            state = stack.pop(-1)
            num_backtracks += 1
            # possibility that states could have empty possible_nums lists; account for that
            while len(state[2]) == 0:
                state = stack.pop(-1)
                num_backtracks += 1
            current_position = state[0]
            state[1][current_position] = state[2].pop(-1) #use last item on list
            current_board = state[1][:]
            stack.append(state)
        else:
            state = (current_position, current_board, moves)
            state[1][current_position] = state[2].pop(-1) #use last item on list
            current_board = state[1][:]
            stack.append(state)
        current_board = solve_obvious(current_board)
        current_board = clique_solve(current_board, current_position)
        current_position = next_position(current_position, current_board)
    # if you get here, you done it
    if len(stack) == 0:
        return current_board, num_backtracks
    return current_board, num_backtracks

def smartest_sudoku(board):
    '''
    Solves a board using the smartest search.
    '''
    stack = []
    current_board = solve_obvious(board)
    current_position, moves = next_priority_position(board)
    # current_board = clique_solve(current_board, current_position)
    # print(string_board(current_board), current_position)
    num_backtracks = 0
    # stack.push(State(0, board, get_possible_moves(0, board)))

    while current_position != -1:
        # moves = get_possible_moves(current_position, current_board)
        # print(string_board(current_board), current_position, moves, '\n\n')
        # if the board is no longer solvable
        if moves == []:
            state = stack.pop(-1)
            num_backtracks += 1
            # possibility that states could have empty possible_nums lists; account for that
            while len(state[2]) == 0:
                state = stack.pop(-1)
                num_backtracks += 1
            current_position = state[0]
            state[1][current_position] = state[2].pop(-1) #use last item on list
            current_board = state[1][:]
            stack.append(state)
        else:
            state = (current_position, current_board, moves)
            state[1][current_position] = state[2].pop(-1) #use last item on list
            current_board = state[1][:]
            stack.append(state)
        current_board = solve_obvious(current_board)
        current_board = clique_solve(current_board, current_position)
        # current_board = solve_obvious(current_board)
        current_position, moves = next_priority_position(current_board)
    # if you get here, you done it
    if len(stack) == 0:
        return current_board, num_backtracks
    return current_board, num_backtracks

def string_board(board):
    '''
    stringifies the board.
    '''
    index = 0
    returned_list = []
    while index < len(board):
        array = [str(x) for x in board[index:index+9]]
        returned_list.append(','.join(array))
        index += 9
    return '\n'.join(returned_list)

def test_sudoku(sudoku, board, function_label):
    """Tests the given sudoku function against the board and prints the results."""
    print('{}\n{}'.format(board, string_board(games[board])))
    print()
    start_time = time.time()
    solved_board, num_backtracks = sudoku(games[board])
    elapsed_time = time.time() - start_time
    print('The algorithm backtracked {} times for {} using {}. Elapsed time: {}\n'.format(num_backtracks, board, function_label, '%.3f'% elapsed_time))
    print(string_board(solved_board))
    print()



if __name__ == '__main__':
    import sys
    if len(sys.argv) == 4:
        process(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        process(sys.argv[1], sys.argv[2])
        for sudoku in [(smartest_sudoku, 'smartest_sudoku')]: #(smarter_sudoku, 'smarter_sudoku'),
            for board in [ 'name,Easy-NYTimes,unsolved', 'name,Medium-NYTimes,unsolved', 'name,Hard-NYTimes,unsolved', 'name,hardest-sudoku-telegraph,unsolved', 'name,sudokugarden.de/files/100sudoku2-en.pdf-Nr-100,unsolved', 'name,sudokugarden.de/files/100sudoku2-en.pdf-Nr-50,unsolved']:
                test_sudoku(sudoku[0], board, sudoku[1])

    # print_board(games[9])
    # print_board(sudoku(games['A7-1,Hardest,unsolved']))
    # print(games['A1-2,Easy-NYTimes,solved'] == sudoku(games['A1-1,Easy-NYTimes,unsolved']))
    # solution = sudoku(games['A2-1,Medium-NYTimes,unsolved'])
    # print(games['A2-2,Medium-NYTimes,solved'] == solution)
    # # print_board(solution)
    # # print_board(games[3])
    # print(games['A3-2,Hard-NYTimes,solved'] == sudoku(games['A3-1,Hard-NYTimes,unsolved']))
