import pygame
import random
import sys
import os



pygame.init()

displaywidth = 1280
displayheight = 720

display = pygame.display.set_mode((displaywidth, displayheight))



images = {}

zero = ['n', 'r', 'l', 'e', 'o', 'p', 'm', '3', 'a', 's', 'w', 'd', '2', 'i', 'f', 'j', 'k', 'u', 'v']





PLAYER_HEALTHBAR_WIDTH = 400
HEALTHBAR_HEALTH1_WIDTH = 4
HEALTHBAR_MARGIN_TOP = 50
HEALTHBAR_MARGIN_RIGHT = 50
HEALTHBAR_START = displaywidth - PLAYER_HEALTHBAR_WIDTH - HEALTHBAR_MARGIN_RIGHT
HEALTHBAR_HEIGHT = 50

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
    "healthbar_back.png": (PLAYER_HEALTHBAR_WIDTH, HEALTHBAR_HEIGHT),
    
    "healthbar_edge.png": (HEALTHBAR_HEALTH1_WIDTH, HEALTHBAR_HEIGHT),
}

HEAPTHBAR_EDGE = "healthbar_edge.png"



PERSON_RIGHT = "person_right.png"

clock = pygame.time.Clock()

FPS = 60

TICK = clock.tick(FPS)





BULLET_LONG_LENGTH = 10
BULLET_SHORT_LENGTH = 7


PLAYER_X = displaywidth / 2 + transform_images[PERSON_RIGHT][0] / 2
PLAYER_Y = displayheight / 2 + transform_images[PERSON_RIGHT][1] / 2



def init_images():
    global images
    imageFilename = os.listdir("./resources/images")
    for filename in imageFilename:
        
        images[filename] = pygame.transform.scale( pygame.image.load(os.path.join("./resources/images/",  filename)), transform_images.get(filename)) if transform_images.get(filename) else pygame.image.load(os.path.join("./resources/images/",  filename))




class GameObject:
    def __init__(self, x, y, image : pygame.Surface, drawable=True, collidable=False, width=0, height=0):
        self.x = x
        self.drawable = drawable
        self.y = y
        self.image = image
        self.collidable = collidable
        self.w = width
        self.h = height
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height()) if self.drawable else pygame.Rect(self.x, self.y, self.w, self.h)
    def update(self):
        
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height()) if self.drawable else pygame.Rect(self.x, self.y, self.w, self.h)




class Player:

    def __init__(self) -> None:
        
        self.max_health = 100
        self.health = self.max_health
        self.x = 0
        self.y = 0
        self.istwo = False  
        self.pressed_key = "None"
        self.direction = "front"
        
        
        self.maxspeed = 10
        self.speed = self.maxspeed
        self.objects = []
        self.drawable = True
        
        self.rect = pygame.Rect(PLAYER_X,
                                PLAYER_Y,
                                transform_images[PERSON_RIGHT][0],
                                 transform_images[PERSON_RIGHT][1]
                                )
    
    def draw_healthbar(self):
        
        display.blit(images[HEAPTHBAR_EDGE], (HEALTHBAR_START - HEALTHBAR_HEALTH1_WIDTH, HEALTHBAR_MARGIN_TOP))
        display.blit(images[HEAPTHBAR_EDGE], (displaywidth - HEALTHBAR_MARGIN_RIGHT, HEALTHBAR_MARGIN_TOP))
        display.blit(images["healthbar_back.png"], (HEALTHBAR_START, HEALTHBAR_MARGIN_TOP))
        bar_image = pygame.transform.scale(images["healthbar.png"], (self.health * HEALTHBAR_HEALTH1_WIDTH, HEALTHBAR_HEIGHT))
        display.blit(bar_image, (HEALTHBAR_START, HEALTHBAR_MARGIN_TOP))

    def draw(self):
        if self.drawable:
            
            image = f"person_{self.direction}.png"
            display.blit(images[image], self.rect)

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
            if targetobject.drawable:
                display.blit(targetobject.image, (self.x + targetobject.x, self.y + targetobject.y))
            # update objects
            targetobject.update()
            # self.fader.draw(display)
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
    def setdirection(self, event):
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
            if event.key == pygame.K_SPACE:
                self.add_object(Bullet(self.direction, 100, self.x + self.rect.centerx, self.y + self.rect.centery, self))    
            
        # print(self.pressed_key)        
        if event.type == pygame.KEYUP:
            # print("Keyup")
            self.pressed_key = "none"
    def update(self):
        
        self.rect = pygame.Rect(PLAYER_X,
                                PLAYER_Y,
                                transform_images[PERSON_RIGHT][0],
                                 transform_images[PERSON_RIGHT][1]
                                )
        print("update") 
        self.move()
        self.update_object()
        self.draw_healthbar()




class Bullet(GameObject):
    def __init__(self, direction, damage, x, y, player : Player):
        self.speed = 1
       
        self.direction = direction
        self.damage = damage
        self.player = player

        super().__init__(x, y, None, False, False, BULLET_LONG_LENGTH if self.direction in ["left", "right"] else BULLET_SHORT_LENGTH, BULLET_SHORT_LENGTH if self.direction in ["left", "right"] else BULLET_LONG_LENGTH)

    def update(self):
        super().update()
        pygame.draw.rect(display, (50, 50, 50), (self.x, self.y, BULLET_LONG_LENGTH if self.direction in ["left", "right"] else BULLET_SHORT_LENGTH, BULLET_SHORT_LENGTH if self.direction in ["left", "right"] else BULLET_LONG_LENGTH))
        if self.direction == "right":
            self.x += self.speed * TICK
        if self.direction == "back":
            self.y -= self.speed * TICK
        if self.direction == "front":
            self.y += self.speed * TICK
        if self.direction == "left":
            self.x -= self.speed * TICK
        # if self.player.rect.colliderect(self.rect):
        #     print("damage:", self.damage)
        #     self.player.objects.remove(self)
        
        

# class Meme:
#     def __init__(self):
        




def main():
    init_images()
    while True:
        rungame()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def rungame():

    player = Player()

    while True:
        display.fill((255, 255, 255))
        player.draw()
        for event in pygame.event.get():
            player.setdirection(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        player.update()
        
        clock.tick(FPS)
        pygame.display.update()


if __name__ == "__main__":
    main()