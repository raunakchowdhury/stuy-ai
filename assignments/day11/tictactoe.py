#! /usr/bin/python3


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
        self.parents = [] # all layouts that can lead to this one, by one move
        self.children = [] # all layouts that can be reached with a single move

    def print_me(self):
        print ('layout:',self.layout, 'endState:',self.endState)
        print ('parents:',self.parents)
        print ('children:',self.children)

def CreateAllBoards(layout,parent):
    # recursive function to manufacture all BoardNode nodes and place them into the AllBoards dictionary
    CreateAllBoardsHelper(layout, parent, 'x', None)

def CreateAllBoardsHelper(layout, parent, player, pos):
    """recursive helper"""
    board = [char for char in layout]
    if pos == None:
        node = BoardNode(layout)
        AllBoards[layout] = node
        for i in range(9):
            if board[i] == '_':
                CreateAllBoardsHelper(layout, node, player, i)
        return
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
    node.parents.append(parent.layout)

    win, player_won = is_win(board)
    if win or '_' not in board:
        if win:
            if player_won == 'x':
                node.endState = 'x'
            else:
                node.endState = 'o'
        else:
            node.endState = 'd'
        return
    # expand all possibilities
    for i in range(9):
        if board[i] == '_':
            CreateAllBoardsHelper(new_layout, node, swap_players(player), i)

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

def calc_stats():
    """Calculates stats for AllBoards"""
    results = { 'x': 0, 'o': 0, 'd': 0}
    intermediate_boards = 0
    child_boards = 0
    for node in AllBoards.values():
        if len(node.children) > 9:
            print(node.children)
        child_boards += len(node.children)
        if node.endState:
            results[node.endState] += 1
        else:
            intermediate_boards += 1
    return len(AllBoards), results['x'], results['o'], results['d'], intermediate_boards, child_boards

if __name__ == '__main__':
    CreateAllBoards('_________',None)
    # AllBoards['_'*9].print_me()
    print('# boards: {}\n# x wins: {}\
    \n# o wins: {}\n# draws: {}\
    \n# intermediate boards: {}\
    \n# children: {}'.format(*calc_stats()))
