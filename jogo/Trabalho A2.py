import pygame
import random
from pygame.locals import (DOUBLEBUF,
                           FULLSCREEN,
                           KEYDOWN,
                           KEYUP,
                           K_LEFT,
                           K_RIGHT,
                           QUIT,
                           K_ESCAPE, K_UP, K_DOWN, K_RCTRL, K_LCTRL
                           )
from Background import Fundo

class Jogo:
    def __init__(self,size=(800,800),fullscreen= True):
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.run = True
        self.screen_size = self.screen.get_size()
        self.fundo = Fundo()
        pygame.display.set_caption('Trabalho A2')
        flags = DOUBLEBUF

    def eventos(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.run = False

        if event.type in (KEYDOWN, KEYUP):
            key = event.key
            if key == K_ESCAPE:
                self.run = False
                
    def atualiza_elementos(self, dt):
        self.fundo.update(dt) 
        
    def desenha_elementos(self):
        self.fundo.draw(self.screen)

        
    def loop(self):
        clock = pygame.time.Clock() 
        dt = 16
        while self.run:
            clock.tick(1000 / dt)
            self.eventos()
            self.atualiza_elementos(dt)
            self.desenha_elementos()
            pygame.display.flip()

J = Jogo()
J.loop()