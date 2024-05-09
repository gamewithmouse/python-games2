import pygame
from easiersocket import Client
import json
import threading
import random

display = pygame.display.set_mode((1280, 720))

sock = Client("127.0.0.1", 22222)

name = str(random.randint(1, 100))
player_data = {
    "x" : 0,
    "y" : 0,
    "character" : 1,
    "level" : 1,
    "name" : name
}

x = 0
y = 0
map_surf = pygame.image.load("Cook_Real_map.png")
map_surf = pygame.transform.scale(map_surf,(2000, 2000))
class Button:
    def __init__(self, x, y, w, h, text, color, backcolor, bordercolor) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.color = color
        self.backcolor = backcolor
        self.bordercolor = bordercolor
    def draw(self):
        pygame.draw.rect(display, self.backcolor, (self.x, self.y, self.w, self.h), 10, 8)
        pygame.draw.rect(display, self.backcolor, (self.x+5, self.y+5, self.w-10, self.h-10))
        pygame.draw.rect(display, self.bordercolor, (self.x, self.y, self.w, self.h), 10, 8)
    def click(self, buttonnum):
        mouse = pygame.mouse.get_pressed(3)
        if mouse[buttonnum]:
            pos = pygame.mouse.get_pos()
            rect = pygame.Rect(self.x, self.y, self.w, self.h)
            if rect.collidepoint(pos):
                return True
        return False

def draw_map():
    display.blit(map_surf, (player_data["x"] * -1, player_data["y"] * -1))


def calculate_others(otherx, othery):
    relative_x = 0
    relative_y = 0
    if otherx < x + 640 and otherx > x - 640:
        if othery < y + 480 and othery > y - 480:
            relative_x = otherx - (x - 640)
            relative_y = othery - (y - 480)
    return (relative_y, relative_x)

def draw_others():
    while True:
        data = sock.recive()
        if data['Protocol'] == "Players":
            json_dict = json.loads(data["data"].split("|")[0])
            for key, value in json_dict.items():
                x = json_dict[key]["x"]
                y = json_dict[key]["y"]
                relativepos = calculate_others(x, y)
                pygame.draw.rect(display, (255, 255, 255), (relativepos[0], relativepos[1], 100, 100))



def rungame():
    threading.Thread(target=draw_others).start()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # sock.send("disconnect", name)
                pygame.quit()
        draw_map()
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            player_data["y"] -= 1
        if key[pygame.K_d]:
            player_data["x"] += 1
        if key[pygame.K_a]:
            player_data["x"] -= 1
        if key[pygame.K_s]:
            player_data["y"] += 1
        pygame.draw.rect(display, (255, 255, 255), (590, 430, 100, 100))
        pygame.display.update()
        sock.send("player_info", json.dumps(player_data) + "|")
# def infomation_me(): # 내 정보 확인 (레벨, 보유 식당, 일하는 식당, 일정 등)
#     selected_menu = "dashboard"
#     while True:
rungame()