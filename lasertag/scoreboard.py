board = {}
player_hits = []
def add_score(player_id, amount):
    global board
    if player_id not in board:
        board[player_id] = 0
    board[player_id] += amount
    print(board)

def add_player_hits(sender,hit,points):
    global player_hits
    player_hits.append((sender, hit, points))
    print(player_hits)