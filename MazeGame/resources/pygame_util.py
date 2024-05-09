import pygame
import time

healthbar_back = pygame.image.load("./resources/images/healthbar_back.png")
healthbar_edge = pygame.image.load("./resources/images/healthbar_edge.png")
healthbar = pygame.image.load("./resources/images/healthbar.png")


class HealthBar:
    def __init__(self, max_health=100, healthbar_width=300, healthbar_height=50):
        self.health = max_health
        self.max_health = max_health
        self.healthbar_one_width = healthbar_width / max_health
        self.heatlhbar_width = healthbar_width + self.healthbar_one_width * 2
        self.healthbar_height = healthbar_height
        self.healthbar_back = pygame.transform.scale(healthbar_back, (healthbar_width, self.healthbar_height))
        self.healthbar_edge = pygame.transform.scale(healthbar_edge, (self.healthbar_one_width, self.healthbar_height))
        self.surface = pygame.surface.Surface((healthbar_width, healthbar_height))
        
    
    def update(self):
        
        healthbar_surf = pygame.transform.scale(healthbar, (self.healthbar_one_width * self.health, self.healthbar_height))
        
        
        # self.surface.fill((0, 0, 0))
        # 297
        
        self.surface.blit(self.healthbar_back, (self.healthbar_one_width, 0))
        self.surface.blit(healthbar_surf, (self.healthbar_one_width, 0))
        self.surface.blit(self.healthbar_edge, (0, 0))
        self.surface.blit(self.healthbar_edge, (self.heatlhbar_width - self.healthbar_one_width * 3, 0))
        
        
        
    
    def get_surface(self):
        return self.surface
    
if __name__ == '__main__':
    display = pygame.display.set_mode((1280, 720))
    healthbar1 = HealthBar()
    while True:
        display.fill((255, 255, 255))
        if healthbar1.health > 0:
            print(healthbar1.health)
            healthbar1.health -= 1
        healthbar1.update()
        display.blit(healthbar1.get_surface(), (10, 10))
        
        pygame.display.update()
        time.sleep(0.1)
        