from easiersocket import Server
import random
import json

app = Server("127.0.0.1", 21231)

player_name = []


def makeboard():
    list1 = [[]] * 10
    return [list1] * 10

board = makeboard()

ladders = []

turn = 1

def new_connect(data):
    player_name.append(data)
    app.send("player_id", str(len(player_name) + 1))
    board[0][9] = []
    board[0][9].append(data)
    app.send("board", str(board))

ladders = [
    [(0, 2), (0, 0)],
    [(4, 9), (3, 6)],
    [(6, 4), (5, 3)],
    [(7, 0), (5, 1)],
    [(7, 7), (1, 3)],
    [(0, 9), (6, 2)],
    [(3, 9), (6, 8)],
    [(8, 9), (5, 9)]
]

snakes = [
    [(2, 0), (2, 2)],
    [(5, 0), (5, 2)],
    [(7, 0), (7, 2)],
    [(1, 3), (1, 8)],
    [(3, 3), (0, 4)],
    [(4, 4), (4, 7)],
    [(6, 5), (5, 7)],
    [(8, 5), (9, 8)],
    [(8, 4), (9, 5)]

]


def roll_dice(data):
    global turn
    result = random.randint(1, 6)
    print("Rolling dice")
    for y, list1 in enumerate(board):
        for x, lists in enumerate(list1):
            if lists == data:
                mx, my = calculate_move(x, y, result)
                mx2, my2 = checkforboardevent(mx, my)
                board[y].pop(x)
                board[my2][mx2].append(data)

                app.send("move", json.dumps({"player" : data, "pos" : (mx2, my2)}))
    
    turn += 1
    if len(player_name) - 1 < turn:
        turn = 1
    app.send("turn", str(turn))
def checkforboardevent(x, y):
    rx = x
    ry = y
    for ladder in ladders:
        if ladder[0] == (x, y):
            rx = ladder[1][0]
            ry = ladder[1][1]
    for snake in snakes:
        if snake[0] == (x, y):
            rx = snake[1][0]
            ry = snake[1][0]
    return rx, ry
def calculate_move(x, y, dice):
    rx = x
    ry = y
    for space in range(dice):
        if rx == 9:
            ry -= 1
            rx = 0
        else:

            rx += 1

    return rx, ry



app.add_protocol("new_connect", new_connect)
app.add_protocol("rolldice", roll_dice)

app.run()

