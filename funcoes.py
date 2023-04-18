import pygame

class Tela:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Jump Toshi')
        
        self.window = pygame.display.set_mode((540,720))
        imagem_fundo = pygame.transform.scale(pygame.image.load('assets/imagem_fundo_pygame.jpg'), (540,720))
        imagem_toshi = pygame.transform.scale(pygame.image.load('assets/toshi.png'),(80,100))
        
        self.assets = {
            'imagem_fundo': imagem_fundo,
            'toshi':imagem_toshi
        }
        
    def atualiza_estado():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def desenha(self):
        self.window.blit(self.assets['imagem_fundo'],(0,0))
        self.window.blit(self.assets['toshi'],(270,360))

        pygame.display.update()

    def game_loop(self):
        while Tela.atualiza_estado():
            Tela.desenha(self)

