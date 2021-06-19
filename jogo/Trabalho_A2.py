import pygame
import random

from pygame.locals import (DOUBLEBUF,
                           FULLSCREEN,
                           KEYDOWN,
                           KEYUP,
                           K_LEFT,
                           K_RIGHT,
                           QUIT,
                           K_ESCAPE, K_UP, K_DOWN, K_RCTRL, K_LCTRL, K_w,K_a,K_s,K_d
                           )
from Background import Fundo
from Elementos import ElementoSprite

class Jogo:
    def __init__(self,size=(800,800),fullscreen= False):
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

        if event.type == KEYDOWN:
            key = event.key
            if key == K_ESCAPE:
                self.run = False
            elif key == K_UP or key == K_w:
                self.jogador.accel_top()
            elif key == K_DOWN or key == K_s:
                self.jogador.accel_bottom()
            elif key == K_RIGHT or key == K_d:
                self.jogador.accel_right()
            elif key == K_LEFT or key == K_a:
                self.jogador.accel_left()
        if event.type == KEYUP:
            key = event.key
            if key == K_UP or key == K_w:
                self.jogador.accel_bottom()
#                self.jogador.zerar_accel_t()
            elif key == K_DOWN or key == K_s:
                self.jogador.accel_top()
#                self.jogador.zerar_accel_b()
            elif key == K_RIGHT or key == K_d:
                self.jogador.accel_left()
#                self.jogador.zerar_accel_r()
            elif key == K_LEFT or key == K_a:
                self.jogador.accel_right()
#                self.jogador.zerar_accel_l()
                
    def atualiza_elementos(self, dt):
        self.fundo.update(dt) 
        for v in self.elementos.values():
            v.update(dt)
        
    def desenha_elementos(self):
        self.fundo.draw(self.screen)
        for v in self.elementos.values():
            v.draw(self.screen)
        
    def loop(self):
        clock = pygame.time.Clock() 
        dt = 16
        self.jogador = Jogador([100, 400], 5)
        self.elementos['jogador'] = pygame.sprite.RenderPlain(self.jogador)
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
        super().__init__(image, position,[0,0], new_size)
        self.pontos = 0
    def update(self, dt):
        move_speed = (self.speed[0] * dt / 16 , self.speed[1] * dt / 16)
        self.rect = self.rect.move(move_speed)
    def get_pos(self):
        return (self.rect.center[0], self.rect.top)

    def get_pontos(self):
        return self.pontos

    def set_pontos(self, pontos):
        self.pontos = pontos
     
    
    def accel_top(self):
        speed = self.get_speed()
        self.set_speed((speed[0], speed[1] - self.acceleration[1]))

    def accel_bottom(self):
        speed = self.get_speed()
        self.set_speed((speed[0], speed[1] + self.acceleration[1]))

    def accel_left(self):
        speed = self.get_speed()
        self.set_speed((speed[0] - self.acceleration[0], speed[1]))

    def accel_right(self):
        speed = self.get_speed()
        self.set_speed((speed[0] + self.acceleration[0], speed[1]))
    
    def zerar_accel_t(self):
        speed = self.get_speed()
        if speed[1] < 0:
            self.set_speed((speed[0],0))
    def zerar_accel_b(self):
        speed = self.get_speed()
        if speed[1] > 0:
            self.set_speed((speed[0],0))
    def zerar_accel_l(self):
        speed = self.get_speed()
        if speed[0] < 0:
            self.set_speed((0,speed[1]))
    def zerar_accel_r(self):
        speed = self.get_speed()
        if speed[0] > 0:
            self.set_speed((0,speed[1]))




    
J = Jogo()