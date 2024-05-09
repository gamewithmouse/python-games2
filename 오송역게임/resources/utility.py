import pygame




class Fader:
    def __init__(self, resoulotion = (1280, 720)):
        self.mode = "None"
        self.alpha = 0
        self.surface = pygame.Surface(resoulotion)
        self.surface.fill((0, 0, 0))
        self.surface.set_alpha(self.alpha)   
    def draw(self, display : pygame.Surface):
        # if self.mode == "In":
        #     if self.alpha >= 255:
        #         self.mode = "None"
        #     self.alpha += 1
        # if self.mode == "Out":
        #     if self.alpha <= 0:
        #         self.mode = "None"
        #     self.alpha -= 1
        # self.surface.set_alpha(self.alpha)   
        # display.blit(self.surface, (0, 0))    
        pass

    def fade_in(self):
        self.mode = "In"
    def fade_out(self):
        self.mode = "Out"    