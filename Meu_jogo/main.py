import pygame
from pygame.locals import (KEYDOWN,
                           KEYUP,
                           K_LEFT,
                           K_RIGHT,
                           QUIT,
                           K_ESCAPE
                           )
from fundo import Fundo
from elementos import ElementoSprite
import random as rd


class Jogo:
    def __init__(self, size=(823,759)):
        self.elementos={}
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.fundo = Fundo()
        self.screen_size = self.screen.get_size()
        pygame.mouse.set_visible(0)
        self.run = True
        self.gap=150
        self.abertura=100
        
    def atualiza_elementos(self, dt):
        self.fundo.update(dt)
        for v in self.elementos.values():
            v.update(dt)
        
    def trata_eventos(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.run = False

        if event.type==KEYDOWN:
            key = event.key
            if key == K_ESCAPE:
                self.run = False
            if key == K_RIGHT:
                self.jogador.speed_right(3)
            if key == K_LEFT:
                self.jogador.speed_left(3)
                
        if event.type==KEYUP:
            key = event.key
            if key == K_RIGHT:
                self.jogador.speed_right(0)
            if key == K_LEFT:
                self.jogador.speed_left(0)
                
    def desenha_elementos(self):
        self.fundo.draw(self.screen)
        for v in self.elementos.values():
            v.draw(self.screen)
            
    def loop(self):
        clock = pygame.time.Clock()
        dt = 16
        
        contador=0
        
        turnos=(self.screen_size[1]-(self.screen_size[1]%self.gap))/self.gap + 1
        turnos = int(turnos)
        
        auxiliar = 2*(self.screen_size[0]-self.abertura)
             
        r = rd.randint(0, auxiliar)
                        
        self.jogador=Bola([self.screen_size[0]/2, 20])
        self.elementos['jogador'] = pygame.sprite.RenderPlain(self.jogador)
        
        self.elementos['plataformas'] = pygame.sprite.RenderPlain(Plataforma([0, self.screen_size[1]], new_size=[r,10]))
        self.elementos['plataformas'].add(pygame.sprite.RenderPlain(Plataforma([self.screen_size[0], self.screen_size[1]], new_size=[auxiliar-r,10])))
            
            
        while self.run:
            clock.tick(1000 / dt)
            
            contador+=1
            
            if contador==self.gap:
                r = rd.randint(0, auxiliar)
                self.elementos['plataformas'].add(pygame.sprite.RenderPlain(Plataforma([0, self.screen_size[1]], new_size=[r,10])))
                self.elementos['plataformas'].add(pygame.sprite.RenderPlain(Plataforma([self.screen_size[0], self.screen_size[1]], new_size=[auxiliar-r,10])))
                contador=0
            

            self.trata_eventos()

            # Atualiza Elementos
            self.atualiza_elementos(dt)

            # Desenhe no back buffer
            self.desenha_elementos()
            pygame.display.flip()
            

class Bola(ElementoSprite):
    def __init__(self, position, speed=[0,1], image='virus.png', new_size=[20,20]):
        super().__init__(image, position, speed, new_size)
        self.position = position
        
    def speed_up(self, value):
        speed = self.get_speed()
        self.set_speed((speed[0], -value))

    def speed_down(self, value):
        speed = self.get_speed()
        self.set_speed((speed[0], value))

    def speed_left(self, value):
        speed = self.get_speed()
        self.set_speed((-value, speed[1]))

    def speed_right(self, value):
        speed = self.get_speed()
        self.set_speed((value, speed[1]))
        
    def update(self, dt):
        move_speed = (self.speed[0] * dt / 16,
                      self.speed[1] * dt / 16)
        self.rect = self.rect.move(move_speed)

        if (self.rect.right > self.area.right):
            self.rect.right = self.area.right

        elif (self.rect.left < 0):
            self.rect.left = 0

        if (self.rect.bottom > self.area.bottom):
            self.rect.bottom = self.area.bottom

        elif (self.rect.top < 0):
            self.rect.top = 0
        
class Plataforma(ElementoSprite):
    def __init__(self, position, speed=[0,-1], image='vermelho.png', new_size=[500,10]):
        super().__init__(image, position, speed, new_size)


if __name__ == '__main__':
    J = Jogo()
    J.loop()








        
