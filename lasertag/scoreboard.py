board = {}

def add_score(player_id, amount):
    global board
    if player_id not in board:
        board[player_id] = 0
    board[player_id] += amount
    print(board)