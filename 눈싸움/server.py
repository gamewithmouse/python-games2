import socket

sock = socket.socket()


client_list = []

sock.bind(('127.0.0.1', 22222))

def sendAllClients(data):
    for client in client_list:
        client.send(data)

def clientthread(sock):
    while True:
        recivedata = sock.recv(1024).decode()
        command = recivedata.split("/")[0]
        data = recivedata.split("/")[1]

        if command == "Playerstate":
            sendAllClients(recivedata)
            




