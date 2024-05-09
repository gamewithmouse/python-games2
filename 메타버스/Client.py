import socket
import pygame
import sys, os

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

images_dict = {}
display = None

def initgame():
    global display, images_dict
    
    pygame.init()
    images = os.listdir("./images")

    for image in images:
        print(image.strip(".png"))
        images_dict[image.rsplit(".png",1)[0]] = pygame.image.load("images/"+image)

    print(images_dict)
    display = pygame.display.set_mode((1280,720))

def rungame(addr):
    
    
    x = 0
    y = 0
    map_list = [
        ["green"] * 50,
        ["green"] * 50,
        ["green"] * 50,
        ["green"] * 50,
        ["green"] * 50,
        ["green"] * 50,
        ["green"] * 50,
        ["green"] * 50,
        ["green"] * 50,
        ["green"] * 50,
        ["green"] * 50,
        ["green"] * 50,
        ["green"] * 50,
        ["green"] * 50
    ]
    Player_Info = {'x' : x, 'y' : y, "money" : 100, }

    while True:
        render_map(x, y, map_list)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            x += 1
        if key[pygame.K_w]:
            y -= 1
        if key[pygame.K_a]:
            x -= 1
        if  key[pygame.K_s]:
            y += 1

        sending = addr + "pos" + str(x)+ "," + str(y)
        #print("Sending" , sending)
        
        sock.send(sending.encode())
        
        
        data = "data"
        data = sock.recv(1024).decode()
        #print("data: ",data)
        try:
            dicts = dict(eval(data))
            map_list = dicts["map_list"]
            print("Map+list" , map_list)
        except Exception as e:
            pass
        if data.find("Player") != -1:
            data = data.strip("Playerpos")
            pos = data.split(",")
            
            data = ""
            if pos:
                
                pygame.draw.rect(display,(0,100,0),(int(pos[0]),int(pos[1]),100,100))

        pygame.draw.rect(display,(0,100,0),(590,430,100,100))
        pygame.display.update()

def render_map(x, y, map_list):
    render_start_x = int(x / 100)
    render_start_y = int(y / 100)
    offset_x = (x % 100)
    offset_y = (y % 100)
    RENDER_WIDTH = 15
    RENDER_HEIGHT = 10
    print("ddd")
    for yyy in range(RENDER_HEIGHT):
        for xxx in range(RENDER_WIDTH):

            yy = yyy + render_start_y
            xx = xxx + render_start_x
            
            target_block = map_list[yy][xx]
            blit_x = (xxx * 100) - offset_x
            blit_y = (yyy * 100) - offset_y
            
            display.blit(images_dict[target_block], (blit_x, blit_y))

def draw_UI(player_info):
    pygame.draw.rect(display)

def start():
    
    sock.connect(("127.0.0.1", 22222))
    addr = input("address:port")
    initgame()
    rungame(addr)
            
start()
