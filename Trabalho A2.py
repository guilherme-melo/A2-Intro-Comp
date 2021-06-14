import pygame
import random

class Jogo:
    def __init__(self,size=(800,800),fullscreen= True):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.run = True
        self.screen_size = self.screen.get_size()
    def loop(self):
        clock = pygame.time.Clock() 
        dt = 16
        while self.run:
            clock.tick(1000 / dt)
            pygame.display.flip()
            
            
J = Jogo()
J.loop()