import pygame
from sys import exit
import random

pygame.init()

def desenharCobra(tela, block_size, cobra):
    for coordenada in cobra:
        pygame.draw.rect(tela, (0,0,255), (coordenada[0], coordenada[1], block_size, block_size))

comprimento_tela = 640
altura_tela = 480
block_size = 20
velocidade = 6
relogio = pygame.time.Clock()
direction = {"UP":(0,-1),"DOWN":(0,1),"RIGHT":(1,0),"LEFT":(-1,0)}
move = (0,0)
new_move = (0,0)
condicao = True
timing = 0

x_cobra = 320
y_cobra = 240
x_aux = (x_cobra//block_size)
y_aux = (y_cobra//block_size)
cobra = [(x_cobra,y_cobra)]
cont_cobra = 0

x_vermelho = random.randrange(0, comprimento_tela, block_size)
y_vermelho = random.randrange(0, altura_tela, block_size)

x_amarelo = random.randrange(0, comprimento_tela, block_size)
y_amarelo = random.randrange(0, altura_tela, block_size)
cont_amarelo = 0

tela = pygame.display.set_mode((comprimento_tela,altura_tela))

while True:
    timing+=1
    cont_cobra-=1
    if cont_cobra < 0:
        cont_cobra = 0
    
    cont_amarelo-=1
    if cont_amarelo < 0:
        cont_amarelo = 0

    relogio.tick(40)
    tela.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and condicao:
            if pygame.key.get_pressed()[pygame.K_w]:
                if move != direction["DOWN"] and move != direction["UP"]:
                    new_move = direction["UP"]
                    condicao = False
            elif pygame.key.get_pressed()[pygame.K_d]:
                if move != direction["LEFT"] and move != direction["RIGHT"]:
                    new_move = direction["RIGHT"]
                    condicao = False
            elif pygame.key.get_pressed()[pygame.K_s]:
                if move != direction["UP"] and move != direction["DOWN"]:
                    new_move = direction["DOWN"]
                    condicao = False
            elif pygame.key.get_pressed()[pygame.K_a]:
                if move != direction["RIGHT"] and move != direction["LEFT"]:
                    new_move = direction["LEFT"]
                    condicao = False
    
    if abs(x_cobra - x_aux*block_size) < velocidade and abs(y_cobra - y_aux*block_size) < velocidade:

        x_cobra = x_aux*block_size
        y_cobra = y_aux*block_size
        x_aux = (x_cobra//block_size)+new_move[0]
        y_aux = (y_cobra//block_size)+new_move[1]
        move = new_move
        condicao = True

    x_cobra += move[0]*velocidade
    y_cobra += move[1]*velocidade
    if x_cobra > comprimento_tela:
        x_cobra = -block_size
        x_aux = (x_cobra//block_size)+1
    if y_cobra > altura_tela:
        y_cobra = -block_size
        y_aux = (y_cobra//block_size)+1
    if x_cobra < -block_size:
        x_cobra = comprimento_tela
        x_aux = (x_cobra//block_size)-1
    if y_cobra < -block_size:
        y_cobra = altura_tela
        y_aux = (y_cobra//block_size)-1
    
    for i in range(velocidade+1):
        cobra.append((x_cobra+(-i*move[0]),y_cobra+(-i*move[1])))
        if cont_cobra == 0:
            cobra.pop(0)

    if cobra.count((x_cobra,y_cobra)) > 1:
        break

    ret = pygame.draw.rect(tela, (0,0,255), (x_cobra, y_cobra, block_size, block_size))
    ret_vermelho = pygame.draw.rect(tela, (255,0,0), (x_vermelho, y_vermelho, block_size, block_size))
    if timing%200 == 0:
        cont_amarelo+=50
    if cont_amarelo > 0:
        ret_amarelo = pygame.draw.rect(tela, (255,255,0), (x_amarelo, y_amarelo, block_size, block_size))
        if ret.colliderect(ret_amarelo):
            break
    else:
        x_amarelo = random.randrange(0, comprimento_tela, block_size)
        y_amarelo = random.randrange(0, altura_tela, block_size)

    desenharCobra(tela, block_size, cobra)

    if ret.colliderect(ret_vermelho):
        cont_cobra += 10
        x_vermelho = random.randrange(0, comprimento_tela, block_size)
        y_vermelho = random.randrange(0, altura_tela, block_size)

    pygame.display.flip()