import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

#Tamanho da Tela:
largura = 640
altura = 480

#Coord. da cobra
x_cobra = int(largura/2) 
y_cobra = int(altura/2)

#Velocidade
velocidade = 10
x_controle = velocidade
y_controle = 0

#Coordenadas inicias dos coletáveis:
x_maca = randint(40, 600)
y_maca = randint(50, 430)

x_manga = randint(40, 600)
y_manga = randint(50, 430)

x_goiaba = randint(40, 600)
y_goiaba = randint(50, 430)

#Contador Frutas
macas, mangas, goiabas = 0, 0, 0

#Definindo a tela e fonte
fonte = pygame.font.SysFont('times new roman', 40, bold=False, italic=False)
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Snake Game IP 2025.1')
relogio = pygame.time.Clock()

#Tamanho inicial da cobra
lista_cobra = []
comprimento_inicial = 5
morreu = False

#Função para aumentar o tamanho da compra
def aumenta_cobra(lista_cobra):
    for XeY in lista_cobra:
        x = XeY[0]
        y = XeY[1]

        pygame.draw.rect(tela, (0,255,0), (x, y, 20, 20))

#Função similiar as instruções iniciais, em caso de morte e reinicio:
def reiniciar_jogo():
    global pontos, comprimento_inicial, x_cobra, y_cobra, lista_cobra, lista_cabeca, x_maca, y_maca, x_manga, y_manga, x_goiaba, y_goiaba, morreu
    comprimento_inicial = 5
    x_cobra = int(largura/2) 
    y_cobra = int(altura/2)
    lista_cobra = []
    lista_cabeca = []

    x_maca = randint(40, 600)
    y_maca = randint(50, 430)

    x_manga = randint(40, 600)
    y_manga = randint(50, 430)

    x_goiaba = randint(40, 600)
    y_goiaba = randint(50, 430)

    morreu = False

#Loop principal do jogo:
while True:
    relogio.tick(30)
    tela.fill((255,255,255))
    
    #Mensagens com os contadores dos coletáveis:
    mensagem = f'Maçãs: {macas}'
    texto_formatado = fonte.render(mensagem, True, (0,0,0))
    mensagem2 = f'Mangas: {mangas}'
    texto_formatado2 = fonte.render(mensagem2, True, (0,0,0))
    mensagem3 = f'Goiaba: {mangas}'
    texto_formatado3 = fonte.render(mensagem3, True, (0,0,0))
    
    #Caso o player feche o jogo:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        #Movimento:
        if event.type == KEYDOWN:
            if event.key == K_a:
                if x_controle == velocidade:
                    pass
                else:
                    x_controle = -velocidade
                    y_controle = 0
            if event.key == K_d:
                if x_controle == -velocidade:
                    pass
                else:
                    x_controle = velocidade
                    y_controle = 0
            if event.key == K_w:
                if y_controle == velocidade:
                    pass
                else:
                    y_controle = -velocidade
                    x_controle = 0
            if event.key == K_s:
                if y_controle == -velocidade:
                    pass
                else:
                    y_controle = velocidade
                    x_controle = 0

    x_cobra = x_cobra + x_controle
    y_cobra = y_cobra + y_controle

    #Desenhando a cobra:   
    cobra = pygame.draw.rect(tela, (0,255,0), (x_cobra,y_cobra,20,20))

    #Desenhando as frutas:
    maca = pygame.draw.rect(tela, (255,0,0), (x_maca,y_maca,20,20))
    manga = pygame.draw.rect(tela, (255,255,0), (x_manga,y_manga,20,20))
    goiaba = pygame.draw.rect(tela, (125,191,121), (x_goiaba,y_goiaba,20,20))
    
    #Se colidiu com a maçã:
    if cobra.colliderect(maca):
        x_maca = randint(40, 600)
        y_maca = randint(50, 430)
        macas += 1
        comprimento_inicial = comprimento_inicial + 1
    
    #Com a manga:
    if cobra.colliderect(manga):
        x_manga = randint(40, 600)
        y_manga = randint(50, 430)
        mangas += 1
        comprimento_inicial = comprimento_inicial - 1
    
    #Com a goiaba:
    if cobra.colliderect(goiaba):
        x_goiaba = randint(40, 600)
        y_goiaba = randint(50, 430)
        goiabas += 1
        comprimento_inicial = comprimento_inicial - 1

    #Verificando o tamanho da cobra e seu aumento:
    lista_cabeca = []
    lista_cabeca.append(x_cobra)
    lista_cabeca.append(y_cobra)
    
    lista_cobra.append(lista_cabeca)

    #Verificando se a cobra tocou nela mesma:
    if lista_cobra.count(lista_cabeca) > 1:
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
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        reiniciar_jogo()

            ret_texto.center = (largura//2, altura//2) 
            tela.blit(texto_formatado, ret_texto)
            pygame.display.update()

    
    if x_cobra > largura:
        x_cobra = 0
    if x_cobra < 0:
        x_cobra = largura
    if y_cobra < 0:
        y_cobra = altura
    if y_cobra > altura:
        y_cobra = 0

    if len(lista_cobra) > comprimento_inicial:
        del lista_cobra[0]

    aumenta_cobra(lista_cobra)

    tela.blit(texto_formatado, (430,40))
    tela.blit(texto_formatado2, (430,70))
    #tela.blit(texto_formatado3, (430,100))

    
    pygame.display.update()
