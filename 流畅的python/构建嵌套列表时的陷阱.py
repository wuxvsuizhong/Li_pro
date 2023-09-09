board = [['_']*3 for i in range(3)]
print(board)        # [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
board[1][2] = '0'
print(board)        # [['_', '_', '_'], ['_', '_', '0'], ['_', '_', '_']]

weird_board = [['_']*3]*3
print(weird_board)  # [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
weird_board[1][2] = '0'
print(weird_board)  # [['_', '_', '0'], ['_', '_', '0'], ['_', '_', '0']


