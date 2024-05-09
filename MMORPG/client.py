import pygame
import sys, random



pygame.init()


character_list = [
    {"name": "노란색 강아지", "image" : pygame.image.load('images/yellow-dog.png')},
    {"name": "하얀 강아지", "image" : pygame.image.load('images/white_dog.png')}
]
selectedindexofcharacter = 0
character = character_list[selectedindexofcharacter]
displaysize = (1200, 800)

display = pygame.display.set_mode(displaysize)

def get_font(size):
    return pygame.font.Font("Fonts.ttf", size)

def showtextscreen(text, color, font, pos):
    textsurf = font.render(text, True, color)
    display.blit(textsurf, pos)


def showtextscreencenter(text, color, font, pos):
    textsurf = font.render(text, True, color)
    textrect = textsurf.get_rect()
    textrect.center = pos
    display.blit(textsurf, textrect)


class Button:
    def __init__(self, x, y, w, h, text, color, size=30):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.color = color
        self.size = size
    def draw(self):
        pygame.draw.rect(display, self.color, (self.x, self.y, self.w, self.h), 3, 8)
        showtextscreencenter(self.text, self.color, get_font(self.size), (self.x + (self.w / 2), self.y + (self.h / 2)))
    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] >= self.x and event.pos[0] < self.x + self.w:
                if event.pos[1] >= self.y and event.pos[1] < self.y + self.h:
                    return True
                
        return False


def rungame():
    px = 100
    py = 100
    while True:
        display.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    action = menu()
                    if action == "Go to main":
                        display.fill((0, 0, 0))
                        return
        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            px += 1
        if key[pygame.K_w]:
            py -= 1
        if key[pygame.K_s]:
            py += 1
        if key[pygame.K_a]:
            px -= 1
        image = pygame.transform.scale(character["image"], (200, 70))
        display.blit(image, (px, py))
        pygame.display.update()
        

def menu():
    gotomainbutton = Button(500, 250, 200, 50, "메인 메뉴로 돌아가기", (255, 255, 255), 20)
    gotogamebutton = Button(500, 350, 200, 50, "게임으로 돌아가기", (255, 255, 255), 20)
    while True:
        for event in pygame.event.get():
            gotomain = gotomainbutton.click(event)
            gotogame = gotogamebutton.click(event)
            if gotomain:
                
                return "Go to main"
            if gotogame:
                return
        pygame.draw.rect(display, (0, 0, 0), (450, 200, 300, 500))
        pygame.draw.rect(display, (255, 255, 255), (450, 200, 300, 500), 6, 7)
        gotomainbutton.draw()
        gotogamebutton.draw()
        pygame.display.update()
            


def Character():
    global selectedindexofcharacter, character
    nextbutton = Button(800, 350, 50, 50, "▶", (255, 255, 255))
    backbutton = Button(400, 350, 50, 50, "◀", (255, 255, 255))
    submitbutton = Button(1000, 700, 150, 50, "확인", (255, 255, 255))
    
    while True:
        display.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            nextclick = nextbutton.click(event)
            backclick = backbutton.click(event)
            if selectedindexofcharacter == len(character_list) - 1:
                nextbutton.color = (150, 150, 150)
                nextclick = False
            else:
                nextbutton.color = (255, 255, 255)
            if selectedindexofcharacter == 0:
                backbutton.color = (150, 150, 150)
                backclick = False
            else:
                backbutton.color = (255, 255, 255)
            if nextclick:
                selectedindexofcharacter += 1
            if backclick:
                selectedindexofcharacter -= 1
            
            if submitbutton.click(event):
                return
            

        character = character_list[selectedindexofcharacter]
        image = pygame.transform.scale(character['image'], (300, 200))
        display.blit(image, (450, 250))
        showtextscreencenter(character["name"], (255, 255, 255), get_font(30), (displaysize[0] / 2, 500))
        submitbutton.draw()
        nextbutton.draw()
        backbutton.draw()

        pygame.display.update()

def main():
    startbutton = Button(500, 400, 200, 70, "게임 시작", (255, 255, 255))
    chrbutton = Button(500, 500, 200, 70, "캐릭터 변경", (255, 255, 255))
    
    while True:

        showtextscreencenter("Barking RPG", (255, 255, 255), get_font(50), (displaysize[0] / 2, 150))
        for event in pygame.event.get():
            startclick = startbutton.click(event)
            chrclick = chrbutton.click(event)
            if chrclick:
                Character()
            if startclick:
                rungame()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        startbutton.draw()
        chrbutton.draw()
        pygame.display.update()
            

            
        


if __name__ == '__main__':
    main()
