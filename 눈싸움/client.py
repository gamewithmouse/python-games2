import pygame

import socket

import _asyncio

sock = socket.socket()

sock.connect(("127.0.0.1", 22222))



display = pygame.display.set_mode((1280, 720))

async def recive():
    return sock.recv(1024)

def rungame():
    while True:
        _asynciorecive()