import socket
import json
import time

sock = socket.socket()

sock.connect(("127.0.0.1", 22222))


dists = {"nickname" : "John"}


jsons = json.dumps(dists)
string = f"0x0103#{jsons}"

sock.sendall(string.encode())

def main():

    while True:
        dicts = {"nickname" : "John", "direction" : "right"}
        sendstr = "0x0101#" + json.dumps(dicts)
        sock.sendall(sendstr.encode())
        # print(sock.recv(1024).decode())
time.sleep(2)
main()
