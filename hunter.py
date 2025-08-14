import pygame
from pygame.locals import *

BASE, HEIGHT = 800, 600

class Hunter:
    def __init__(self, x, vel):
        self.x = x
        self.y = 0
        self.velocidade = vel
        self.hunter = pygame.image.load("sprites/Item/fantasminha.png").convert_alpha()
        self.hunter = pygame.transform.scale(self.hunter, (35, 50))
    
    def atualizar(self):
        self.y += self.velocidade
        if self.y >= 475:
            self.y = 0
    
    def desenhar(self, tela):
        tela.blit(self.hunter, (self.x, self.y))
    
    def colidiu_com_snake(self, snake):
        cacador_rect = pygame.Rect(self.x, self.y, 30, 50)
        for parte in snake.corpo:
            if pygame.Rect(parte[0], parte[1], 20, 20).colliderect(cacador_rect):
                return True
        return False