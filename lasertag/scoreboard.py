board = {}
player_hits = []
red_score = 0
green_score = 0
def add_score(player_id, amount):
    global board
    if player_id not in board:
        board[player_id] = 0
    board[player_id] += amount
    print(board)
    team_scores(board)

def add_player_hits(sender,hit,points):
    global player_hits
    player_hits.append((sender, hit, points))
    print(player_hits)

def team_scores(board):
    global green_score, red_score
    green_score = 0
    red_score = 0
    for id in board:
        if int(id) % 2 == 0:
            green_score += int(board[id])
        else:
            red_score += int(board[id])
