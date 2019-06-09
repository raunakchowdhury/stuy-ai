#! /usr/bin/python3

import random
import sys


''' Layout positions:
0 1 2
3 4 5
6 7 8
'''
# layouts look like "_x_ox__o_"

Wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

AllBoards = {} # this is a dictionary with key = a layout, and value = its corresponding BoardNode

class BoardNode:
    def __init__(self,layout):
        self.layout = layout
        self.endState = None # if this is a terminal board, endState == 'x' or 'o' for wins, of 'd' for draw, else None
        self.children = [] # all layouts that can be reached with a single move
        self.best_move = -1  # cell position (0-8) of the best move from this layout, or -1 if this is a final layout
        self.moves_to_end = 0 # how many moves until the end of the game, if played perfectly.  0 if this is a final layout
        self.final_state = None  # expected final state ('x' if 'x' wins, 'o' if 'o' wins, else 'd' for a draw)

    def print_me(self):
        print ('layout:',self.layout, 'endState:',self.endState)
        print ('children:',self.children)

def CreateAllBoards(layout):
    """
    Generates the game tree up to the given layout.
    Maintains invariate that 'x' is the first player.
    """
    # string sanitization
    if len(layout) != 9:
        raise BaseException('Not correct length! Input had a length of {}'.format(len(layout)))
    # recursive function to manufacture all BoardNode nodes and place them into the AllBoards dictionary
    player = 'x'

    # hardcode the first move because processing takes too long
    # generate the rest of the boards based on that first move
    if layout == '_' * 9:
        pos = random.choice([0,2,4,6,8])
        current_layout = layout[0:pos] + 'x' + layout[pos+1:]
        node = BoardNode(layout)
        AllBoards[layout] = node
        node.children.append(current_layout)
    else:
        current_layout = layout[:]

    # determine who goes first initially
    num_o_played = current_layout.count('o')
    num_x_played = current_layout.count('x')
    if num_o_played + 1 == num_x_played: # if 'o' needs to move next
        player = 'o'
    # print("Player's move:", player)
    CreateAllBoardsHelper(current_layout, None, player, None)

def CreateAllBoardsHelper(layout, parent, player, pos):
    """recursive helper"""
    board = [char for char in layout]
    if pos == None:
        node = BoardNode(layout)
        AllBoards[layout] = node
        # check if a winning board was put in
        if is_win(board)[0] or '_' not in board:
            return
        for i in range(9):
            if board[i] == '_':
                CreateAllBoardsHelper(layout, node, player, i)
    else:
        board[pos] = player
        new_layout = ''.join(board)
        node = None
        if new_layout in AllBoards:
            node = AllBoards[new_layout]
        else:
            node = BoardNode(new_layout)
            AllBoards[new_layout] = node
        if new_layout not in parent.children:
            parent.children.append(new_layout)
        win, player_won = is_win(board)
        if win or '_' not in board:
            if win:
                if player_won == 'x':
                    node.endState = 'x'
                    node.final_state = 'x'
                else:
                    node.endState = 'o'
                    node.final_state = 'o'
            else:
                node.endState = 'd'
                node.final_state = 'd'
            return
        # expand all possibilities
        # else:
        for i in range(9):
            if board[i] == '_':
                CreateAllBoardsHelper(new_layout, node, swap_players(player), i)

    # only choose the nodes with the characteristics that you want
    # only wins if possible, then
    # only draws if possible, then
    # only losses if possible
    win_list = list(filter(lambda child: AllBoards[child].final_state == player, node.children))
    # if node.layout == sys.argv[1]:
    #     print(win_list)
    # print(player, win_list, node.children)
    draws_list = list(filter(lambda child: AllBoards[child].final_state == 'd', node.children))

    # print(chosen_node_list, node.layout)
    final_state_chosen = player
    # if wins exist, get the smallest # of moves possible
    if len(win_list) != 0:
        min_moves = min([AllBoards[child].moves_to_end for child in win_list])
        win_list = list(filter(lambda child: AllBoards[child].moves_to_end == min_moves, win_list))
        chosen_layout = random.choice(win_list)
        node.best_move = find_spot(layout, chosen_layout)
        node.final_state = AllBoards[chosen_layout].final_state
        node.moves_to_end = AllBoards[chosen_layout].moves_to_end + 1

    # if draws exist
    elif len(draws_list) != 0:
        if node.layout == sys.argv[1]:
            print([(AllBoards[child].final_state, AllBoards[child].layout) for child in draws_list])
        # chosen_node_list = list(filter(lambda child: AllBoards[child].final_state == 'd' or AllBoards[child].final_state == swap_players(original_player), node.children))
        final_state_chosen = 'd'
        chosen_layout = random.choice(draws_list)
        node.best_move = find_spot(layout, chosen_layout)
        node.final_state = AllBoards[chosen_layout].final_state
        node.moves_to_end = AllBoards[chosen_layout].moves_to_end + 1
        # print(chosen_layout, AllBoards[chosen_layout].moves_to_end, node.moves_to_end )

    else:
        # only losses exist
        loss_list = node.children
        final_state_chosen = swap_players(player)
        max_moves = max([AllBoards[child].moves_to_end for child in node.children])
        # filter down to a list with just children with the max # of moves
        loss_list = list(filter(lambda child: AllBoards[child].moves_to_end == max_moves, node.children))
        chosen_layout = random.choice(loss_list)
        node.best_move = find_spot(layout, chosen_layout)
        node.final_state = AllBoards[chosen_layout].final_state
        node.moves_to_end = AllBoards[chosen_layout].moves_to_end + 1


def find_spot(board, second_board):
    """find the move to take from the first board to the second. Returns index."""
    for char in range(len(board)):
        if board[char] != second_board[char]:
            return char
    return -1

def is_win(board):
    """determines win"""
    for pos_1, pos_2, pos_3 in Wins:
        if board[pos_1] != '_':
            if board[pos_1] == board[pos_2] == board[pos_3]:
                return True, board[pos_1]
    return False, None

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

def process(layout):
    """Prints out calculations based on what was given."""
    ret_str = ''
    board_node = AllBoards[layout]
    # final post-processing for an empty layout
    if layout == '_' * 9:
        child = AllBoards[board_node.children[0]]
        board_node.final_state = child.final_state
        board_node.moves_to_end = child.moves_to_end + 1
        board_node.best_move = find_spot(layout, child.layout)

    if board_node.best_move == -1:
        return 'Board already in win or draw state!\n'
    direction = ['upper-left', 'upper-center', 'upper-right',\
     'center-left', 'center-center', 'center-right',\
     'bottom-left', 'bottom-center', 'bottom-right']
    ret_str += 'move={}'.format(board_node.best_move) + '\n'
    ret_str += 'best move is {}'.format(direction[board_node.best_move]) + '\n'
    if board_node.final_state == 'd':
        ret_str += 'Draw in {} moves'.format(board_node.moves_to_end) + '\n'
        return ret_str
    ret_str += '{} wins in {} moves'.format(board_node.final_state, board_node.moves_to_end) + '\n'
    return ret_str

if __name__ == '__main__':
    result_str = '' # contains the string that will be the final output of the program
    arg_dict = {} # contains all the args given by CLI
    for arg in sys.argv[1:]:
        arg = arg.split('=')
        arg_dict[arg[0]] = arg[1]
    # if result prefix is given
    if 'result_prefix' in arg_dict:
        result_str += arg_dict['result_prefix'] + '\n'
    # if board is given
    if 'board' in arg_dict:
        CreateAllBoards(arg_dict['board'])
        result_str += process(arg_dict['board'])
    elif 'id' in arg_dict:
        result_str += "author=Raunak\ntitle=raunak's AI\n"

    # now append or print
    if 'result_file' in arg_dict:
        f = open(arg_dict['result_file'], 'w')
        f.write(result_str)
        f.close()
    else:
        print(result_str)
