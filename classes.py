import pygame

import random


class Tela:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Toshis Coxinha Adventure')
        
        self.window = pygame.display.set_mode((540,720))
        imagem_toshi = pygame.transform.scale(pygame.image.load('assets/toshi.png').convert_alpha(),(80,100))
        imagem_fundo = pygame.transform.scale(pygame.image.load('assets/imagem_fundo_pygame.jpg'), (540,720))
        botao_info = pygame.transform.scale(pygame.image.load('assets/botao_info.png'),(220,140))
        botao_play = pygame.transform.scale(pygame.image.load('assets/botao_play.png'),(220,140))
        plataforma = pygame.transform.scale(pygame.image.load('assets/plataforma.png'),(80,15))
        espinho = pygame.transform.scale(pygame.image.load('assets/espinho.png'),(540,40))
        seta = pygame.transform.scale(pygame.image.load('assets/seta_pygame.png'),(50,50))
        instru = pygame.transform.scale(pygame.image.load('assets/instru.png'),(270,360))
        teclas = pygame.transform.scale(pygame.image.load('assets/teclas.png'),(270,173))
        chegada = pygame.image.load('assets/chegada.png')

        rect_espinho = pygame.Rect(0,680,540,40)

        fonte = ('fonte/Minecraft.ttf')
        fonte_usa = pygame.font.Font(fonte,20)

        self.state = {
            'tela_inicio':True,
            'tela_jogo':False,
            'tela_gameover': False,
            'desce_tela': False,
            'tela_info': False,
            'desce_tela_num':0,
            'plataformas': [],
            'rect_plataformas':[],
            't0' : 0,
            'tempo': 0,
            'colidiu': False,
            'altura': 0,
            'pulou': True,
            'pulos':0,
            'chegada' :-16200,
            'segundos': 0 ,
            'contador':0 ,
            'espinho' : rect_espinho       
        }

        self.assets = {
            'botao_play':botao_play,
            'rect_play': pygame.Rect(180,400,180,35),
            'rect_info':pygame.Rect(180,465,180,40),
            'rect_seta':pygame.Rect(0,0,50,50),
            'botao_info':botao_info,
            'plataforma':plataforma,
            'imagem_fundo': imagem_fundo,
            'toshi':imagem_toshi,
            'espinho' : espinho,
            'seta':seta,
            'instru':instru,
            'teclas':teclas,
            'chegada':chegada,
            'fonte' : fonte_usa
        }


        with open('plataformas.txt','r') as arquivo:
            linhas = arquivo.readlines()
            for linha in linhas:
                coord = linha.split(',')
                self.state['plataformas'].append(pygame.Rect(int(coord[0]),int(coord[1]),80,15))


        self.personagem = Personagem(self.window, [230, 550] , self.assets, self.state)
        

    def atualiza_estado(self):
        pygame.time.Clock().tick(120)
        t1 = pygame.time.get_ticks()
        tempo = t1- self.state['t0'] if self.state['t0']>=0 else t1
        self.state['t0'] = t1
        self.state['tempo'] = tempo/1000
        
        mouse_pos = pygame.mouse.get_pos()
        if self.personagem.alt != 1000:
            self.state['contador']+=1
            if self.state['contador'] == 70:
                self.state['contador'] = 0
                self.state['segundos'] +=1

        altura1 = self.personagem.rect.y
        if altura1 == self.state['altura'] or self.state['colidiu']:
            pode_pular = True
        else: 
            pode_pular = False
        self.state['altura'] = self.personagem.rect.y

        if self.personagem.rect.y < 225:
            self.state['desce_tela'] = True
        

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.assets['rect_play'].collidepoint(mouse_pos):
                    self.state['tela_inicio'] = False
                    self.state['tela_info'] = False
                    self.state['tela_jogo'] = True

                if self.assets['rect_info'].collidepoint(mouse_pos):
                    self.state['tela_inicio'] = False
                    self.state['tela_jogo'] = False
                    self.state['tela_info'] = True

                if self.assets['rect_seta'].collidepoint(mouse_pos):
                    self.state['tela_inicio'] = True
                    self.state['tela_jogo'] = False
                    self.state['tela_info'] = False

            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.personagem.velocidade -=800
                if event.key == pygame.K_d:
                    self.personagem.velocidade +=800
                if event.key == pygame.K_SPACE and pode_pular:
                    self.state['pulou'] = True
                    self.personagem.gravidade = -15
                    self.state['pulos'] +=1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.personagem.velocidade +=800
                if event.key == pygame.K_d:
                    self.personagem.velocidade -=800
                
        if self.state['desce_tela']:
            for coord in self.state['plataformas']:
                coord.y += 3
            self.state['chegada'] += 3
            

        self.personagem.update()

        rect_chegada = pygame.Rect(0,self.state['chegada'],540,50)

        test = False
        for plataforma in self.state['plataformas']:
            if plataforma.y >=700:
                self.state['plataformas'].remove(plataforma)
            if plataforma.top <= self.personagem.rect.bottom:
                if plataforma.colliderect(self.personagem.rect):
                    if self.personagem.alt < plataforma.y - 100 :
                        self.state['colidiu'] = True
                        test = True
                        self.personagem.rect.bottom = plataforma.top+4
        if (not test):
            self.state['colidiu'] = False

        # if rect_chegada.colliderect(self.personagem.rect):

        if self.state['espinho'].colliderect(self.personagem.rect):
            self.personagem.rect.bottom = self.state['espinho'].y +20

        print(self.state['segundos'])
       
        self.personagem.muda_posicao()
        

        return True

    def desenha(self):
        if self.state['tela_inicio']:
            self.window.blit(self.assets['imagem_fundo'],(0,0))
            self.window.blit(self.assets['botao_play'],(180,350))
            self.window.blit(self.assets['botao_info'],(180,420))

            pygame.display.update()

        if self.state['tela_info']:
            self.window.blit(self.assets['imagem_fundo'],(0,0))
            self.window.blit(self.assets['seta'],(0,0))
            self.window.blit(self.assets['instru'],(135,60))
            self.window.blit(self.assets['teclas'],(135,330))

            pygame.display.update()

        if self.state['tela_jogo']:
            self.window.blit(self.assets['imagem_fundo'],(0,0))
            self.window.blit(self.assets['espinho'],(0,680))
            img = self.assets['fonte'].render(f'Tempo total: {self.state["segundos"]}' , True , (0,0,0))

            for coord in self.state['plataformas']:
                plat = Plataformas(self.window,80,15,coord.x,coord.y, self.assets)
                plat.desenha_plataformas()

            chegada = Chegada(self.window,540,50,0,self.state['chegada'],self.assets,self.state)
            chegada.desenha_chegada()
            self.window.blit(img,(10,50))
            
            

            self.personagem.desenha()
            pygame.display.update()

    def game_loop(self):
        while self.atualiza_estado():
            self.desenha()


class Personagem:
    def __init__(self, window, pos, assets, state):
        self.vida = 3
        self.rect = pygame.Rect(pos[0], pos[1], 80, 100)
        self.velocidade = 0
        self.window = window
        self.state = state
        self.gravidade = 0
        self.alt = 1000
        self.assets = assets
        self.colidiu = state['colidiu']

    def desenha(self):
        self.window.blit(self.assets['toshi'],(self.rect.x,self.rect.y ))
    
    def update(self):
        if self.colidiu:
            self.gravidade = 0
        else:
            self.gravidade+=0.8
        
        self.rect.y += self.gravidade

        if self.gravidade <= 0:
            self.alt = self.rect.y
        self.rect.x += self.velocidade*self.state['tempo']

    def muda_posicao(self):
        if self.rect.x >= 540:
            self.rect.x = 1
        if self.rect.x <= 0:
            self.rect.x = 530
        if self.state['pulos'] == 0:
            if self.rect.x>= 230 and self.rect.x<= 310:
                if self.rect.y >= 570:
                    self.gravidade = 0
        if self.state['colidiu']:
            self.gravidade = 0
            



class Plataformas:
    def __init__(self,window,width,height,coord_x,coord_y, assets):
        self.window = window
        self.width = width
        self.height = height
        self.x = coord_x
        self.y = coord_y
        self.assets = assets
        

    def desenha_plataformas(self):
        self.window.blit(self.assets['plataforma'],(self.x,self.y))


class Chegada:
    def __init__(self,window,width,height,coord_x,coord_y,assets,state):
        self.window = window
        self.width = width
        self.height = height
        self.x = coord_x
        self.y = coord_y
        self.assets = assets
        self.state = state
        

    def desenha_chegada(self):
        self.window.blit(self.assets['chegada'],(self.x,self.y))

