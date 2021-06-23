import pygame
from pygame.locals import (KEYDOWN,
                           KEYUP,
                           K_LEFT,
                           K_RIGHT,
                           QUIT,
                           K_ESCAPE,K_a,K_d,K_p,K_w
                           )
from Background import Fundo
from Elementos import ElementoSprite
import random as rd



class Jogo:
    def __init__(self, size=(823,759)):
        self.elementos={}
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.fundo = Fundo()
        self.screen_size = self.screen.get_size()
        pygame.mouse.set_visible(1)
        self.run = True
        self.pontos= 0
        self.multiplicador = 1
        pygame.font.init()
        self.fonte = pygame.font.Font(None, 70)
        pygame.mixer.music.load('sons/musica.wav')
        """Deixamos um agradecimento especial ao nosso amigo Matheus Fonseca, que gravou a trilha sonora do jogo no piano."""
        pygame.mixer.music.play(-1)
        #Distância vertical entre as barreiras
        self.gap=150
        self.jogar_novamente = False
        
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
            sp = i.get_speed()

            #Se tiver contato bolinha começa a subir
            if i in hitted:
                pygame.mixer.init()
                colisao = pygame.mixer.Sound('sons/colision.wav')
                colisao.play()
                self.multiplicador = 1
                b=hitted[i][0]
                sb=b.get_speed()
                #Condições pra não ficar grudado
                if (i.rect.bottom <= b.rect.top + 3):                    
                    i.speed_up(self.velocidade_padrão[1]-sb[1]+2)
                elif i.rect.bottom==self.screen_size[1]:
                    i.speed_up(self.velocidade_padrão[1]-sb[1]+2)
                    i.rect.bottom = b.rect.top+1
                    
                #Aqui corrige o bug de atravessar pela lateral, porém tira o efeito do seta
                elif (i.rect.right >= b.rect.left) or (i.rect.left<=b.rect.right):
                    i.speed_left(sp[0]+1)
            
            #Faz a bola voltar a cair
            elif sp[1] < 1:
                i.speed_down(self.velocidade_padrão[1])
  

    def escreve_placar(self):
        score = self.fonte.render(f'Score: {self.pontos}', True, (20, 130, 50))
        self.screen.blit(score, (self.screen_size[0] - 300, 30))
        pygame.display.update()
        
    def trata_eventos(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type==KEYDOWN:
            key = event.key
            if key == K_ESCAPE:
                pygame.quit()
            if key == K_RIGHT or key == K_d:
                self.jogador.speed_right(3)
            if key == K_LEFT or key == K_a:
                self.jogador.speed_left(3)
            if key == pygame.K_p:
                Jogo.pause(self)
                
    def pause(self):
    
        self.screen = pygame.display.set_mode((823, 759))
        pygame.font.init()
        self.font1 = pygame.font.Font(None, 70)
        self.font2 = pygame.font.Font(None, 50)
    
        self.screen_text_1 = self.font1.render('JOGO PAUSADO!', True, (255, 255, 255),(0,0,0))
        self.screen_text_2 = self.font2.render('P para DESPAUSAR', True, (0,0,0))
        self.screen_text_3 = self.font2.render('S para SAIR', True, (0,0,0))
    
        self.pause = True    

        while self.pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause = False
            
                    elif event.key == pygame.K_s:
                        pygame.quit()  
            
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.screen_text_1, [210, 200])
            self.screen.blit(self.screen_text_2, [250, 400])
            self.screen.blit(self.screen_text_3, [300, 450])
            pygame.display.flip()
              
    def desenha_elementos(self):
        self.fundo.draw(self.screen)
        for v in self.elementos.values():
            v.draw(self.screen)
            
    def loop(self):
        clock = pygame.time.Clock()
        dt = 16        
        contadores=[0,0,0,0]
        auxiliar = 2*(self.screen_size[0]-self.abertura)
        
        #Randomiza a posição do buraco
        r = rd.randint(0, auxiliar)
        
        #Cria a bola                
        self.jogador=Bola([self.screen_size[0]/2, 400], speed= self.velocidade_padrão)
        self.elementos['jogador'] = pygame.sprite.RenderPlain(self.jogador)
        
        #Cria as primeiras plataformas (esquerda e direita)
        self.elementos['plataformas'] = pygame.sprite.RenderPlain(Plataforma([0, self.screen_size[1]], new_size=[r,10],speed = [0,-2]))
        self.elementos['plataformas'].add(pygame.sprite.RenderPlain(Plataforma([self.screen_size[0], self.screen_size[1]], new_size=[auxiliar-r,10],speed = [0,-2])))
            
            
        while self.jogador.morto == False:
            clock.tick(1000 / dt)
            contadores[:]=[i+1 for i in contadores]
            if contadores[0]==self.gap:
                #Cria as outra plataformas
                r = rd.randint(0, auxiliar)
                a=[0,0,0,-2,2][rd.randint(0, 4)]
                self.elementos['plataformas'].add(pygame.sprite.RenderPlain(Plataforma([0, self.screen_size[1]], new_size=[r,10],speed = [a,-2])))
                self.elementos['plataformas'].add(pygame.sprite.RenderPlain(Plataforma([self.screen_size[0], self.screen_size[1]], new_size=[auxiliar-r,10], speed=[a,-2])))
                contadores[0]=0
            if contadores[3] == 80:
                for elementos in self.elementos['plataformas']:
                    a = elementos.get_speed()
                    elementos.set_speed((-a[0],a[1]))
                    contadores[3] = 0
                
            if contadores[1] == 5:
                spd = self.jogador.get_speed()
                if spd[0] < 0: 
                    if self.jogador.index_lista == 0:
                        self.jogador.index_lista = 8
                    else:
                        self.jogador.index_lista -=1
                if spd[0] > 0: 
                    if self.jogador.index_lista == 8:
                        self.jogador.index_lista = 0
                    else:
                        self.jogador.index_lista +=1
                self.jogador.image = self.jogador.sprite_lista[self.jogador.index_lista]
                contadores[1]=0
            turnos=(self.screen_size[1]-(self.screen_size[1]%self.gap))/self.gap + 1
            turnos = int(turnos)
            
            if contadores[2] == self.gap:
                self.multiplicador += 5
                contadores[2] = 0
                
            self.pontos += self.multiplicador  


            self.trata_eventos()
            self.contato(self.elementos['jogador'], self.elementos['plataformas'])

            # Atualiza Elementos
            self.atualiza_elementos(dt)

            # Desenhe no back buffer
            self.desenha_elementos()
            self.escreve_placar()
            pygame.display.flip()
            if self.jogador.morto:
                self.run=False
        self.pontos = 0
class Bola(ElementoSprite):
    def __init__(self, position, speed, image='bola_spritesheet.png', new_size=[40,40]):
        super().__init__(image, position, speed, new_size)
        self.position = position
        self.morto = False
    def get_speed(self):
        return self.speed
        
    def speed_up(self, value):
        speed = self.get_speed()
        self.set_speed((speed[0], speed[1]  - value))

    def speed_down(self, value):
        speed = self.get_speed()
        self.set_speed((speed[0], speed[1] + value))

    def speed_left(self, value):
        speed = self.get_speed()
        self.set_speed((speed[0] - value, speed[1]))

    def speed_right(self, value):
        speed = self.get_speed()
        self.set_speed((speed[0]+ value, speed[1]))
        
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
    def __init__(self, position, speed = [0,-2], image='grama.png', new_size=[500,10]):
        super().__init__(image, position, speed, new_size)

    def get_speed(self):
        return self.speed
        
J = Jogo()











        
