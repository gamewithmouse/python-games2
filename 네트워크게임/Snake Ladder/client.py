from easiersocket import Client

import threading
import random
import json

app = Client("127.0.0.1", 21231)

board = [[True] * 10] * 10


name = str(random.randint(0, 10))

app.send("new_connect", name)


data = None

def rec():
    while True:
        data = app.recive()

threading.Thread(target=rec).start()

def moveplayer(player, tx, ty):
    for x, list1 in enumerate(board):
        for y, list2 in enumerate(list1):
            if list2 == player:
                board[y][x] = True
                board[ty][tx] = player

while True:
    print(board)
    input("주사위를 굴리시겠습니까?")
    app.send("rolldice", name)
    if data:
        if data["protocol"] == "move":
            print("Move Protocol")
            datas = json.loads(data["data"])
            player = datas["player"]
            moveplayer(player, data["pos"][0], data["pos"][1])
        if data["protocol"] == "board":
            board = list(eval(data["data"]))

