import pygame

import random


class Tela:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Toshis Coxinha Adventure')
        
        self.window = pygame.display.set_mode((540,720))
        imagem_fundo = pygame.transform.scale(pygame.image.load('assets/imagem_fundo_pygame.jpg'), (540,720))
        imagem_toshi = pygame.transform.scale(pygame.image.load('assets/toshi.png').convert_alpha(),(80,100))
        botao_play = pygame.transform.scale(pygame.image.load('assets/botao_play.png'),(220,140))
        botao_info = pygame.transform.scale(pygame.image.load('assets/botao_info.png'),(220,140))
        plataforma = pygame.transform.scale(pygame.image.load('assets/plataforma.png'),(80,20))

        self.state = {
            'tela_inicio':True,
            'tela_jogo':False,
            'tela_gameover': False,
            'desce_tela': False,
            'desce_tela_num':0,
            'plataformas': [],
            'rect_plataformas':[]

        }

        self.assets = {
            'botao_play':botao_play,
            'rect_play': pygame.Rect(180,360,220,100),
            'botao_info':botao_info,
            'plataforma':plataforma,
            'imagem_fundo': imagem_fundo,
            'toshi':imagem_toshi,
            't0' : 0,
            'tempo': 0,
            'gravidade': 1,
            'pulando': False
        }

        with open('plataformas.txt','r') as arquivo:
            linhas = arquivo.readlines()
            for linha in linhas:
                coord = linha.split(',')
                self.state['plataformas'].append(pygame.Rect(int(coord[0]),int(coord[1]),80,15))

        self.personagem = Personagem(self.window, [230, 400] , self.assets)
    
    def atualiza_estado(self):
        pygame.time.Clock().tick(120)
        t1 = pygame.time.get_ticks()
        tempo = t1- self.assets['t0'] if self.assets['t0']>=0 else t1
        self.assets['t0'] = t1
        self.assets['tempo'] = tempo/1000
        
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.assets['rect_play'].collidepoint(mouse_pos):
                    self.state['tela_inicio'] = False
                    self.state['tela_jogo'] = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.personagem.velocidade[0] -=1000
                if event.key == pygame.K_d:
                    self.personagem.velocidade[0] +=1000
                if event.key == pygame.K_SPACE:
                    self.assets['pulando'] = True
                if event.key == pygame.K_w:
                    self.state['desce_tela'] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.personagem.velocidade[0] +=1000
                if event.key == pygame.K_d:
                    self.personagem.velocidade[0] -=1000
                if event.key == pygame.K_w:
                    self.state['desce_tela'] = False
            if event.type == pygame.QUIT:
                return False
       
        if self.assets['pulando']:
            self.personagem.rect.y -= self.personagem.y_vel
            self.personagem.y_vel -= self.assets['gravidade']
            if self.personagem.y_vel < -self.personagem.jump_alt:
                self.assets['pulando'] = False
                self.personagem.y_vel = self.personagem.jump_alt


        if self.state['desce_tela']:
            for coord in self.state['plataformas']:
                coord.y+=4

        self.personagem.update()
        
        for plataforma in self.state['plataformas']:
            if plataforma.colliderect(self.personagem.rect):
                print("oi")

        self.personagem.muda_posicao()

        return True

    def desenha(self):
        if self.state['tela_inicio']:
            self.window.blit(self.assets['imagem_fundo'],(0,0))
            self.window.blit(self.assets['botao_play'],(180,350))
            self.window.blit(self.assets['botao_info'],(180,420))

            pygame.display.update()

        if self.state['tela_jogo']:
            self.window.blit(self.assets['imagem_fundo'],(0,0))

            for coord in self.state['plataformas']:
                plat = Plataformas(self.window,80,15,coord.x,coord.y)
                plat.desenha_plataformas()
 
            self.personagem.desenha()
            pygame.display.update()
        
    def game_loop(self):
        while self.atualiza_estado():
            self.desenha()


class Personagem:
    def __init__(self, window, pos,assets):
        self.vida = 3
        self.jump_alt = 20
        self.y_vel = self.jump_alt
        self.velocidade = [0,self.y_vel]
        self.rect = pygame.Rect(pos[0], pos[1], 80, 100)
        self.window = window
        self.assets = assets


    def desenha(self):
        self.rect.y += self.assets['gravidade']
        self.window.blit(self.assets['toshi'],(self.rect.x,self.rect.y ))
    
    def update(self):
        self.rect.x += self.velocidade[0]*self.assets['tempo']

    def muda_posicao(self):
        if self.rect.x >= 540:
            self.rect.x = 1
        if self.rect.x <= 0:
            self.rect.x = 530
        if self.rect.y >= 600:
            self.rect.y = 599

class Plataformas:
    def __init__(self,window,width,height,coord_x,coord_y):
        self.window = window
        self.width = width
        self.height = height
        self.x = coord_x
        self.y = coord_y
        

    def desenha_plataformas(self):
        plataforma = pygame.transform.scale(pygame.image.load('assets/plataforma.png'),(self.width,self.height))
        self.window.blit(plataforma,(self.x,self.y))
  