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
        
        #Distância vertical entre as barreiras
        self.gap=150
        
        #Tamanho do buraco entre as barreiras (horizontal)
        self.abertura=100
        
        #Velocidade padrão da bolinha
        self.velocidade_padrão=[0,1]
        
    def atualiza_elementos(self, dt):
        self.fundo.update(dt)
        for v in self.elementos.values():
            v.update(dt)
            
    def contato(self, jogador, barreira):
        hitted = pygame.sprite.groupcollide(jogador, barreira, 0, 0)
        for i in jogador:  
            
            #Se tiver contato bolinha começa a subir
            if i in hitted:   
                b=hitted[i][0]
                sb=b.get_speed()
                
                #Condições pra não ficar grudado
                if (i.rect.bottom <= b.rect.top + 2):                    
                    i.speed_down(sb[1])
                elif i.rect.bottom==self.screen_size[1]:
                    i.speed_down(sb[1])
                    i.rect.bottom = b.rect.top+1
                    
                #Aqui corrige o bug de atravessar pela lateral, porém tira o efeito do seta
                elif (i.rect.right >= b.rect.left) or (i.rect.left<=b.rect.right):
                    i.speed_left(0)
            
            #Faz a bola voltar a cair
            else:
                i.speed_down(self.velocidade_padrão[1])
  
        
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
        
        #Randomiza a posição do buraco
        r = rd.randint(0, auxiliar)
        
        #Cria a bola                
        self.jogador=Bola([self.screen_size[0]/2, 20], speed= self.velocidade_padrão)
        self.elementos['jogador'] = pygame.sprite.RenderPlain(self.jogador)
        
        #Cria as primeiras plataformas (esquerda e direita)
        self.elementos['plataformas'] = pygame.sprite.RenderPlain(Plataforma([0, self.screen_size[1]], new_size=[r,10]))
        self.elementos['plataformas'].add(pygame.sprite.RenderPlain(Plataforma([self.screen_size[0], self.screen_size[1]], new_size=[auxiliar-r,10])))
            
            
        while self.run:
            clock.tick(1000 / dt)
            
            contador+=1
            
            if contador==self.gap:
                #Cria as outra plataformas
                r = rd.randint(0, auxiliar)
                self.elementos['plataformas'].add(pygame.sprite.RenderPlain(Plataforma([0, self.screen_size[1]], new_size=[r,10])))
                self.elementos['plataformas'].add(pygame.sprite.RenderPlain(Plataforma([self.screen_size[0], self.screen_size[1]], new_size=[auxiliar-r,10])))
                contador=0
            

            self.trata_eventos()
            self.contato(self.elementos['jogador'], self.elementos['plataformas'])

            # Atualiza Elementos
            self.atualiza_elementos(dt)

            # Desenhe no back buffer
            self.desenha_elementos()
            pygame.display.flip()
            
            if self.jogador.morto:
                self.run=False
            

class Bola(ElementoSprite):
    def __init__(self, position, speed, image='virus.png', new_size=[20,20]):
        super().__init__(image, position, speed, new_size)
        self.position = position
        self.morto = False
        
    def get_speed(self):
        return self.speed
        
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
            self.morto = True
        
class Plataforma(ElementoSprite):
    def __init__(self, position, speed=[0,-1], image='vermelho.png', new_size=[500,10]):
        super().__init__(image, position, speed, new_size)
        
    def get_speed(self):
        return self.speed


if __name__ == '__main__':
    J = Jogo()
    J.loop()








        
