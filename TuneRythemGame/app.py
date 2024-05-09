import pygame
import sys
import os

import time

import pygame

import json

pygame.init()

display = pygame.display.set_mode((1280, 720))


bigfont = pygame.font.Font("./resources/fonts/ONE Mobile POP.ttf", 70)

basicfont = pygame.font.Font("./resources/fonts/ONE Mobile POP.ttf", 40)

smallfont = pygame.font.Font("./resources/fonts/ONE Mobile POP.ttf", 20)



tune_info = {
    1 : ("도", (200, 0, 0)),
    2 : ("레", (255, 155, 0)),
    3 : ("미", (200, 200, 0)),
    4 : ("파", (0, 100, 0)),
    5 : ("솔", (0, 100, 255)),
    6 : ("라", (0, 50, 200)),
    7 : ("시", (175, 35, 175)),
    8 : ("높은 도", (200, 0, 0)),
    -7 : ("낮은 시", (175, 35, 175)),
    -6 : ("낮은 라", (0, 50, 200)),
    -5 : ("낮은 솔", (0, 100, 255))
}

tune_sounds = {}

banjo_sounds = {}


images = {}


TUNE_PATH = "./resources/sounds/tunes"

transform_images = {
    "wood.jpg": (1280, 720),
    "play.png": (200, 80),
    "lang.png": (80, 80),
    "home.png": (80, 80),
    "ok.png" : (120, 50)

}

pref = {}

lang = {}

json_data = {}

filpping_sound = pygame.mixer.Sound("./resources/sounds/flipping.wav")


JSON_PATH = "resources/info.json"

PREF_PATH = "resources/setting.txt"

MAX_LIVES = 2

def load_pref():
    global pref
    with open(PREF_PATH, "r", encoding="utf-8") as f:
        pref = dict(eval(" ".join(f.readlines())))
        
    
def init_lang():
    global lang
    lang = json_data["lang"].get((pref.get("lang")))




def init_tunes():
    tunes_list = os.listdir(TUNE_PATH)
    tunes_list.sort(key=lambda tunes: int(tunes[0:2].strip(".").strip("-")))
    
    for i, filename in enumerate(tunes_list):
        targettunepath = TUNE_PATH + "/" + filename
        if filename.find("-") != -1:
            banjo_sounds[str(filename.replace("-.mp3", ""))] = pygame.mixer.Sound(targettunepath)
            continue
        tune_sounds[str(filename.replace(".mp3", ""))] = pygame.mixer.Sound(targettunepath)
    
        
        
        


def init_images():
    global images
    imageFilename = os.listdir("./resources/images")
    for filename in imageFilename:
        
        images[filename] = pygame.transform.scale( pygame.image.load(os.path.join("./resources/images/",  filename)), transform_images.get(filename)) if transform_images.get(filename) else pygame.image.load(os.path.join("./resources/images/",  filename))





def load_json():
    global json_data
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        json_data = json.load(f)



def listen_music(song_index):    
    print(pref["lang"])
    mtune_list = json_data["songs"][song_index]["melody"]["tunes"]
    
    mtime_list = json_data["songs"][song_index]["melody"]["times"]

    btune_list = json_data["songs"][song_index]["banjo"]["tunes"]
    
    btime_list = json_data["songs"][song_index]["banjo"]["times"]

    mtimer = Timer()

    btimer = Timer()

    tune_idx = 0

    banjo_idx = 0
    
    assert len(mtune_list) == len(mtime_list), f"tune_list's length should same with time_list's length (m) - {len(mtune_list)} : {len(mtime_list)}"
    assert len(btune_list) == len(btime_list), f"tune_list's length should same with time_list's length (b) - {len(btune_list)} : {len(btime_list)}"

    is_juldaumgam = pref["is_juldaumgam"]
    play_tune( str(mtune_list[tune_idx]))
    play_tune( str(btune_list[tune_idx]), banjo=True)
    mtimer.start(mtime_list[tune_idx])
    btimer.start(btime_list[banjo_idx])
    
    
    while True:
        display.blit(images["wood.jpg"], (0, 0))

        

        if mtimer.ended == True and tune_idx < len(mtune_list) - 1:
            
            tune_idx += 1
            
            play_tune( str(mtune_list[tune_idx]))
            mtimer.ended = False
            if tune_idx >= len(mtune_list) - 1:
                play_tune( str(mtune_list[tune_idx]))
            mtimer.start(mtime_list[tune_idx])
        if mtimer.ended == True and tune_idx >= len(mtune_list) - 1:
            return
        if btimer.ended == True and banjo_idx < len(btune_list) - 1:
            
            banjo_idx += 1
            
            play_tune( str(btune_list[banjo_idx]), banjo=True)
            btimer.ended = False
            if banjo_idx >= len(btune_list) - 1:
                play_tune( str(btune_list[banjo_idx]), banjo=True)
            btimer.start(btime_list[banjo_idx])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        mtimer.update()
        btimer.update()
        showtextscreencenter((640, 50), lang.get("listen_music"), (50, 50, 50), basicfont)
        if not is_juldaumgam:
            showtextscreencenter((640, 360), get_tune_name(mtune_list[tune_idx]), (50, 50, 50), bigfont)

        pygame.display.update()

def quit_game():
    with open(PREF_PATH, "w", encoding="utf-8") as fw:
        fw.write(str(pref))

    pygame.quit()
    sys.exit()
            



def play_tune(tune_id, banjo=False):
    if banjo or int(tune_id) <= 0:
        banjo_sounds[(str(abs(int(tune_id))))].play()
    else:
        tune_sounds[tune_id].play()

def checkforquit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def init_game():
    load_json()
    load_pref()
    init_lang()
    init_images()
    init_tunes()

def get_tune_name(tune_id):
    return lang.get("tune" + str(tune_id))

def main():
    global pref
    init_game()

    pygame.display.set_caption("A one pitch")
    pygame.display.set_icon(images["note.png"])
    
    start_button = Button(530, 530, 240, 80, image=images["play.png"])
    lang_button = Button(1120, 560, 80, 80, image=images["lang.png"])

    juldaumgam_button = Button(1120, 40, 80, 80, text="O" if pref["is_juldaumgam"] else "X", font=basicfont)

    juldaumgam_popup = Buttonright(1080, 40, 300, 80, text=lang.get("is_juldaumgam"), font=smallfont, color=(50, 50, 50))

    
    
    while True:

        display.blit(images["wood.jpg"], (0, 0))
        start_button.draw()
        lang_button.draw()
        juldaumgam_button.draw()
        if pref["show-perfect-pitch-popup"] and not pref["is_juldaumgam"]:
            juldaumgam_popup.draw()
        showtextscreencenter((640, 320), "A One Pitch", (50, 50, 50), bigfont)

        for event in pygame.event.get():
            if juldaumgam_button.click(event):
                pref["is_juldaumgam"] = not pref["is_juldaumgam"]
                juldaumgam_button.text = text="O" if pref["is_juldaumgam"] else "X"
            if juldaumgam_popup.click(event):
                pref["show-perfect-pitch-popup"] = False
            if event.type == pygame.QUIT:
                quit_game()
            if start_button.click(event):
                start_game()
            if lang_button.click(event):
                pref["lang"] = chooselang()
                init_lang()
                
        pygame.display.update()
        

def start_game():
    songindex = choosesong()

    if songindex == "h":
        return

    tune = choose_tune(songindex)

    if tune == "h":
        return

    game_result = rungame(songindex, tune)
    end_screen(game_result)
    print(game_result)

    

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

class Buttonright(Button):
    def __init__(self, x, y, w, h, image=None, text=None, color=(0, 0, 0, 0), font=None):
        super().__init__(x, y, w, h, image, text, color, font)
        self.rect.right = x
        # print(self.rect.centery)
    
    def draw(self):
        showtextscreenright((self.rect.right, self.rect.centery), self.text, self.color, self.font)

def showtextscreencenter(pos, text, color, font):
    textsurf = font.render(text, True, color)
    textrect = textsurf.get_rect()
    textrect.center = pos
    # if text.find("Space") != -1:
        # print(textrect.topleft)
        # print(textrect.size)
    display.blit(textsurf, textrect)


def showtextscreenright(pos, text, color, font):
    textsurf = font.render(text, True, color)
    textrect = textsurf.get_rect()
    textrect.right = pos[0]
    textrect.centery = pos[1]
    # if text.find("Space") != -1:
        # print(textrect.topleft)
        # print(textrect.size)
    display.blit(textsurf, textrect)

def choose_tune(song_index):
    tune_setted = list(set(json_data["songs"][song_index]["melody"]["tunes"]))

    tune_setted.sort()
    
    back_button = Button(50, 310, 100, 100, text="◀", color=(50, 50, 50), font=basicfont)

    next_button = Button(1130, 310, 100, 100, text="▶", color=(50, 50, 50), font=basicfont)

    home_button = Button(10, 10, 80, 80, image=images["home.png"])

    

    play_rect = pygame.Rect(400, 80, 480, 560)

    tune_index = 0

    while True:
        display.blit(images["wood.jpg"], (0, 0))
        back_button.draw()
        next_button.draw()
        home_button.draw()

        pygame.draw.rect(display, (255, 255, 230), (400, 80, 480, 560))

        showtextscreencenter((640, 560), get_tune_name(tune_setted[tune_index]), (50, 50, 70), basicfont)

        
        pygame.draw.circle(display, tune_info.get(tune_setted[tune_index])[1], (640, 320), 60)
        # checkforquit()

        if tune_index == 0:
            back_button.color = (100, 100, 100)
        else:
            back_button.color = (50, 50, 50)

        if tune_index == len(tune_setted) - 1:
            next_button.color = (100, 100, 100)
        else:
            next_button.color = (50, 50, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if home_button.click(event):
                return "h"
            if event.type == pygame.MOUSEBUTTONDOWN and play_rect.collidepoint(event.pos):
                return tune_index + 1
                
            if (back_button.click(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT)) and tune_index != 0:
                filpping_sound.play()
                tune_index -= 1
            if (next_button.click(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT)) and tune_index < len(tune_setted) - 1:
                filpping_sound.play()
                tune_index += 1

            
        pygame.display.update()
        


def choosesong():
    display.fill((0, 0, 0))

    home_button = Button(10, 10, 80, 80, image=images["home.png"])

    song_name_list = [song["name"] for song in json_data["songs"]]

    back_button = Button(50, 310, 100, 100, text="◀", color=(50, 50, 50), font=basicfont)

    next_button = Button(1130, 310, 100, 100, text="▶", color=(50, 50, 50), font=basicfont)

    

    play_rect = pygame.Rect(400, 80, 480, 560)

    song_index = 0

    while True:
        
        display.blit(images["wood.jpg"], (0, 0))
        home_button.draw()
        back_button.draw()
        next_button.draw()

        pygame.draw.rect(display, (255, 255, 230), (400, 80, 480, 560))

        showtextscreencenter((640, 560), song_name_list[song_index], (50, 50, 70), basicfont)

        display.blit(images["note.png"], (520, 160))
        # checkforquit()

        if song_index == 0:
            back_button.color = (100, 100, 100)
        else:
            back_button.color = (50, 50, 50)

        if song_index == len(song_name_list) - 1:
            next_button.color = (100, 100, 100)
        else:
            next_button.color = (50, 50, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if home_button.click(event):
                return "h"
            if event.type == pygame.MOUSEBUTTONDOWN and play_rect.collidepoint(event.pos):
                return song_index
                
            if (back_button.click(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT)) and song_index != 0:
                filpping_sound.play()
                song_index -= 1
            if (next_button.click(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT)) and song_index < len(song_name_list) - 1:
                filpping_sound.play()
                song_index += 1

        
        pygame.display.update()

def chooselang():
    
    display.fill((0, 0, 0))

    lang_list = list(json_data.get("lang").keys())

    back_button = Button(50, 310, 100, 100, text="◀", color=(50, 50, 50), font=basicfont)

    next_button = Button(1130, 310, 100, 100, text="▶", color=(50, 50, 50), font=basicfont)

    

    play_rect = pygame.Rect(400, 80, 480, 560)

    lang_index = 0

    while True:
        display.blit(images["wood.jpg"], (0, 0))
        back_button.draw()
        next_button.draw()

        pygame.draw.rect(display, (255, 255, 230), (400, 80, 480, 560))

        showtextscreencenter((640, 560), lang_list[lang_index], (50, 50, 70), basicfont)

        display.blit(images["note.png"], (520, 160))
        # checkforquit()

        if lang_index == 0:
            back_button.color = (100, 100, 100)
        else:
            back_button.color = (50, 50, 50)

        if lang_index == len(lang_list) - 1:
            next_button.color = (100, 100, 100)
        else:
            next_button.color = (50, 50, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN and play_rect.collidepoint(event.pos):
                return lang_list[lang_index]
                
            if (back_button.click(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT)) and lang_index != 0:
                filpping_sound.play()
                lang_index -= 1
            if (next_button.click(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT)) and lang_index < len(lang_list) - 1:
                filpping_sound.play()
                lang_index += 1

        
        pygame.display.update()

def rungame(song_index, tune):
    listen_music(song_index)
    display.fill((0, 0, 0))

    
    mtimer = Timer()
    note_index = 0

    banjo_idx = 0

    btimer = Timer()
    tune_list = json_data["songs"][song_index]["melody"]["tunes"]
    
    time_list = json_data["songs"][song_index]["melody"]["times"]

    btune_list = json_data["songs"][song_index]["banjo"]["tunes"]

    btime_list = json_data["songs"][song_index]["banjo"]["times"]

    lives = MAX_LIVES

    
    
    assert len(tune_list) == len(time_list), "tune_list's length should same with time_list's length"
    
    print("asdf")
    for i in range(3, 1, -1):
        print("asdf")
        display.blit(images["wood.jpg"], (0, 0))
        showtextscreencenter((640, 30), lang.get("yournote-f") + get_tune_name(tune) + lang.get("yournote-b"), (50, 50, 50), basicfont)
        showtextscreencenter((640, 360), str(i), (50, 50, 50), bigfont)
        pygame.display.update()
        time.sleep(0.5)
    display.blit(images["wood.jpg"], (0, 0))
    showtextscreencenter((640, 360), lang.get("start"), (50, 50, 50), bigfont)
    pygame.display.update()
    time.sleep(0.5)
    mtimer.start(time_list[note_index])
    btimer.start(btime_list[banjo_idx])

    tonga = False

    

    play_tune( str(tune_list[note_index]))
    play_tune( str(btune_list[banjo_idx]), banjo=True)
    try:

        while True:
            display.blit(images["wood.jpg"], (0, 0))

            showtextscreencenter((640, 360), lang.get("space"), (50, 50, 50), bigfont)
            showtextscreencenter((640, 30), lang.get("yournote-f") + get_tune_name(tune) + lang.get("yournote-b"), (50, 50, 50), basicfont)
            showtextscreencenter((1000, 30), lang.get("lives") + str(lives), (50, 50, 50), basicfont)
            # showtextscreencenter((640, 360), "Space Bar", (50, 50, 50), bigfont)

            pygame.draw.rect(display, (50, 50, 50), (115, 315, 390, 90), 4, 15)
            
            mtimer.update()
            btimer.update()

            if btimer.ended == True and banjo_idx < len(btune_list) - 1:
                
                banjo_idx += 1
                
                play_tune( str(btune_list[banjo_idx]), banjo=True)
                btimer.ended = False
                if banjo_idx >= len(btune_list) - 1:
                    play_tune( str(btune_list[banjo_idx]), banjo=True)
                btimer.start(btime_list[banjo_idx])
        
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if tune_list[note_index] != tune:
                        
                        
                        if lives == 1:
                            
                            return 1 
                        lives -= 1
                        break
                    tonga = True
            if mtimer.ended == True:
                
                    
                note_index += 1 
                play_tune( str(tune_list[note_index]))
            
                if note_index != 0 and tune_list[note_index - 1] == tune and not tonga:
                    
                    if lives == 0:
                        return 2
                    lives -= 1
                    break
                tonga = False
                mtimer.start(time_list[note_index])    
                mtimer.ended = False
            pygame.display.update()
            
            
    except IndexError:
        return 0
            
            
                


class Timer:
    def __init__(self):
        self.started_time = None
        self.started = False
        self.amount = 0
        self.ended = False
    
    def start(self, amount):
        self.started = True
        self.amount = amount
        self.started_time = time.time()
    
    def update(self):
        
        if self.started_time and self.started_time + self.amount <= time.time() and self.started:
            self.started = False
            self.ended = True
            
def end_screen(result):
    title_text = lang.get("result-" + str(result))

    ok_button = Button(580, 500, 120, 50, image=images["ok.png"])
    while True:

        display.blit(images["wood.jpg"], (0, 0))
        ok_button.draw()
        showtextscreencenter((640, 320), title_text, (50, 50, 50), bigfont)
        for event in pygame.event.get():
            if ok_button.click(event):
                return
        pygame.display.update()


if __name__ == '__main__':
    main() 
    
    