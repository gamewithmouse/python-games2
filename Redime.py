import pygame, sys, threading, random

import timedict
pygame.init()
music_list = ["minecraft", "music", "Butter", "night Of Nights", "Ievan Polkka"]
type_list = ["basic"]
SCREENWIDTH  = 700
SCREENHEIGHT = 1000
display = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
alpha_surf = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))   
alpha_surf.set_alpha(128)
customsurf = [pygame.Surface((SCREENWIDTH, SCREENHEIGHT))] * 5

WHITE = (255, 255, 255)
SKYBLUE = (0,150,255)
def get_font(size):
    font = pygame.font.Font("GROBOLD.ttf", size)
    return font
Settings = {"FPS": 100, "dd":"dd"}

def home():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                music = SelectMusic()
                Game_Basic(music[0])
                return 
        showtextscreen(display, "Redime", (255,255,255), get_font(100), (170,100))
        showtextscreen(display, "Press Keys For Start Game", (255,255,255), get_font(40), (100,600))
        pygame.display.update()
def Setting():
    display.fill((0, 0, 0))
    
    BasicButton = Button(50, 50, 200, 50, "Basic")
    while True:
        BasicButton.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.draw.line(display, (255, 255, 255), (300, 0), (300, SCREENHEIGHT), 5)
        pygame.display.update()
        

    
class Blocks:
    def __init__(self, x):
        self.y = 0
        self.x = x

    def draw(self):
        if self.x == 0:
            xx = 210
        if self.x == 1:
            xx = 280
        if self.x == 2:
            xx = 350
        if self.x == 3:
            xx = 420
        
        pygame.draw.rect(display, (255, 255, 255, 100  ), (xx, self.y, 70, 150))
    def move(self, df):
        self.y += (1 * df)
class Button:

    def __init__(self, x, y, w, h, text):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.rect = None
    def draw(self):
        pygame.draw.rect(display, (255, 255, 255), (self.x, self.y, self.w, self.h), 4, 4)
        showtextscreen(display, self.text, (255, 255, 255), get_font(30), (self.x + self.w/2 - 40, self.y + self.h / 2 - 15))
    def isclicked(self, pos):
        
        return Isclicked(pos, self.x, self.y, self.w, self.h)

def Isclicked(pos, sx, sy, w, h):
    if (pos == None):
        return False
    
    if pos[0] >= sx and pos[0] <= sx + w:
        if pos[1] >= sy and pos[1] <= sy + h:
            return True
        else:
            return False
    else:
        return True
blocks = []
def SelectMusic():
    Selectedmusic = 0
    mouseclicked = False
    Selectedtype = 0
    Okbutton = Button(520, 930, 150, 50, "OK")
    SettingBtn = Button(300, 930, 150, 50, "Settings")
    events = None
    cursor_pos = None
    
    while True:
        display.fill((0, 0, 0))
        showtextscreen(display, "Select Music", (255,255,255), get_font(40), (70,50))
        showtextscreen(display, "Select Type", (255,255,255), get_font(40), (450,50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseclicked = True
                if SettingBtn.isclicked(event.pos):
                    print("SETtong")
                    Setting()
                    return (None, None)
                if Okbutton.isclicked(event.pos):
                    return (music_list[Selectedmusic], type_list[Selectedtype])
            
                    
                cursor_pos = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if not Selectedmusic < 0:

                        Selectedmusic -= 1
                if event.key == pygame.K_DOWN:
                    if not Selectedmusic > len(music_list):
                        Selectedmusic +=1 
                if event.key == pygame.K_RETURN:
                    return (music_list[Selectedmusic], type_list[Selectedtype])
                    
            if event.type == pygame.QUIT:
                sys.exit()
            events = event
        pygame.draw.line(display, (255,255,255), (SCREENWIDTH / 2 + 49, 0), (SCREENWIDTH / 2 + 49, SCREENHEIGHT ), 3)
        Okbutton.draw()
        SettingBtn.draw()
        for i, name in enumerate(type_list):
            y = (50 * i) + 100
            color = WHITE
            if i == Selectedtype:
                color = SKYBLUE
            else:
                color = WHITE
            
            pygame.draw.rect(display, color,(450,y,200,50), 2, 10)
            showtextscreen(display, name, color, get_font(30), (520, y+10))
            
            
            if mouseclicked and Isclicked(cursor_pos, 450, y, 300, 50) :
                Selectedtype = i

                print(y)
                print("Selected music :", music_list[Selectedtype])
                mouseclicked = False
                break
        for i, name in enumerate(music_list):
            y = (50 * i) + 100
            color = WHITE
            if i == Selectedmusic:
                color = SKYBLUE
            else:
                color = WHITE
            pygame.draw.rect(display, color,(50,y,300,50), 2, 10)
            showtextscreen(display, name, color, get_font(30), (70, y+10))
            
            
            if mouseclicked and Isclicked(cursor_pos, 50, y, 300, 50) :
                Selectedmusic = i

                print(y)
                print("Selected music :", music_list[Selectedmusic])
                mouseclicked = False
                break

       
        pygame.display.update()
def rungame(Music, Type):
    pass
def Game_Basic(Music):
    combo = False
    if Music:
        
        Musicf = pygame.mixer.Sound("sounds/"+Music+".mp3")
        Score = 0
        Musicf.play()
        
        print(type(Music))
        t = threading.Thread(target=makenew, args=(Music,))
        t.start()
        clicked = [False] * 4
        print(clicked)
        scoreculltime = 0
        Clock = pygame.time.Clock()
        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        clicked[0] = 1
                        print("A")
                    if event.key == pygame.K_s:
                        clicked[1] = 1
                        print("A")
                    if event.key == pygame.K_d:
                        clicked[2] = 1
                    if event.key == pygame.K_f:
                        clicked[3] = 1
    
            df = Clock.tick(Settings["FPS"])
            display.fill((0, 0, 0))
            
            # customsurf에 있는 것을 display에 보여준다.
            
            # for surf in customsurf:
            #     display.blit(surf, (0, 0))
                
            # 블럭을 내려오게 하며 블럭 관련된 것을 처리한다.  

            for i, block in enumerate(blocks):
                
                if block.y > SCREENHEIGHT:
                    del blocks[i]
                if block.y > 900 and block.y < 960:
                    print(scoreculltime)
                    if clicked[block.x] != False and scoreculltime == 0:
                        Score += 1
                        scoreculltime = Settings["FPS"] / 2
                        print("score")
                if block.y > 900 and block.y < 920:
                    print(scoreculltime)
                    if clicked[block.x] != False and scoreculltime == 0:
                        Score += 1
                        scoreculltime = Settings["FPS"] / 4
                        combo = Settings["FPS"] / 5
                block.move(df)
                block.draw()
            # 위치가 고정된 ui를 표시한다.
            showtextscreen(display,"Score : "+str(Score), (255, 255, 255), get_font(30),( SCREENWIDTH - 150, SCREENHEIGHT - 100))
            # showtextscreenCenter(customsurf[0], "Combo", (255, 255, 255), get_font(70), (SCREENWIDTH / 2, SCREENHEIGHT / 2))
            drawuiBasic()
            # 클릭 이벤트를 처리한다.
            for a, bools in enumerate(clicked):
               
                if bools != False:
                    
                    pygame.draw.rect(alpha_surf, (255, 255, 255), (215+(a * 70), 900, 60, 60), 4)
                    clicked[a] += 1
                else:
                    pygame.draw.rect(display, (255, 255, 255), (215+(a * 70), 900, 60, 60), 4)
                if bools > Settings["FPS"] / 2:
                    clicked[a] = False
            # customsurf[0].set_alpha(combo)
            alpha_surf.set_alpha(128)
            alpha_surf.blit(display, (0, 0))
            pygame.display.update()
            if scoreculltime > 0:
                scoreculltime -= 1
            if combo > 0:
                combo -= 1
def drawuiBasic():
    pygame.draw.line(display, (255, 255, 255), (210,0),(210,SCREENHEIGHT), 3)
    pygame.draw.line(display, (255, 255, 255), (280,0),(280,SCREENHEIGHT), 3)
    pygame.draw.line(display, (255, 255, 255), (350,0),(350,SCREENHEIGHT), 3)
    pygame.draw.line(display, (255, 255, 255), (420,0),(420,SCREENHEIGHT), 3)
    pygame.draw.line(display, (255, 255, 255), (490,0),(490,SCREENHEIGHT), 3)
def makenew(music):
    print("OK")
    Clock = pygame.time.Clock()
    for wait in timedict.TimeDict[music]:

        blocks.append(Blocks(random.randint(0,3)))
        Clock.tick(wait)
        


def showtextscreen(where, text, color, font, pos):
    fontsurf = font.render(text, True, color)
    where.blit(fontsurf, pos)
def showtextscreenCenter(where, text, color, font, pos):
    fonsurf = font.render(text, True, color)
    rect = fonsurf.get_rect()
    rect.center = pos
    where.blit(fonsurf, rect)
    
home()