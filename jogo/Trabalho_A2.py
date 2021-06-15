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
from Elementos import ElementoSprite

class Jogo:
    def __init__(self,size=(600,600),fullscreen= True):
        pygame.init()
        self.elementos = {}
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
        self.jogador.draw(self.screen)

        
    def loop(self):
        clock = pygame.time.Clock() 
        dt = 16
        self.jogador = pygame.sprite.Group(Jogador([200, 400], 5))
        while self.run:
            clock.tick(1000 / dt)
            self.eventos()
            self.atualiza_elementos(dt)
            self.desenha_elementos()
            pygame.display.flip()

class Jogador(ElementoSprite):
    def __init__(self, position, speed=[0, 0], image=None, new_size=[100, 100]):
        self.acceleration = [3, 3]
        if not image:
            image = "bola_spritesheet.png"
        super().__init__(image, position, speed, new_size)




"""class Jogador(ElementoSprite):
    def __init__(self, position, speed=[0, 0], image=None, new_size=[715, 715]):
        self.acceleration = [3, 3]
        self.image = image
        if not image:
            image = "bola_spritesheet.png"
        self.imagens_bola = []
        for i in range(3):
            for j in range(3):
                img = self.image.subsurface((i*715,j*715),(715,715))
                self.imagens_bola.append(img)
        self.index_bola = 0
        self.sprite = self.imagens_bola[self.index_bola]
        super().__init__(image, position, speed, new_size)"""


    
J = Jogo()
J.loop()