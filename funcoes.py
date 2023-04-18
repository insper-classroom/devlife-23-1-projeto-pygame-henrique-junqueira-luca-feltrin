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
            'toshi':imagem_toshi
        }

        self.personagem = Personagem(self.window, [100, 100] , self.assets)
    
    def atualiza_estado(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                self.personagem.velocidade[0] +=10


        self.personagem.update()
        
        return True

    def desenha(self):
        self.window.blit(self.assets['imagem_fundo'],(0,0))
        self.personagem.desenha()
        pygame.display.update()
        
    def game_loop(self):
        while self.atualiza_estado():
            self.desenha()


# toshi = Tela()

class Personagem:
    def __init__(self, window, pos,assets):
        self.vida = 3
        self.velocidade = [0,0]
        self.rect = pygame.Rect(pos[0], pos[1], 80, 100)
        self.window = window
        self.assets = assets

    
    def desenha(self):
        self.window.blit(self.assets['toshi'],(self.rect.x, self.rect.y))
    
    def update(self):
        self.rect.x += self.velocidade[0]
        self.rect.y += self.velocidade[1]
