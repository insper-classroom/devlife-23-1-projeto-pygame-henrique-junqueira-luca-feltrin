import pygame
 
def inicializa():
    pygame.init()

    window = pygame.display.set_mode((540,720))
    pygame.display.set_caption('blablabla')
    imagem_fundo = pygame.transform.scale(pygame.image.load('assets/imagem_fundo_pygame.jpg'), (540,720))
    imagem_toshi = pygame.transform.scale(pygame.image.load('assets/toshi.png'),(80,100))

    assets = {
        'imagem_fundo': imagem_fundo,
        'toshi': imagem_toshi
    }

    return window,assets

def atualiza_estado():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def desenha(window,assets):
    window.blit(assets['imagem_fundo'],(0,0))
    window.blit(assets['toshi'],(270,360))

    pygame.display.update()

def game_loop(window,assets):
    while atualiza_estado():
        desenha(window,assets)