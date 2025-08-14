import pygame
from pygame.locals import *
from random import randint

def coord_itens(exclusoes=None):
    if exclusoes is None:
        exclusoes = []

    #normalizar exclusoes para tuplas (x,y)
    exclusoes_tupla = set((e[0], e[1]) for e in exclusoes)

    while True:
        x = randint(30, 770)
        y = randint(40, 490)

        if (x, y) not in exclusoes_tupla:
            return x, y

class Item:
    def __init__(self, cor, exclusoes=None):
        self.cor = cor
        self.maça = pygame.image.load("sprites/Item/apple-pixel-art-png.webp").convert_alpha()
        self.maça = pygame.transform.scale(self.maça, (25, 25))
        self.manga = pygame.image.load("sprites/Item/pngtree-mango-vector-pixel-art-png-image_13730506.png").convert_alpha()
        self.manga = pygame.transform.scale(self.manga, (25, 25))
        self.vida = pygame.image.load("sprites/Item/pngtree-pixel-art-pink-heart-illustration-png-image_11436092.png").convert_alpha()
        self.vida = pygame.transform.scale(self.vida, (25, 25))
        # permite passar exclusoes na criação
        if exclusoes:
            self.x, self.y = coord_itens(exclusoes)
        else:
            self.x, self.y = coord_itens()
    
    def reposicionar(self, exclusoes=None):
        if exclusoes:
            self.x, self.y = coord_itens(exclusoes)
        else:
            self.x, self.y = coord_itens()
    
    def desenhar(self, tela):
        if self.cor == (255, 0, 0):
            tela.blit(self.maça, (self.x, self.y))
        elif self.cor == (255, 255, 0):
            tela.blit(self.manga, (self.x, self.y))
        elif self.cor == (166, 232, 138):
            tela.blit(self.vida, (self.x, self.y))
    
    def colidiu(self, snake):
        cabeca_rect = pygame.Rect(snake.x, snake.y, 20, 20)
        item_rect = pygame.Rect(self.x, self.y, 20, 20)
        return cabeca_rect.colliderect(item_rect)