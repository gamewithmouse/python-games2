import socket
import json
import threading

import generate_maze

import traceback

import logger

import random



serverlogger = logger.Logger()

import sys
from collections import Counter



import time

import math



sock = socket.socket()


clients = []

player_data = list()

MAZE_SIZE = 43

monster_costs = {
    "police" : 1000,
    "teleporter" : 1200
}

monster_count = 0

CELL_SIZE = 100

MAX_PLAYERS = 10

id_list = [False] * MAX_PLAYERS

maze = generate_maze.generate_maze(MAZE_SIZE, MAZE_SIZE)

MAZE_HALF = math.floor(MAZE_SIZE / 2)

sock.bind(("0.0.0.0", 22122))

def client_thread(conn, addr):
    global monster_count, player_data

    

    my_player_data = {}
    
    client_notmine = clients

    buffer = []

    
    
    

    

    for i, has in enumerate(id_list):
        if not has:
            myid = i
            id_list[i] = True
            break

    
    print(id_list)
    
    

    
    try:
        #
        send_json(conn, {"command" : "maze", "maze" : generate_maze.tostring(maze)})  
        print("abd")
        for data in player_data:
            data["command"] = "player"
            send_json(conn, data)
        
        my_player_data["id"] =  myid
        my_player_data["money"] = 0
        my_player_data["items"] = []

        player_data.append(my_player_data)
        send_json_not_me(conn, {"command" : "player", "id" : myid})
        send_json(conn, {"command" : "id", "data" : myid})
        while True:
            send_json(conn, {"command" : "money", "money" : my_player_data["money"]})
            recvdata = conn.recv(2048).decode()
            
            buffer.append(recvdata.split("~")[0])
            
            strdata = buffer[0]
            
            del buffer[0]

            
        

            # print(f"len_buffer - id : {myid}, value = {len(buffer)}")
            
            if strdata and strdata != "":
                # print(f"len_split - id : {myid}, value = {len(recvdata.split('~'))}")
                jsondata = json.loads(strdata)
                command = jsondata["command"]
                
                if command == "player_state":
                    # print(recvdata)
                    

                    my_player_data.update(jsondata)
                    
                    
                    
                    send_json_not_me(conn, jsondata)
                elif command == "monsterdirection" and myid == 0:
                    send_json_not_me(conn, jsondata)
                elif command == "addmoney":
                    my_player_data["money"] += jsondata["amount"]
                    
                    
                elif command == "spawn_monster":
                    if my_player_data["money"] >= monster_costs[jsondata["type"]]:
                        my_player_data["money"] -= monster_costs[jsondata["type"]]
                        jsondata["x"], jsondata["y"] = get_random_pos()
                        jsondata["id"] = monster_count
                        monster_count += 1
                        send_json_all(jsondata)
                elif command == "win":
                    send_json_not_me(conn, {"command" : "lose"})
                elif command == "bullet":
                    send_json_all({"command" : "bullet", "owner" : myid, "x" : my_player_data["x"], "y" : my_player_data["y"], "direction" : my_player_data["direction"]})
            # time.sleep(0.01)
            
            
    except Exception as e:
        print(traceback.format_exc())
    finally:
        print("client disconnected or error")
        conn.close()
        
        clients.remove(conn)
        id_list[myid] = False
        player_data.remove(my_player_data)
 
        

def send_json_not_me(conn, data : dict):
    send_not_me(conn, json.dumps(data))

def send_not_me(conn, data : str):
    for client in clients:
        if client != conn:
            senddata = data + "~"
            client.send(senddata.encode())

def send_json_all(data : dict):
    send_all(json.dumps(data))

def send_all( data : str):
    for client in clients:
        
        senddata = data + "~"
        client.send(senddata.encode())

def send_json(conn, data : dict):
    senddata = json.dumps(data) + "~"
    conn.send(senddata.encode())
def quit_event():
    while True:
        a = input()
        print("asdf")
        sock.close()
        sys.exit(1)

def get_random_pos():
    

    return (random.randint(2, MAZE_HALF) * 2 - 1) * CELL_SIZE, (random.randint(2, MAZE_HALF) * 2 - 1) * CELL_SIZE 


def run_server():
    threading.Thread(target=quit_event).start()
    serverlogger.info("server started")
    while True:
        sock.listen(10)
        
        conn, addr = sock.accept()

        serverlogger.info("new client connected")

        clients.append(conn)
            
        thread = threading.Thread(target=client_thread, args=(conn, addr,))
         # thread.setDaemon(True)
        thread.start()

        

run_server()