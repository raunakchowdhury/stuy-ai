#! /usr/bin/python3

import time

cliques=[(0,1,2),\
(3,4,5),\
(6,7,8),\
(0,3,6),\
(1,4,7),\
(2,5,8),\
(0,4,8),\
(2,4,6),\
]

def is_win(board):
    """determines win"""
    for pos_1, pos_2, pos_3 in cliques:
        if board[pos_1] != '_':
            if board[pos_1] == board[pos_2] == board[pos_3]:
                return True, board[pos_1]
    return False, None

def next_position(board):
    """determines next pos of player"""
    # print(type(board))
    for i in range(len(board)):
        if board[i] == '_':
            return i
    return -1

def next_rel_position(board, cur_pos):
    """determines next pos of player"""
    # print(type(board))
    next_pos = cur_pos + 1
    while next_pos < len(board):
        if board[next_pos] == '_':
            # print(string_board(board), cur_pos+1, next_pos)
            return next_pos
        next_pos += 1
    return -1

def swap_players(player):
    """switch players"""
    if player == 'x':
        return 'o'
    return 'x'

# def play_game(board):
#     """plays game"""
def string_board(board):
    """stringifies the board."""
    index = 0
    returned_list = []
    while index < len(board):
        array = [str(x) for x in board[index:index+3]]
        returned_list.append(','.join(array))
        index += 3
    return '\n'.join(returned_list)

def tictactoe_recursive():
    board = ['_'] * 9
    cur_pos = 0
    game_ctr = 0
    cur_player = 'x'
    for i in range(9):
        if board[i] == '_':
            current_board = board[:]
            game_ctr += recursive_helper(current_board, i, 'x')
    return game_ctr

def recursive_helper(board, pos, player):
    """play one move per recursion"""
    game_ctr = 0
    board[pos] = player
    if is_win(board) or '_' not in board:
        # print(string_board(board), pos, player)
        return 1
    # expand all possibilities
    for i in range(9):
        if board[i] == '_':
            current_board = board[:]
            game_ctr += recursive_helper(current_board, i, swap_players(player))
    return game_ctr

def rotate(board, degrees):
    """rotate board by 90, 180, or 270 degrees"""
    old_board = board
    new_board = [None] * 9
    rotate_positions = [(2,0), (5,1), (8,2), (1,3), (4,4), (7,5), (0,6), (3,7), (6,8)]
    # print(string_board(board))
    if degrees == 0:
        return board
    # rotate however many times as needed
    for i in range(degrees // 90):
        for new_pos, old_pos in rotate_positions:
            new_board[new_pos] = old_board[old_pos]
        old_board = new_board[:]
    return new_board

def reflect(board):
    """reflects the board"""
    board[0],board[2] = board[2],board[0]
    board[3],board[5] = board[5],board[3]
    board[6],board[8] = board[8],board[6]
    return board

def find_families(boards):
    """finds all board families"""
    board_families = set()
    listified_board = []
    add_board = True
    for board in boards:
        listified_board = list(board)
        for degree in [0, 90, 180, 270]:
            if tuple(rotate(listified_board, degree)) in board_families or tuple(rotate(reflect(listified_board), degree)) in board_families:
                add_board = False
        if add_board:
            board_families.add(board)
        add_board = True
    # print(board_families)
    return len(board_families)

def tictactoe_game_tree():
    """Explores game tree of tic tac toe; uses a "recursive" approach"""
    board = ['_' for i in range(9)]
    ctrs = {'games': 0, 'x': 0, 'o': 0, 'draw': 0}
    intermediate_boards = set() # current state of board causes problems, will +1 later
    # intermediate_boards = [board]
    cur_player = 'x'
    stack = []

    for i in range(9):
        if board[i] == '_':
            current_board = board[:]
            stack.append((current_board, i, 'x'))

    # # for all 'x'
    while len(stack) != 0:
        board, cur_pos, cur_player = stack.pop(-1)
        board[cur_pos] = cur_player
        intermediate_boards.add(tuple(board))
        # intermediate_boards.append(board)
        win, player_won = is_win(board)
        if win or '_' not in board:
            ctrs['games'] += 1
            if win:
                ctrs[player_won] += 1
            else:
                ctrs['draw'] += 1
        else:
            # expand all possibilities
            for i in range(9):
                if board[i] == '_':
                    current_board = board[:]
                    stack.append((current_board, i, swap_players(cur_player)))
    # print(intermediate_boards)
    # for bord in intermediate_boards:
    #     print(string_board(bord))
    #     print()
    families = find_families(intermediate_boards)
    # intermediate_boards = set([tuple(board) for board in intermediate_boards])
    return ctrs['games'], ctrs['x'], ctrs['o'], ctrs['draw'], len(intermediate_boards) + 1, families + 1

if __name__ == '__main__':
    board = [\
        'x','o','x',\
        '_','x','o',\
        'x','_','_',\
    ]
    # print(string_board(board))
    # print()
    # for degree in [90, 180, 270]:
    #     print(string_board(rotate(board, degree)))
    #     print()
        # print(string_board(reflect(board)))
    game_ctr, x_wins, o_wins, draws, intermediate_boards, families = tictactoe_game_tree()
    print('Games (A): {}\nWins by x (B1): {}\
        \nWins by o (B2): {}\nDraws (B3): {}\
        \n# Intermediate boards (C): {}\
        \n# Board Families (D): {}'.format(game_ctr, x_wins, o_wins, draws, intermediate_boards, families))
    # print(tictactoe_recursive())
