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




tune_info = {
    1 : ("도", (200, 0, 0)),
    2 : ("레", (255, 155, 0)),
    3 : ("미", (200, 200, 0)),
    4 : ("파", (0, 100, 0)),
    5 : ("솔", (0, 100, 255)),
    6 : ("라", (0, 50, 200)),
    7 : ("시", (175, 35, 175)),
    8 : ("높은 도", (200, 0, 0))
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

    is_juldaumgam = json_data["is_juldaumgam"]
    play_tune( str(mtune_list[tune_idx]))
    play_tune( str(btune_list[tune_idx]), banjo=True)
    mtimer.start(mtime_list[tune_idx])
    btimer.start(btime_list[banjo_idx])
    
    
    while True:
        display.blit(images["wood.jpg"], (0, 0))
        if mtimer.ended == True and banjo_idx < len(mtune_list) - 1:
            
            tune_idx += 1
            
            play_tune( str(mtune_list[tune_idx]))
            mtimer.ended = False
            if tune_idx >= len(mtune_list) - 1:
                play_tune( str(mtune_list[tune_idx]))
            mtimer.start(mtime_list[tune_idx])
        if btimer.ended == True and banjo_idx < len(btune_list) - 1:
            
            banjo_idx += 1
            
            play_tune( str(btune_list[banjo_idx]), banjo=True)
            btimer.ended = False
            if banjo_idx >= len(btune_list) - 1:
                play_tune( str(btune_list[banjo_idx]), banjo=True)
            btimer.start(btime_list[banjo_idx])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        mtimer.update()
        btimer.update()
        # showtextscreencenter((640, 50), lang.get("listen_music"), (50, 50, 50), basicfont)
        # if not is_juldaumgam:
        #     showtextscreencenter((640, 360), get_tune_name(mtune_list[tune_idx]), (50, 50, 50), bigfont)

        pygame.display.update()

            



def play_tune(tune_id, banjo=False):
    if banjo or int(tune_id) <= 0:
        banjo_sounds[(str(abs(int(tune_id))))].play()
    else:
        tune_sounds[tune_id].play()


def init_game():
    load_json()
    load_pref()
    init_lang()
    init_images()
    init_tunes()
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
            
if __name__ == '__main__':
    music_id = int(input("music-id: "))
    
    init_game()
    listen_music(music_id)