import pygame

class Tela:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Toshis Coxinha Adventure')
        
        self.window = pygame.display.set_mode((540,720))
        imagem_fundo = pygame.transform.scale(pygame.image.load('assets/imagem_fundo_pygame.jpg'), (540,720))
        imagem_toshi = pygame.transform.scale(pygame.image.load('assets/toshi.png'),(80,100))
        
        self.assets = {
            'imagem_fundo': imagem_fundo,
            'toshi':imagem_toshi,
            't0' : 0,
            'tempo': 0
        }

        self.personagem = Personagem(self.window, [230, 600] , self.assets)
    
    def atualiza_estado(self):
        t1 = pygame.time.get_ticks()
        tempo = t1- self.assets['t0'] if self.assets['t0']>=0 else t1
        self.assets['t0'] = t1
        self.assets['tempo'] = tempo
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.personagem.velocidade[0] -=1
                if event.key == pygame.K_d:
                    self.personagem.velocidade[0] +=1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.personagem.velocidade[0] +=1
                if event.key == pygame.K_d:
                    self.personagem.velocidade[0] -=1

        
        

        self.personagem.update()

        self.personagem.muda_posicao()

        return True

    def desenha(self):
        self.window.blit(self.assets['imagem_fundo'],(0,0))
        self.personagem.desenha()
        pygame.display.update()
        
    def game_loop(self):
        while self.atualiza_estado():
            self.desenha()


class Personagem:
    def __init__(self, window, pos,assets):
        self.vida = 3
        self.velocidade = [0,0]
        self.rect = pygame.Rect(pos[0], pos[1], 80, 100)
        self.window = window
        self.assets = assets
        self
    
    def desenha(self):
        self.window.blit(self.assets['toshi'],(self.rect.x, self.rect.y))
    
    def update(self):
        self.rect.x += self.velocidade[0]*self.assets['tempo']
        self.rect.y += self.velocidade[1]*self.assets['tempo']

    def muda_posicao(self):
        if self.rect.x >= 540:
            self.rect.x = 1
        if self.rect.x <= 0:
            self.rect.x = 530