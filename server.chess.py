import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.bind("127.0.0.1",5000)
basic_board = [["r", "n", "b", "q", "k", "b", "n", "r"],
               ["p"]*8,
               ["g"]*8,
               ["g"]*8,
               ["g"]*8,
               ["g"]*8,
               ["P"]*8,
               ["R", "N", "B", "Q", "K", "B", "N", "R"]]
print(basic_board)
def client_socket():
    pass