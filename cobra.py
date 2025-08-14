import pygame
from pygame.locals import *

BASE, HEIGHT = 800, 600

class Snake:
    def __init__(self, VELOCIDADE_INICIAL, cor, nivel):
        self.x = 20
        self.y = 20
        self.velocidade = VELOCIDADE_INICIAL
        self.x_controle = self.velocidade  
        self.y_controle = 0
        self.corpo = []  
        self.tamanho = 5
        self.cor = cor
        self.nivel = nivel
        self.direção = (self.x_controle//self.velocidade, self.y_controle//self.velocidade)
        self.sprites_cabeca = []
        self.sprites_cauda = []
        for i in range(1,5):  
            cabeca = pygame.image.load(f"sprites\cabeças\cabeça_nivel{i}.png").convert_alpha()
            cabeca = pygame.transform.scale(cabeca, (20, 20))
            self.sprites_cabeca.append(cabeca)
            cauda = pygame.image.load(f"sprites\cauda\cauda_nivel{i}.png").convert_alpha()
            cauda = pygame.transform.scale(cauda, (20, 20))
            self.sprites_cauda.append(cauda)

    def mover(self, event):
        if event.type == KEYDOWN:
            #movimento para esquerda
            if event.key in (K_a, K_LEFT) and self.x_controle != self.velocidade:
                self.x_controle, self.y_controle = -self.velocidade, 0
            #movimento para direita
            elif event.key in (K_d, K_RIGHT) and self.x_controle != -self.velocidade:
                self.x_controle, self.y_controle = self.velocidade, 0
            #movimento para cima
            elif event.key in (K_w, K_UP) and self.y_controle != self.velocidade:
                self.x_controle, self.y_controle = 0, -self.velocidade
            #movimento para baixo
            elif event.key in (K_s, K_DOWN) and self.y_controle != -self.velocidade:
                self.x_controle, self.y_controle = 0, self.velocidade
            self.direção = (self.x_controle//self.velocidade, self.y_controle//self.velocidade)
    
    def atualizar(self):
        self.x += self.x_controle
        self.y += self.y_controle
        #permite atravessar as bordas da tela
        if self.x > BASE-10: self.x = 0
        if self.x < 0: self.x = BASE-10
        if self.y < 0: self.y = 500
        if self.y > 500: self.y = 0
        #atualiza a posição do corpo
        cabeca = [self.x, self.y]
        self.corpo.append(cabeca)
        if len(self.corpo) > self.tamanho:
            del self.corpo[0]  #remove a última parte se passar do tamanho

    def desenhar(self, tela):
        for i, parte in enumerate(self.corpo):
            if i == len(self.corpo) - 1:  # cabeça e cauda
                sprite_cabeca = self.sprites_cabeca[self.nivel-1]
                if self.direção == (0,1):
                    sprite_cabeca = pygame.transform.rotate(sprite_cabeca, 0)
                elif self.direção == (0,-1):
                    sprite_cabeca = pygame.transform.rotate(sprite_cabeca, 180)
                elif self.direção == (1,0):
                    sprite_cabeca = pygame.transform.rotate(sprite_cabeca, 90)
                elif self.direção == (-1,0):
                    sprite_cabeca = pygame.transform.rotate(sprite_cabeca, 270)

                tela.blit(sprite_cabeca, (parte[0], parte[1]))
            if i == 0:
                sprite_cauda = self.sprites_cauda[self.nivel-1]
                if self.direção == (0,1):
                    sprite_cauda = pygame.transform.rotate(sprite_cauda, 180)
                elif self.direção == (0,-1):
                    sprite_cauda = pygame.transform.rotate(sprite_cauda, 0)
                elif self.direção == (1,0):
                    sprite_cauda = pygame.transform.rotate(sprite_cauda, 270)
                elif self.direção == (-1,0):
                    sprite_cauda = pygame.transform.rotate(sprite_cauda, 90)

                tela.blit(sprite_cauda, (parte[0], parte[1]))
            elif self.corpo.index(parte) < len(self.corpo)-3:
                pygame.draw.rect(tela, self.cor, (parte[0], parte[1], 20, 20))
    def crescer(self, quantidade=1):
        self.tamanho += quantidade
    def colidiu_com_corpo(self):
        # colisão com ela mesma
        return self.corpo.count([self.x, self.y]) > 1