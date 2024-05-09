import socket
import threading, uuid, logging, datetime


logger = logging.getLogger(__name__)
sock = socket.socket()

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        
sock.bind(("127.0.0.1",22222))
Player_list = {"123123123":Player(), "2222222" : Player()}
connlist = []
turn = 0
map_list = [
    ["street", "street_bottom_in","street_bottom_in","street_bottom_in","street_bottom_in","street_bottom_in","street_bottom_in","street_bottom_in","street_bottom_in","street_bottom_in","street_bottom_in","street_bottom_in","street_bottom_in","street_bottom_in","street_bottom_in",],

    ["street_right_in", "street","street","street","street","street","street","street","street","street","street","street","street","street","street",],
    ["street_right_in", "street","street","street","street","street","street","street","street","street","street","street","street","street","street",],
    ["street_right_in", "street","street","street","street","street","street","street","street","street","street","street","street","street","street",],
    ["street_right_in", "street","street","street","street","street","street","street","street","street","street","street","street","street","street",],
    ["street_right_in", "street","street","street","street","street","street","street","street","street","street","street","street","street","street",],
    ["street_right_in", "street","street","street","street","street","street","street","street","street","street","street","street","street","street",],
    ["street_right_in", "street","street","street","street","street","street","street","street","street","street","street","street","street","street",],
    ["street_right_in", "street","street","street","street","street","street","street","street","street","street","street","street","street","street",],
    ["street_right_in", "street","street","street","street","street","street","street","street","street","street","street","street","street","street",],
    ["street_right_in", "street","street","street","street","street","street","street","street","street","street","street","street","street","street",],
    ["street_right_in", "street","street","street","street","street","street","street","street","street","street","street","street","street","street",],
    ["street_right_in", "street","street","street","street","street","street","street","street","street","street","street","street","street","street",],

]
      

    
def run_server():
    print("Server Started")
        
    
    while True:
        sock.listen(5000)
        conn,addr = sock.accept()
        threading.Thread(target=Client, args=(conn,)).start()
        connlist.append(conn)
def should_send():
    while True:
        send(f"{{'map_list' : {map_list}}}", None)
def Client(conn):
    sending = ""
    while True:
        try:
            data = conn.recv(1024).decode()
            
            

            
            print(data)
            if data.find("pos") != -1:
                
                data = data.split("pos")
                addr = data[0]
                slist = data[1].split(",")
                print(slist)
                Player_list[str(addr)].x = slist[0]
                
                Player_list[str(addr)].y = slist[1]
                data = ""
            sending = "Player" + str(Player_list[str(addr)].x) + "," + str(Player_list[str(addr)].y)
            
            send(sending, conn)
        except ConnectionResetError:
            logging.info(f"[{datetime.datetime.today()}] [INFO] {addr} Disconnected {addr}'s Thread Will Be Stop")
            break
        
def send(data, connm):
    
    for conn in connlist:
        if conn != connm:
            conn.send(data.encode())
        
threading.Thread(run_server()).start()

