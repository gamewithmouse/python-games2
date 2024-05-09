import random


class Packet:
    def __init__(self, socket, data) -> None:
        self.socket = socket
        self.data = data



class Room:

    rooms = {}
    def __init__(self, code, name):
        self.clients = []
        self.code = code
        self.name = name
        self.gamestarted = False
        self.leader = None
        self.packet_buffer = []
        self.running = True
        self.first_join = False
        self.
    @staticmethod
    def make_new_room(name):
        roomcode = random.randint(0, 4194304)
        room = Room(roomcode, name)
        Room.rooms[roomcode] = room
        return room
    
    def join(self, socket):
        self.clients.append(socket)
    @staticmethod
    def join_room(client, roomcode=0):
        target_room = Room.rooms[roomcode]
        if target_room:
            target_room.join(client)
        return target_room    

    def recive_packet():


    # def update_state(self, packet=None):
    #     pass

    # def run_room(self):
    #     while self.running:
    #         self.update_state()
    # def recive_packet(self):
    #     while True:
    #         for client in self.clients:
    #             self.packet_buffer.append(Packet(client, client.recv(1024).decode()))


        