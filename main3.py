import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()
BASE, HEIGHT = 800, 600
metade = int(BASE/2)
fonte = fonte = pygame.font.SysFont('monospace', 30, bold=True, italic=False)
tela = pygame.display.set_mode((BASE, HEIGHT))
pygame.display.set_caption('Snake Forest')
relogio = pygame.time.Clock()

x_cobra, y_cobra = 0, HEIGHT - 20
velocidade = 5
x_controle, y_controle = velocidade, 0
lista_cobra = []
lista_cabeca = []
comprimento = 5

def aumenta_cobra(lista_cobra):
    for cabeca in lista_cobra:
        x = cabeca[0]
        y = cabeca[1]

        pygame.draw.rect(tela, (0,255,0), (x, y, 20, 20))

def coord_itens():
    x = randint(10, 790)
    while 320 <= x <= 460:
        x = randint(10, 790)
    
    y = randint(20, 580)
    return x, y

def movimento(event, velocidade, x_controle, y_controle):
    if event.type == KEYDOWN:
        if event.key == K_a:
            if x_controle == velocidade:
                pass
            else:
                x_controle, y_controle = -velocidade, 0
        if event.key == K_d:
            if x_controle == -velocidade:
                pass
            else:
                x_controle, y_controle = velocidade, 0
        if event.key == K_w:
                if y_controle == velocidade:
                    pass
                else:
                    x_controle, y_controle = 0, -velocidade  
        if event.key == K_s:
                if y_controle == -velocidade:
                    pass
                else:
                    x_controle, y_controle = 0, velocidade
    
    return x_controle, y_controle 

def reiniciar():
    global comprimento, x_cobra, y_cobra, lista_cobra, lista_cabeca, \
    x_maca, y_maca, x_manga, y_manga, x_rato, y_rato, \
    morreu, macas, mangas, ratos \
    
    morreu = False
    
    comprimento = 5
    x_cobra, y_cobra = 0, HEIGHT - 20
    lista_cobra, lista_cabeca = [], []
    macas, mangas, ratos = 0, 0, 0

    x_maca, y_maca = coord_itens()
    x_manga, y_manga = coord_itens()
    x_rato, y_rato = coord_itens()

x_maca, y_maca = coord_itens()
x_manga, y_manga = coord_itens()
x_rato, y_rato = coord_itens()
x_cacador, y_cacador = 400, 0
macas, mangas, ratos = 0, 0, 0

fonte = pygame.font.SysFont('monospace', 30, bold=True, italic=False)
tela = pygame.display.set_mode((BASE, HEIGHT))
pygame.display.set_caption('Snake Game IP 2025.1')
relogio = pygame.time.Clock()

morreu = False

while True:
    relogio.tick(60)
    tela.fill((37, 102, 20))
    path = pygame.draw.rect(tela, (179,137,46), ((int(BASE/2) - 12),0,60,HEIGHT))

    mensagem = f'Maçãs: {macas}'
    texto_formatado = fonte.render(mensagem, True, (0,0,0))
    mensagem2 = f'Mangas: {mangas}'
    texto_formatado2 = fonte.render(mensagem2, True, (0,0,0))
    mensagem3 = f'Ratos: {ratos}'
    texto_formatado3 = fonte.render(mensagem3, True, (0,0,0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        x_controle, y_controle = movimento(event, velocidade, x_controle, y_controle)
    
    x_cobra += x_controle
    y_cobra += y_controle
    if y_cacador >= HEIGHT:
        y_cacador = 0
    y_cacador += 8

    cabeca_cobra = pygame.draw.rect(tela, ('green'), (x_cobra, y_cobra, 10,10))
    cacador = pygame.draw.rect(tela, ("black"), (int(BASE/2), y_cacador, 30,50))

    maca = pygame.draw.rect(tela, ('red'), (x_maca, y_maca, 20,20))
    manga = pygame.draw.rect(tela, ('yellow'), (x_manga, y_manga, 20,20))
    rato = pygame.draw.rect(tela, ('gray'), (x_rato, y_rato, 20,20))

    for item in [maca, manga, rato]:
        if cabeca_cobra.colliderect(item):
            x, y = coord_itens()
            if item == maca:
                x_maca, y_maca = x, y
                macas += 1
            elif item == manga:
                x_manga, y_manga = x, y
                mangas += 1
            elif item == rato:
                x_rato, y_rato = x, y
                ratos += 1
    
    while cabeca_cobra.colliderect(cacador):
        if ratos > 0:
            morreu = False
            ratos -= 1
        else:
            morreu = True
            break
    
    lista_cabeca = []
    lista_cabeca.append(x_cobra)
    lista_cabeca.append(y_cobra)
    lista_cobra.append(lista_cabeca)

    if lista_cobra.count(lista_cabeca) > 1 or morreu:
        fonte2 = pygame.font.SysFont('arial', 20, True, True)
        mensagem = 'Game over! Pressione a tecla R para jogar novamente'
        texto_formatado = fonte2.render(mensagem, True, (0,0,0))
        ret_texto = texto_formatado.get_rect()

        morreu = True
        while morreu:
            tela.fill((255,255,255))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                #Reiniciando o jogo:
                elif event.type == KEYDOWN:
                    if event.key == K_r:
                        reiniciar()

            ret_texto.center = (BASE//2, HEIGHT//2) 
            tela.blit(texto_formatado, ret_texto)
            pygame.display.update()
    
    if x_cobra > BASE:
        x_cobra = 0
    if x_cobra < 0:
        x_cobra = BASE
    if y_cobra < 0:
        y_cobra = HEIGHT
    if y_cobra > HEIGHT:
        y_cobra = 0
    
    if len(lista_cobra) > comprimento:
        del lista_cobra[0]

    aumenta_cobra(lista_cobra)

    tela.blit(texto_formatado, (600,40))
    tela.blit(texto_formatado2, (600,80))
    tela.blit(texto_formatado3, (600,120))

    pygame.display.update()
