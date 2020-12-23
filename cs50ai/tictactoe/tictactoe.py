"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    
    # Returns starting board
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    
    # Counts number of empty spaces
    counter = 0
    for row in board:
        counter += row.count(EMPTY)
        
    # Returns player's turn
    if counter % 2 == 1:
        return X
    return O
    

def actions(board):

    # Returns set of all possible actions (i, j) available on the board.
    moves = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                moves.add((i, j))
    return moves
            

def result(board, action):
    
    # Test if action is valid
    if board[action[0]][action[1]] != EMPTY:
        raise Exception('Not a valid move.')
    
    # Deepcopy board
    board_new = copy.deepcopy(board)
    
    # Fill in new value
    counter = 0
    for row in board:
        counter += row.count(EMPTY)
        
    # Change value
    if counter % 2 == 1:
        board_new[action[0]][action[1]] = X
        return board_new
    board_new[action[0]][action[1]] = O
    return board_new


def winner(board):
    
    # Check horizontal values
    for row in board:
        if row.count(X) == 3:
            return X
        if row.count(O) == 3:
            return O
    
    # Check vertical values
    for col in range(len(board)):
        if board[0][col] == X and board[1][col] == X and board[2][col] == X:
            return X
        if board[0][col] == O and board[1][col] == O and board[2][col] == O:
            return O
        
    # Check diagonal values
    if (board[0][0] == X and board[1][1] == X and board[2][2] == X) or \
        (board[2][0] == X and board[1][1] == X and board[0][2] == X):
        return X

    if (board[0][0] == O and board[1][1] == O and board[2][2] == O) or \
        (board[2][0] == O and board[1][1] == O and board[0][2] == O):
        return O


def terminal(board):
    
    # Terminate game if there is a winner
    if winner(board) != None:
        return True
    
    # Terminate game if there are no more moves to make
    if len(actions(board)) == 0:
        return True
    
    # Otherwise continue game
    return False


def utility(board):
    
    # Utility if X won
    if winner(board) == X:
        return 1
    
    # Utility if O won
    if winner(board) == O:
        return -1
    
    # Utility if draw
    else:
        return 0


def minimax(board):
    
    # No moves if terminal board
    if terminal(board):
        return None

    # Utility from initial moves
    i = 0
    utilities = []
    for action in actions(board):
        board_new = result(board, action)
        utilities.append(utility(board_new))
        
        # Utility from subsequent moves
        if terminal(board_new) == False:
            action_new = minimax(board_new)
            utilities[i] = utility(result(board_new, action_new))
        
        i += 1
    
    # Optimal move from utilities
    if player(board) == X:
        action_opt = list(actions(board))[utilities.index(max(utilities))]
    if player(board) == O:
        action_opt = list(actions(board))[utilities.index(min(utilities))]
    
    return action_opt
    
    

    
    
    
    
    
    
    

