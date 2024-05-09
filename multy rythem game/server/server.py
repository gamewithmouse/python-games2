import socket
import logger
import debugger
import sys
import roommanager

import threading


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


logger = logger.Logger()

server_config = {
    "max_client" : 200
}


server_info = {
    "client_count": 0,
    "client_ips" : [],
    "rooms" : [],
    
}





def debug_server():
    try:
        while True:
            input()
            action = debugger.ask_action()
            if action == "stop server":
                logger.info("Stopping server..")
                logger.info("Closing socket..")
                sock.close()
                logger.info("Successfully closed socket")
                logger.info("Successfully stopped server")
                sys.exit()
            if action == "get all of the server info":
                print(str(server_info)) 
            if action == "get one key of the server info":
                debugger.get_key_of_server_info(server_info)    
    except Exception as e:
        logger.error("Error on Debugging. Restarting debugger. message : " + str(e))
        debug_thread = threading.Thread(target=debug_server, args=())
        debug_thread.start()






def start_server():
    logger.info("Starting server..")
    success = False
    try:
        sock.bind(("0.0.0.0", 22222))
        

        
    except Exception as e:
        logger.error("Error on starting server | " + str(e))
    run_server()
def run_server():
    global sock
    debug_thread = threading.Thread(target=debug_server, args=())
    debug_thread.start()
    
    print("asdf")
    while True:
        logger.info("Wating for client")
        sock.listen(server_config["max_client"])
        conn, addr = sock.accept()
        server_info["client_count"] += 1
        logger.info(f"new Client connected Info [{str(addr)}]")
        server_info["client_ips"].append(addr)
        threading.Thread(target=handle_client_recv, args=(conn, addr,)).start()

def handle_client_recv(conn, addr):
    info, code = roommanager.make_new_room("asdfasdf")
    print(info, code)
    
    while True:
        recivedata = conn.recv(8192).decode()
        if recivedata.find("/") != -1:
            commanddata = recivedata.split("/")
            command = commanddata[0]
            data = commanddata[1]

            
            



start_server()



