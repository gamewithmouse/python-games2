import pygame
import os
import sys
import random
import time

import pygame.surflock
from resources import config
from resources.utility import Fader



displaywidth = 1280
displayheight = 720
pygame.init()


display = pygame.display.set_mode((displaywidth, displayheight)) 

talkfont = pygame.font.Font("resources/fonts/neodgm.ttf", 30)

selectfont = pygame.font.Font("resources/fonts/neodgm.ttf", 10)

stationfont = pygame.font.Font("resources/fonts/notosans.ttf", 15)



images = {}

transform_images = {
    "playbutton.png" : (200, 80),
    "smartphone_menu.png" : (80, 80),
    "smartphone.png" : (320, 480),
    "person_back.png": (100, 100),
    "person_back2.png": (100, 100),
    "person_right.png": (100, 100),
    "person_right2.png": (100, 100),
    "person_left.png": (100, 100),
    "person_left2.png": (100, 100),
    "person_front.png": (100, 100),
    "person_front2.png": (100, 100),
    "KTX.png": (400, 200),
    "stobKTX.png" : (400, 200),
    "talk_panel.png" : (1020, 250),
    "selectpanel.png" : (150, 70),
    "ticketmachine.png" : (40, 100),
    "rail.png" : (100, 100),
    "tongapanel.png" : (160, 60)

}

PLAYER_X = displaywidth / 2 - transform_images["person_right.png"][0] / 2
PLAYER_Y = displayheight / 2 - transform_images["person_right.png"][1] / 2

DETAIL_OF_FADE = 100
FADE_FREQ = 255 / DETAIL_OF_FADE

FADING_TIME = 2
FADE_ALPHA_FREQ = FADING_TIME / DETAIL_OF_FADE

RAIL_COUNT = 450

KTX_SUMMON_FREQ = 10

KTX_GO_INTERVAL = 10

MAX_KTX_COUNT = 70


startsound = pygame.mixer.Sound("./resources/sounds/start.mp3")
goingsound = pygame.mixer.Sound("./resources/sounds/going.mp3")



ticketinfo = {}
talkindex = 0
talkcontent = []
selectlistno = 0
selected = ""

passed_osong_count = 0

ktx_count = 0

aleadyrided = False

fade_surf = pygame.Surface((displaywidth, displayheight))




class GameObject:
    def __init__(self, x, y, image : pygame.Surface, collidable=False):
        self.x = x
        self.y = y
        self.image = image
        self.collidable = collidable
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())
    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())





class ImageButton:
    def __init__(self, x, y, w, h, image):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = image
        self.Rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self):
        display.blit(self.image, (self.x, self.y, self.w, self.h))

    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.Rect.collidepoint(event.pos)




class Player:

    def __init__(self) -> None:
        self.fader = Fader()
        self.x = 0
        self.y = 0
        self.istwo = False  
        self.pressed_key = "None"
        self.direction = "front"
        self.place = "Deajon"
        
        self.maxspeed = 10
        self.speed = self.maxspeed
        self.objects = []
        self.drawable = True
        self.Rect = pygame.Rect(self.x + displaywidth / 2 - transform_images["person_front.png"][0],
                                self.y + displayheight / 2 - transform_images["person_front.png"][1],
                                transform_images["person_front.png"][0],
                                 transform_images["person_front.png"][1]
                                )
        

    def draw(self):
        if self.drawable:
            
            image = f"person_{self.direction}.png"
            display.blit(images[image], (PLAYER_X, PLAYER_Y))

    def update_object(self):
        for targetobject in self.objects:
            # if targetobject.collidable == True:
            #     if self.Rect.colliderect(targetobject.rect):
                    
            #         if self.pressed_key == "d":
            #             self.x = targetobject.rect.right + 1 
            #         if self.pressed_key == "w":
            #             self.y = targetobject.rect.top + 1 + PLAYER_Y
            #         if self.pressed_key == "s":
            #             self.y = targetobject.rect.bottom - 1 - PLAYER_Y
            #         if self.pressed_key == "a":
            #             self.x = targetobject.rect.left - 1 - PLAYER_X       
            #     else:
            #         self.speed = self.maxspeed
            # else:
            #     self.speed = self.maxspeed        
            # draw objects
            display.blit(targetobject.image, (self.x + targetobject.x, self.y + targetobject.y))
            # update objects
            targetobject.update()
            self.fader.draw(display)
    def add_object(self, gameobject : GameObject):
        self.objects.append(gameobject)

    def move(self):
        
        if self.pressed_key == "d":
            self.x -= self.speed
        if self.pressed_key == "w":
            self.y += self.speed
        if self.pressed_key == "s":
            self.y -= self.speed
        if self.pressed_key == "a":
            self.x += self.speed
        
        # print(self.x, ",", self.y)    
    def setDirection(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.pressed_key = "d"
                self.direction = "right"
            if event.key == pygame.K_w:
                self.pressed_key = "w"
                self.direction = "back"    
            if event.key == pygame.K_s:
                self.pressed_key = "s"
                self.direction = "front"    
            if event.key == pygame.K_a:
                self.pressed_key = "a"
                self.direction = "left"    
        # print(self.pressed_key)        
        if event.type == pygame.KEYUP:
            # print("Keyup")
            self.pressed_key = "none"
    def update(self):
        
        self.Rect = pygame.Rect(-self.x + displaywidth / 2 - transform_images["person_front.png"][0],
                                -self.y + displayheight / 2 - transform_images["person_front.png"][1],
                                transform_images["person_front.png"][0],
                                 transform_images["person_front.png"][1]
                                )
        self.move()
        self.update_object()



def find_index(line, station, tuple_index=0):
    line_station = config.station.get(line)
    for i in range(0, len(line_station)):
        print(line_station[i][tuple_index], station)
        if station == line_station[i][tuple_index]:
            return i


class KTX(GameObject):



    def __init__(self, player : Player):

        self.kind = random.choice(config.lines)
        
        self.player = player
        self.startedtime = "NONE"
        self.nextstationtime = "NONE"
        self.north = bool(random.randint(0, 1))
        self.image = f"{self.kind}KTX.png"
        self.place = "Seoul"
        self.riding = False
        self.x = 10000 if self.north else -400
        super().__init__(self.x, -220, pygame.transform.flip(images[self.image], True, False) if self.north else images[self.image])
        self.speed = -random.randint(15, 30) if self.north else random.randint(15, 30)
        
        self.passed = True
        self.passed_osong = False
        
        self.station = len(config.station.get(self.kind)) - 2 if self.north else 0
        self.fader = player.fader
        
    
    


    def dismount(self):
        global ticketinfo, aleadyrided
        ticketinfo = {}
        self.player.place = config.station.get(self.kind)[self.station][0]
        self.player.drawable = True
        self.player.y = self.y + 100 - PLAYER_Y
        self.riding = False
        aleadyrided = False
        print("dismounting")
        
    
    def update(self):
        global ticketinfo, aleadyrided, passed_osong_count
        super().update()

        if self.x >= 20000 and not self.north:
            self.x = -700 
            self.passed = True
            if self.riding:
                
                self.station += 1
                
                self.speed = random.randint(15, 30)
                if config.station[self.kind][self.station][1] == ticketinfo.get("laststation"):
                    self.speed = -20 if self.north else 20
        if self.x <= -20000 and self.north:
            self.x = 700
            self.passed = True
            if self.riding:
                
                self.station -= 1
                
                # self.speed = -random.randint(15, 30)
                self.speed = 20
                if config.station[self.kind][self.station][1] == ticketinfo.get("laststation"):
                    self.speed = -20 if self.north else 20
                
            
        
        
        if self.riding:
            
            # print(config.station[self.kind][self.station][1], "마크", ticketinfo.get("laststation"))
            show_station(self.station, self.kind, self.x, self.north)
            # print("riding")
            self.player.x = -(self.x - PLAYER_X)
            self.player.y = -(self.y - PLAYER_Y)

        
                
        
        

        if self.x > 404 or self.x < 396: 
            
            
            self.x += self.speed
        
        

            
        else:
            self.passed = False
            if self.player.Rect.colliderect(self.rect) and self.kind == ticketinfo.get("line") and not aleadyrided and ticketinfo.get("north") == self.north:
                if not self.riding:
                    self.station = find_index(ticketinfo.get("line"), self.player.place)
                print("ride")
                aleadyrided = True
                self.riding = True
                self.player.drawable = False
            if self.riding:    
                goingsound.stop()
            
            
            if (config.station[self.kind][self.station][1] == ticketinfo.get("laststation") or len(config.station[self.kind]) - 1 == self.station) and self.riding:
                self.dismount()
            if self.startedtime == "NONE":
                self.startedtime = time.time()
            if self.startedtime + KTX_GO_INTERVAL - 2 <= time.time() and self.riding:
                # startsound.play()
                pass


            if self.startedtime + KTX_GO_INTERVAL <= time.time():
                if self.riding:
                    goingsound.play()
                
                self.startedtime = "NONE"
                self.x = 411 if not self.north else 380
                
            
      
                
        if (self.x > 431 or self.x < 380) and config.station.get(self.kind)[self.station][0] == "Osong" and self.riding and not self.passed_osong and self.passed:
            self.passed_osong = True
            passed_osong_count += 1
            
            print("오송역을 통과함")
        

def show_station(stationindex : int, line : str, x : int, north : bool = False):
    stationlist = config.station[line]
    liney = 60
    texty = 45
    stationGUIInteval = 70

    
    
    stationlistlinelength = (len(stationlist) + 1) * stationGUIInteval
    pygame.draw.line(display, (150, 150, 150), (displaywidth / 2 - stationlistlinelength / 2, liney), (displaywidth / 2 + stationlistlinelength / 2, liney), 3)
    minimapx = (x * (70 / 20700) + (displaywidth / 2) - (stationlistlinelength / 2)) + ((stationindex + 1) * (stationGUIInteval))
    for i, station in enumerate(stationlist):
        x = displaywidth / 2 - stationlistlinelength / 2 + i * stationGUIInteval + stationGUIInteval
        pygame.draw.circle(display, (150, 150, 150), (x, liney), 5, 7)
        showtextscreencenter(station[1], stationfont, 
                            (x , texty), (150, 150, 150))
    if not north:
        pygame.draw.polygon(display, (150, 200, 150), [(minimapx - 5, liney - 5), (minimapx - 5, liney + 5), (minimapx + 5, liney)])
    else:
        pygame.draw.polygon(display, (150, 200, 150), [(minimapx + 5, liney - 5), (minimapx + 5, liney + 5), (minimapx - 5, liney)])
    

class TicketMachine(GameObject):
    def __init__(self, player : Player):
        super().__init__(400, 0, images["ticketmachine.png"])
        self.player = player
        self.time = "Null"
        self.state = 0
        self.state2error = False
        
        
    def update(self):
        global talkcontent, talkindex, ticketinfo

        
        if self.player.Rect.colliderect(self.rect):
            
            if self.state == 0:
                if ticketinfo != None:
                    self.state = 3
                line = select(["경부선"], "탈 노선을 선택하시오.")
                if line == "경부선":
                    print("경부선")
                    if not ticketinfo.get(line):
                        ticketinfo["line"] = "stob"
                    self.state = 1
            if self.state == 1:
                sangha = select(["상행", "하행"], "역이 없습니다. 상행, 하행을 다시 선택해주세요." if self.state2error else "상행을 탈것인가요 아니면 하행을 탈것인가요?")
                
                ticketinfo["north"] = sangha == "상행"

                self.state = 2
                
                    
            if self.state == 2:
                stationlist = config.station.get(ticketinfo.get("line"))
                if stationlist:
                    showlist = []
                    print(ticketinfo.get("line"), ",", self.player.place, ticketinfo.get("line"))
                    
                    stationindex = find_index(ticketinfo.get("line"), self.player.place)
                    print(stationindex)
                    if stationindex != None :
                        print(ticketinfo.get("north"))
                        endvalue = -1 if ticketinfo.get("north") == True else len(stationlist)
                        print(endvalue, stationindex)
                        if endvalue == -1 and stationindex == 0:
                        
                            self.state2error = True
                            self.state = 1
                            return
                            
                        for i in range(stationindex, endvalue, -1 if ticketinfo.get("north") else 1):
                            print("OK")
                            showlist.append(config.station[ticketinfo.get("line")][i][1])
                        if len(showlist) == 0:
                            print("error")
                            
                        else:    
                            ticketinfo["laststation"] = select(showlist, "역을 선택하시오.")
                            self.state = 3
                        
                    else:
                        print("error")
                        self.state2error = True
                        self.state = 2

                    

                     
                
            if self.state == 3:
                self.state2error = False
                if talkindex == -1: 
                    self.state = 0

                print(ticketinfo)
                talkindex = 0
                talkcontent = ["표 예약에 성공했습니다."]
                print(talkindex)
               
                
                


def show_howmany_passed_osong():
    display.blit(images["tongapanel.png"], (1096, 24))
    showtextscreencenter(str(passed_osong_count), talkfont, (1186, 57), (50, 50, 50))




def talk():
    
    global talkindex
    if talkindex != -1 and len(talkcontent) > 0:
        
        showtalkpanel(talkcontent[talkindex])
        

  
def showtalkpanel(content):
    display.blit(images["talk_panel.png"], (130, 450))
    showtextscreencenter(content, talkfont, (640, 595), (0, 25, 40))


def summonktx(player : Player, startedtime=None):
    global ktx_count
    if startedtime == None or startedtime + KTX_SUMMON_FREQ <= time.time() and ktx_count < MAX_KTX_COUNT:
        player.add_object(KTX(player))
        ktx_count += 1
        return time.time()
    return startedtime
        
    


def select(selectlist, content):
    
    buttons = []
    showtalkpanel(content)
    
    for i, content1 in enumerate(selectlist):
        
        button = ImageButton(1000, 380 - i * 70, 150, 70, images["selectpanel.png"])
        buttons.append(button)
        button.draw()
        showtextscreencenter(content1, talkfont, (1075, 415 - i * 70), (0, 25, 40))
    
    while True:
        
        for event in pygame.event.get():
            for i, button in enumerate(buttons):
                if button.click(event):
                    return selectlist[i]

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        
            
            

        pygame.display.update()


        
def showtextscreen(content, font, position, color):
    text_surface = font.render(content, True, color)
    display.blit(text_surface, position)

def showtextscreencenter(content, font, position, color):
    text_surface = font.render(content, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = position
    display.blit(text_surface, text_rect)


def init_sprites(player):
    railstart = -(RAIL_COUNT * 50)
    for i in range(RAIL_COUNT):
        player.add_object(GameObject(railstart + i * 100, -100, images["rail.png"]))



def init_images():
    global images
    imageFilename = os.listdir("./resources/images")
    for filename in imageFilename:
        
        images[filename] = pygame.transform.scale( pygame.image.load(os.path.join("./resources/images/",  filename)), transform_images.get(filename)) if transform_images.get(filename) else pygame.image.load(os.path.join("./resources/images/",  filename))


    # images["rail.png"] = pygame.transform.rotate(images["rail.png"], 270)

def showintro():
    global talkcontent
    talkcontent = config.intro


def main():
    global images

    


    fade_surf.fill((0, 0, 0, 255))
    fade_surf.set_alpha(255)
    
    init_images()
    

    

    playbutton = ImageButton(40, 450, 250, 100, images["playbutton.png"])
    
    while True:
        
    
    
        display.blit(images["background.png"], (0, 0))
        # display.blit(fade_surf, (0, 0))
        playbutton.draw()
        
        for event in pygame.event.get():
            if playbutton.click(event):
                rungame()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # fade_surf.set_alpha(124)
        # display.blit(fade_surf, (0, 0))
        
        pygame.display.update()        
        
def get_station(stationindex, line):
    return config.station.get(line)[stationindex] if config.station.get(line) else None
        

def rungame():
    global talkindex, talkcontent
    place = "Seoul"
 
    using_smartphone = False
    smartphone_y = displaywidth


    smartphone_Menu = ImageButton(displaywidth - 80, 300, 80, 80, images["smartphone_menu.png"])

    SMARTPHONE_X = (displaywidth / 2 - transform_images["smartphone.png"][0] / 2 + 300)

    player = Player()

    player.add_object(KTX(player))
    player.add_object(TicketMachine(player))




    clock = pygame.time.Clock()

    t = clock.tick(60)

    player.update()
    
    showintro()

    # initialize sprites
    init_sprites(player)

    startedtime = None

    

    while True:


        startedtime = summonktx(player, startedtime)
        display.fill((255, 255, 255)) 

        player.draw()

        # player.draw_object()

        # player.move()
        player.update()
        if using_smartphone or smartphone_y <= displayheight:
            display.blit(images["smartphone.png"], (SMARTPHONE_X, smartphone_y))

        if using_smartphone:
            

            if smartphone_y >= displayheight - transform_images["smartphone.png"][1]:
                smartphone_y -= 5 * t
        else:
            if smartphone_y <= displayheight:
                smartphone_y += 5 * t
        # smartphone_Menu.draw()
        
        for event in pygame.event.get():
            
            player.setDirection(event)
            if smartphone_Menu.click(event):
                using_smartphone = not using_smartphone
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if talkindex + 1 != len(talkcontent):
                        talkindex = talkindex + 1    
                    else:
                        talkindex = -1
                        talkcontent = []
                if event.key == pygame.K_RIGHT:
                    talkindex = -1
                    talkcontent = []        
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        talk()
        show_howmany_passed_osong()
        
        pygame.display.update()   
         
        clock.tick(60)        


if __name__ == '__main__':
    main()
