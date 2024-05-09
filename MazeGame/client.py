import generate_maze

import pygame
import os

import socket
import math

 
import time

import random

import json
import threading

from resources.pygame_util import HealthBar

pygame.init()

displaywidth = 1280
displayheight = 720

display = pygame.display.set_mode((displaywidth, displayheight))

maze = None

sock = socket.socket()


clients = []

sock.connect(("222.110.36.204", 22122))

images = {}

PLAYER_SIZE = 70


PRISON_INTEVAL = 10
CELL_SIZE = 100

MAZE_SIZE = 41

MAZE_QUARTER = math.floor(MAZE_SIZE / 4)
MAZE_HALF = math.floor(MAZE_SIZE / 2)

BULLET_WIDTH = 20
BULLET_HEIGHT = 10
BULLET_SPEED = 10

MONSTER_SIZE = 90

transform_images = {
    "playbutton.png" : (200, 80),
    "smartphone_menu.png" : (80, 80),
    "smartphone.png" : (320, 480),
    "person_back.png": (PLAYER_SIZE, PLAYER_SIZE),
    "person_back2.png": (PLAYER_SIZE, PLAYER_SIZE),
    "person_right.png": (PLAYER_SIZE, PLAYER_SIZE),
    "person_right2.png": (PLAYER_SIZE, PLAYER_SIZE),
    "person_left.png": (PLAYER_SIZE, PLAYER_SIZE),
    "person_left2.png": (PLAYER_SIZE, PLAYER_SIZE),
    "person_front.png": (PLAYER_SIZE, PLAYER_SIZE),
    "person_front2.png": (PLAYER_SIZE, PLAYER_SIZE),
    "wall.png" : (CELL_SIZE, CELL_SIZE),
    "bullet.png" : (BULLET_WIDTH, BULLET_HEIGHT),
    "police.png" : (MONSTER_SIZE, MONSTER_SIZE),
    "prison.png" : (1024, 1024),
    "money.png" : (CELL_SIZE, CELL_SIZE),
    "moneypanel.png" : (256, 96),
    "select_background.png" : (displaywidth, displayheight),
    "teleporter.png" : (MONSTER_SIZE, MONSTER_SIZE)

}

basicfont_one = pygame.font.Font("./resources/fonts/one.ttf", 40)

buffer = []




PLAYER_SPEED = 10


PLAYER_X = displaywidth / 2 - PLAYER_SIZE / 2
PLAYER_Y = displayheight / 2 - PLAYER_SIZE / 2

BULLET_DAMAGE = 10

myid = -1


FPS = 80






clock = pygame.time.Clock()


class GameObject:
    def __init__(self, x, y, image : pygame.Surface, collidable=False, drawable=True, width=0, height=0):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.image = image
        self.collidable = collidable
        self.drawable = drawable
        if self.drawable:
            self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())
        else:
            self.rect = pygame.Rect(x, y, self.w, self.h)
    def update(self):
        if self.drawable:
            self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        else:
            self.rect = pygame.Rect(self.x, self.y, self.w, self.h)


class Button:
    def __init__(self, x, y, w, h, image=None, text=None, color=(50, 50, 50, 0), font = None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.image = image
        self.text = text
        self.font = font
        self.rect = pygame.Rect(x, y, w, h)
        assert image == None or text == None, "Image and text shouldn't None"
    
    def draw(self):
        if self.image == None:
            
            showtextscreencenter(self.rect.center, self.text, self.color, self.font)
        else:
            display.blit(self.image, self.rect)

    def click(self, event):
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if self.rect.collidepoint(event.pos):
                return True
            
        return False

class Player:

    def __init__(self) -> None:

        self.max_health = 100

        self.prison_time = "none"

        

        self.health = self.max_health

        self.healthbar = HealthBar(self.max_health, 300, 70)
        
        self.x = 100
        self.y = 1000
        self.istwo = False  
        self.pressed_key = "None"
        self.direction = "front"
        self.place = "Deajon"
        
        
        self.speed = PLAYER_SPEED
        self.objects = []
        
        self.drawable = True
        self.rect = pygame.Rect(self.x + PLAYER_X + PLAYER_SPEED,
                                self.y + PLAYER_Y + PLAYER_SPEED,
                                PLAYER_SIZE - PLAYER_SPEED * 2, 
                                 PLAYER_SIZE - PLAYER_SPEED * 2
                                )
        

    def draw(self):
        if self.drawable:
            
            image = f"person_{self.direction}.png"
            display.blit(images[image], (PLAYER_X, PLAYER_Y))

    def damage(self, amount):
        print(amount)
        health = self.health
        if health - amount >= 0:
            self.health -= amount
        else:
            self.die()
    
    def die(self):
        self.random_teleport()
        self.health = 100
        send_json({"command" : "die"})
    def random_teleport(self):
        
        
        rx = random.randint(0, 1)
        ry = random.randint(0, 1)
        
        self.x, self.y = get_random_pos_of_quarter(rx, ry)

        
        
            
            

    def update_object(self):
        for targetobject in self.objects:
            
                    
                   
             
            # draw objects
            if targetobject.drawable == True:
                display.blit(targetobject.image, (targetobject.x - self.x, targetobject.y - self.y))
            # update objects
            targetobject.update()

    def add_object(self, gameobject : GameObject):
        self.objects.append(gameobject)

    def move(self):
        if self.pressed_key == "d":
            
            newrect = self.rect
            newrect.x += self.speed
            if all((targetobject.collidable == True and not targetobject.rect.colliderect(newrect)) or targetobject.collidable == False for targetobject in self.objects):
                
                self.x += self.speed
        if self.pressed_key == "w":
            newrect = self.rect
            newrect.y -= self.speed
            if all((targetobject.collidable == True and not targetobject.rect.colliderect(newrect)) or targetobject.collidable == False for targetobject in self.objects):
                
        
                self.y -= self.speed
        if self.pressed_key == "s":
            newrect = self.rect
            newrect.y += self.speed
            if all((targetobject.collidable == True and not targetobject.rect.colliderect(newrect)) or targetobject.collidable == False for targetobject in self.objects):
                self.y += self.speed
        if self.pressed_key == "a":
            newrect = self.rect
            newrect.x -= self.speed
            if all((targetobject.collidable == True and not targetobject.rect.colliderect(newrect)) or targetobject.collidable == False for targetobject in self.objects):
                self.x -= self.speed
        
        # print(self.x, ",", self.y)    
    def setDirection(self, event):
        
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_d , pygame.K_RIGHT]:
                self.pressed_key = "d"
                self.direction = "right"
            if event.key in [pygame.K_w, pygame.K_UP]:
                self.pressed_key = "w"
                self.direction = "back"    
            if event.key in [pygame.K_s, pygame.K_DOWN]:
                self.pressed_key = "s"
                self.direction = "front"    
            if event.key in [pygame.K_a, pygame.K_LEFT]:
                self.pressed_key = "a"
                self.direction = "left"    
        # print(self.pressed_key)        
        if event.type == pygame.KEYUP:
            # print("Keyup")
            self.pressed_key = "none"
    def update(self):
        if self.prison_time != "none" and self.prison_time + PRISON_INTEVAL <= time.time():
            self.prison_time = "none"
            self.random_teleport()
        
        
        self.rect = pygame.Rect(self.x + PLAYER_X + PLAYER_SPEED,
                                self.y + PLAYER_Y + PLAYER_SPEED,
                                PLAYER_SIZE - PLAYER_SPEED * 2, 
                                 PLAYER_SIZE - PLAYER_SPEED * 2
                                )
        if self.health <= 0:
            self.die()
        self.healthbar.health = self.health
        self.move()
        self.update_object()
        self.healthbar.update()
        display.blit(self.healthbar.get_surface(), (50, 50))
    def getState(self):
        return {
            "command" : "player_state",
            "x" : self.x,
            "y" : self.y,
            "direction" : self.direction
        }
    

class OtherPlayer(GameObject):
    players = {}
    def __init__(self, myid):
        self.id = myid
        print(self.id)
        OtherPlayer.players[self.id] = self
        self.direction = "right"
        
        super().__init__(100, 1000, images["person_right2.png"], False)
    def update(self):
        super().update()
        self.image = images[f"person_{self.direction}.png"]

class MazeEnd(GameObject):
    def __init__(self, x, y, player : Player):
        self.player = player
        
        super().__init__(x, y, None, False, False, CELL_SIZE, CELL_SIZE)
    
    def update(self):
        if self.player.rect.colliderect(self.rect):
            print("Clear!")





class Monster(GameObject):

    monsters = {}
    def __init__(self, x, y, name, mid, player : Player, speed = 5):
        super().__init__(x, y, images[name + ".png"])
        self.oncollide = monsters_oncollide[name]
        self.id = mid
        self.direction = random.choice(["d", "a", "s", "w"])
        self.speed = speed
        self.player = player
        Monster.monsters[str(self.id)] = self
    def update(self):
        super().update()
        if self.rect.colliderect(self.player.rect):
            self.oncollide(self.player)
            self.player.objects.remove(self)
        if self.direction == "d":
                
            newrect = self.rect
            newrect.x += self.speed
            if all((targetobject.collidable == True and not targetobject.rect.colliderect(newrect)) or targetobject.collidable == False for targetobject in self.player.objects):
                
                self.x += self.speed
            else:
                self.x -= self.speed
                if myid == 0:
                    self.direction = random.choice([ "s", "w"])
                    
                    
        if self.direction == "w":
            newrect = self.rect
            newrect.y -= self.speed
            if all((targetobject.collidable == True and not targetobject.rect.colliderect(newrect)) or targetobject.collidable == False for targetobject in self.player.objects):
                self.y -= self.speed
            else:
                self.y += self.speed
                if myid == 0:
                    self.direction = random.choice(["d", "a"])
                    send_json({"command" : "monsterdirection", "id" : self.id, "direction" : self.direction})
        if self.direction == "s":
            newrect = self.rect
            newrect.y += self.speed
            if all((targetobject.collidable == True and not targetobject.rect.colliderect(newrect)) or targetobject.collidable == False for targetobject in self.player.objects):
                self.y += self.speed
            else:
                self.y -= self.speed
                if myid == 0:
                    self.direction = random.choice(["d", "a"])
                    send_json({"command" : "monsterdirection", "id" : self.id, "direction" : self.direction})
        if self.direction == "a":
            newrect = self.rect
            newrect.x -= self.speed
            if all((targetobject.collidable == True and not targetobject.rect.colliderect(newrect)) or targetobject.collidable == False for targetobject in self.player.objects):
                self.x -= self.speed
            else:
                self.x += self.speed
                if myid == 0:
                    self.direction = random.choice([ "s", "w"])
                    send_json({"command" : "monsterdirection", "id" : self.id, "direction" : self.direction})
        if random.randint(0, 50) == 22 and myid == 0:
            newrect = self.rect
            newrect.x += self.speed
            if all((targetobject.collidable == True and not targetobject.rect.colliderect(newrect)) or targetobject.collidable == False for targetobject in self.player.objects):
                self.direction = "d"
                
                send_json({"command" : "monsterdirection", "id" : self.id, "direction" : self.direction})
                return
            newrect = self.rect
            newrect.y -= self.speed
            if all((targetobject.collidable == True and not targetobject.rect.colliderect(newrect)) or targetobject.collidable == False for targetobject in self.player.objects):
                self.direction = "w"
                send_json({"command" : "monsterdirection", "id" : self.id, "direction" : self.direction})
                return
            newrect = self.rect
            newrect.y += self.speed
            if all((targetobject.collidable == True and not targetobject.rect.colliderect(newrect)) or targetobject.collidable == False for targetobject in self.player.objects):
                self.direction = "s"
                send_json({"command" : "monsterdirection", "id" : self.id, "direction" : self.direction})
                return
            newrect = self.rect
            newrect.x -= self.speed
            if all((targetobject.collidable == True and not targetobject.rect.colliderect(newrect)) or targetobject.collidable == False for targetobject in self.player.objects):
                self.direction = "a"
                send_json({"command" : "monsterdirection", "id" : self.id, "direction" : self.direction})
                



class Bullet(GameObject):
    
    def __init__(self, x, y, player : Player, direction, owner):
        self.player = player
        self.direction = direction
        self.owner = owner
        self.speed = BULLET_SPEED
        
        super().__init__(x + PLAYER_X, y + PLAYER_Y, images["bullet.png"], False, True)
    
    def update(self):
        super().update()
        if self.player.rect.colliderect(self.rect) and self.owner != myid:
            display.blit()
            self.player.objects.remove(self)
    
        
        if self.direction == "right":
            
            newrect = self.rect
            newrect.x += self.speed
            self.x += self.speed
            
        if self.direction == "left":
            newrect = self.rect
            newrect.y -= self.speed
            # if all((targetobject.collidable == True and not targetobject.rect.colliderect(newrect)) or targetobject.collidable == False for targetobject in self.objects):
                
        
            self.y -= self.speed
        if self.direction == "front":
            newrect = self.rect
            newrect.y += self.speed
            # if all((targetobject.collidable == True and not targetobject.rect.colliderect(newrect)) or targetobject.collidable == False for targetobject in self.objects):
            self.y += self.speed
        if self.direction == "back":
            newrect = self.rect
            newrect.x -= self.speed
            # if all((targetobject.collidable == True and not targetobject.rect.colliderect(newrect)) or targetobject.collidable == False for targetobject in self.objects):
            self.x -= self.speed
        # if all(targetobject.collidable == True and targetobject.rect.colliderect(self.rect) and targetobject != self for targetobject in self.player.objects):
        
        if not all(not targetobject.rect.colliderect(self.rect) or targetobject == self or (type(targetobject) == OtherPlayer and targetobject.id == self.owner) for targetobject in self.player.objects):
            print("remove")
            self.player.objects.remove(self)

class MoneyBag(GameObject):
    def __init__(self, tilex, tiley, player : Player) -> None:
        super().__init__(tilex * CELL_SIZE, tiley * CELL_SIZE, images["money.png"])
        self.player = player
    
    def update(self):
        if self.player.rect.colliderect(self.rect):
            self.player.objects.remove(self)
            send_json({"command" : "addmoney", "amount" : 100})
def go_to_prison(player : Player):
    player.x = 5100
    player.prison_time = time.time()
    # pass
    player.y = 50

monsters_oncollide = {
        "police" : go_to_prison,
        "teleporter" : lambda player : player.random_teleport()
}
            
    
def get_random_pos_of_quarter(quarterx, quartery):
    assert quarterx < 2, "quarterx must smaller then 2"
    assert quartery < 2, "quartery must smaller then 2"
    
    offsetx = random.randint(0, MAZE_QUARTER) * 2 * CELL_SIZE# + 1
    offsety = random.randint(0, MAZE_QUARTER) * 2 * CELL_SIZE# + 1

    return quarterx * MAZE_QUARTER + offsetx, quartery * MAZE_QUARTER + offsety





def init_images():

    global images
    imageFilename = os.listdir("./resources/images")
    for filename in imageFilename:
        
        images[filename] = pygame.transform.scale( pygame.image.load(os.path.join("./resources/images/",  filename)), transform_images.get(filename)) if transform_images.get(filename) else pygame.image.load(os.path.join("./resources/images/",  filename))




tickfreq = clock.tick(FPS)

time_buffer = []

def addToBuffer():
    
    while True:
    
        recvdatas = sock.recv(2048).decode()
        for recvdata in recvdatas.split("~"):
            if recvdata != "":
                
                try:
                    buffer.append(json.loads(recvdata))
                    # time_buffer.append(time.time())
                except Exception:
                    pass


     
        

def use_buffer(player : Player):
    global maze, myid
    if len(buffer):
        jsondata = buffer.pop(0)
        

        # print(time.time() - buffertime, "buffer-time")
        
        

        if jsondata and jsondata != "":
            command = jsondata["command"]
            
            if command == "id":
                myid = jsondata["data"]
                print(myid)
            if command == "player":
                print(jsondata)
                player.add_object(OtherPlayer(jsondata["id"]))
            
            if command == "maze":
                print("maze")
                maze = generate_maze.tolist(jsondata["maze"])

            if command == "monsterdirection":
                Monster.monsters[str(jsondata["id"])].direction = jsondata["direction"]
            
            if command == "player_state":
                
               
                targetplayer = OtherPlayer.players.get(jsondata["id"])
                if targetplayer:
                    # pass 
                    targetplayer.x = jsondata["x"] + PLAYER_X
                    targetplayer.y = jsondata["y"] + PLAYER_Y
                    targetplayer.direction = jsondata["direction"]
            if command == "spawn_monster":
                print(jsondata["x"], jsondata["y"], sep=", ")
                player.add_object(Monster(jsondata["x"], jsondata["y"], jsondata["type"], jsondata["id"], player))
            if command == "bullet":
                player.add_object(Bullet(jsondata["x"], jsondata["y"], player, jsondata["direction"], jsondata["owner"]))
            if command == "money":
                
                showtextscreencenter((1128, 80), basicfont_one, str(jsondata["money"]), (255, 255, 255))

def showtextscreencenter(pos, font : pygame.font.Font, text, color):
    textsurf = font.render(text, True, color)
    textrect = textsurf.get_rect()
    textrect.center = pos
    display.blit(textsurf, textrect)

def draw_ui():
    display.blit(images["moneypanel.png"], (992, 32))

def quit_game():
    pygame.quit()

def select(args):
    

    
    
    back_button = Button(50, 310, 100, 100, text="◀", color=(50, 50, 50), font=basicfont_one)

    next_button = Button(1130, 310, 100, 100, text="▶", color=(50, 50, 50), font=basicfont_one)

    

    

    play_rect = pygame.Rect(400, 80, 480, 560)

    index = 0

    while True:
        display.blit(images["select_background.png"], (0, 0))
        back_button.draw()
        next_button.draw()
        

        pygame.draw.rect(display, (255, 255, 230), (400, 80, 480, 560))

        showtextscreencenter((640, 560), args[index], (50, 50, 70), basicfont_one)

        
        
        # checkforquit()

        if index == 0:
            back_button.color = (100, 100, 100)
        else:
            back_button.color = (50, 50, 50)

        if index == len(args) - 1:
            next_button.color = (100, 100, 100)
        else:
            next_button.color = (50, 50, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            
            if event.type == pygame.MOUSEBUTTONDOWN and play_rect.collidepoint(event.pos):
                return index
                
            if (back_button.click(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT)) and index != 0:
                
                index -= 1
            if (next_button.click(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT)) and index < len(args) - 1:
                
                index += 1

            
        pygame.display.update()
                
def rungame():

    

    player = Player()

    

    

    threading.Thread(target=addToBuffer).start()
    while not maze:
        use_buffer(player)
        for event in pygame.event.get(pygame.QUIT):
            pygame.quit()
        display.fill((0, 125, 255))
        pygame.display.update()

    player.add_object(GameObject(5000, 0, images["prison.png"]))        
    player.add_object(GameObject(4900, 0, None, True, False, width=100, height=1024))        
    player.add_object(GameObject(6024, 0, None, True, False, width=100, height=1024))  
    player.add_object(GameObject(5000, -100, None, True, False, width=1024, height=100))        
    player.add_object(GameObject(5000, 1024, None, True, False, width=1024, height=100))        

    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            cell_x = x * CELL_SIZE
            cell_y = y * CELL_SIZE
            if cell == generate_maze.MAZE_END:
                player.add_object(MazeEnd(cell_x, cell_y, player))
            elif cell == generate_maze.MAZE_WALL:
                player.add_object(GameObject(cell_x, cell_y, images["wall.png"], True))
            elif cell == generate_maze.MAZE_MONEY:
                player.add_object(MoneyBag(y, x, player))

    # player.add_object(Monster(100, 1000, images["person_right2.png"], player))

    while True:

        
        
        
        display.fill((0, 0, 0))

        

        player.update()

        

        player.draw()

        draw_ui()

        use_buffer(player)

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    showminimap(maze)
                
                if event.key == pygame.K_SPACE:
                    send_json({"command" : "bullet"})
                if event.key == pygame.K_p:
                    send_json({"command" : "spawn_monster", "type" : "police"})
                if event.key == pygame.K_t:
                    send_json({"command" : "spawn_monster", "type" : "teleporterx"})
                
            player.setDirection(event)
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()

        jsondata = player.getState()

        send_json(jsondata)

        
        clock.tick(FPS)

def send_json(data : dict):
    data = json.dumps(data) + "~"
    sock.send(data.encode())

def showminimap(maze):
    for row in maze:
        for cell in row:
            print("■" if cell == generate_maze.MAZE_WALL else " ", end=" ")
        print()

init_images()
rungame()