import pygame

pygame.init()
display = pygame.display.set_mode((800, 1000))
def chess():
    print("Playing Chess!")
game_list = [
    {"Name" : "Chess", "function": chess()}
]

def main(): # 게임 선택 창
    while True:
        display.fill((230, 230, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        pygame.display.update()
    
if __name__ == "__main__":
    main()


# http://coummunitycenter.com