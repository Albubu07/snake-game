import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()  

# =================== CONFIGURAÇÕES GLOBAIS ===================
BASE, HEIGHT = 800, 600 
VELOCIDADE_INICIAL = 5   
ITENS_PARA_VENCER = 10   
TEMPO_INICIAL = 60       #tempo inicial do jogo (segundos)

# =================== FUNÇÕES ÚTEIS ===================
def coord_itens(exclusoes=None):
    
    if exclusoes is None:
        exclusoes = []

    #normalizar exclusoes para tuplas (x,y)
    exclusoes_tupla = set((e[0], e[1]) for e in exclusoes)

    while True:
        x = randint(10, 790)
        #evita spawn na faixa central (onde o caçador se move)
        while 320 <= x <= 460:
            x = randint(10, 790)
        y = randint(20, 580)

        if (x, y) not in exclusoes_tupla:
            return x, y

def hora_str(hora):
    
    min, sec = divmod(hora, 60)
    return '{:02}:{:02}'.format(min, sec)
# =================== CLASSES ===================
"""classe da cobra."""
class Snake:
    
    def __init__(self):
        self.x = 10
        self.y = HEIGHT - 50
        self.velocidade = VELOCIDADE_INICIAL
        self.x_controle = self.velocidade  
        self.y_controle = 0
        self.corpo = []  
        self.tamanho = 5 

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
    def atualizar(self):
        self.x += self.x_controle
        self.y += self.y_controle
        #permite atravessar as bordas da tela
        if self.x > BASE: self.x = 0
        if self.x < 0: self.x = BASE
        if self.y < 0: self.y = HEIGHT
        if self.y > HEIGHT: self.y = 0
        #atualiza a posição do corpo
        cabeca = [self.x, self.y]
        self.corpo.append(cabeca)
        if len(self.corpo) > self.tamanho:
            del self.corpo[0]  #remove a última parte se passar do tamanho

    def desenhar(self, tela):
        for parte in self.corpo:
            pygame.draw.rect(tela, (0, 255, 0), (parte[0], parte[1], 20, 20))
    def crescer(self, quantidade=2):
        self.tamanho += quantidade
    def colidiu_com_corpo(self):
        """colisão com ela mesma"""
        return self.corpo.count([self.x, self.y]) > 1
    """Classe para os itens a serem coletados(maçã, manga e rato)"""
class Item:
    def __init__(self, cor, exclusoes=None):
        self.cor = cor
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
        pygame.draw.rect(tela, self.cor, (self.x, self.y, 20, 20))
    def colidiu(self, snake):
        cabeca_rect = pygame.Rect(snake.x, snake.y, 20, 20)
        item_rect = pygame.Rect(self.x, self.y, 20, 20)
        return cabeca_rect.colliderect(item_rect)
    """classe que representa o caçador"""
class Hunter:
    def __init__(self):
        self.x = BASE // 2
        self.y = 0
        self.velocidade = 8
    def atualizar(self):
        self.y += self.velocidade
        if self.y >= HEIGHT:
            self.y = 0
    def desenhar(self, tela):
        pygame.draw.rect(tela, (0, 0, 0), (self.x, self.y, 30, 50))
    def colidiu_com_snake(self, snake):
        cacador_rect = pygame.Rect(self.x, self.y, 30, 50)
        for parte in snake.corpo:
            if pygame.Rect(parte[0], parte[1], 20, 20).colliderect(cacador_rect):
                return True
        return False
    
#=================== MAIN ===================
class Game:
    def __init__(self):
        self.tela = pygame.display.set_mode((BASE, HEIGHT))
        pygame.display.set_caption("Snake Forest Classes")
        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.SysFont('monospace', 30, bold=True)
        self.reset()
    def reset(self):
        self.snake = Snake()
        #criar itens garantindo que não coincidam entre si:
        self.rato = Item((128, 128, 128))
        self.manga = Item((255, 255, 0), exclusoes=[(self.rato.x, self.rato.y)])
        self.maca = Item((255, 0, 0), exclusoes=[(self.rato.x, self.rato.y), (self.manga.x, self.manga.y)])
        self.hunter = Hunter()
        self.macas = 0
        self.mangas = 0
        self.ratos = 0
        self.hora = TEMPO_INICIAL
        self.tp = 0  #contador de tempo 
        self.invencivel = 0
        self.venceu = False
        self.morreu = False

    def coletar_itens(self):
        if self.maca.colidiu(self.snake):
            self.macas += 1
            self.snake.crescer()
            exclusoes = [(self.rato.x, self.rato.y), (self.manga.x, self.manga.y)]
            self.maca.reposicionar(exclusoes=exclusoes)
        if self.manga.colidiu(self.snake):
            self.mangas += 1
            self.snake.crescer()
            exclusoes = [(self.rato.x, self.rato.y), (self.maca.x, self.maca.y)]
            self.manga.reposicionar(exclusoes=exclusoes)
        if self.rato.colidiu(self.snake):
            self.ratos += 1
            self.snake.crescer()
            exclusoes = [(self.maca.x, self.maca.y), (self.manga.x, self.manga.y)]
            self.rato.reposicionar(exclusoes=exclusoes)
    def verificar_colisoes(self):
        """verifica colisões da cobra com o caçador ou com ela mesma"""
        #colisão com caçador
        if self.hunter.colidiu_com_snake(self.snake):
            if self.invencivel == 0:
                if self.ratos > 0:
                    self.ratos -= 1
                    self.invencivel = 60  #tempo de invencibilidade
                else:
                    self.morreu = True
        #colisão com ela mesma
        if self.snake.colidiu_com_corpo():
            self.morreu = True
    def desenhar_interface(self):
        self.tela.blit(self.fonte.render(f"Maçãs: {self.macas}/{ITENS_PARA_VENCER}", True, (0, 0, 0)), (550, 40))
        self.tela.blit(self.fonte.render(f"Mangas: {self.mangas}/{ITENS_PARA_VENCER}", True, (0, 0, 0)), (550, 80))
        self.tela.blit(self.fonte.render(f"Ratos: {self.ratos}", True, (0, 0, 0)), (550, 120))
        hora_texto = self.fonte.render(hora_str(self.hora), True, (0, 0, 0))
        rect = hora_texto.get_rect(center=(BASE // 2, 40))
        self.tela.blit(hora_texto, rect)

    def loop(self):
        """Loop principal do jogo."""
        while True:
            dt = self.relogio.tick(60) 
            self.tp += dt
            if self.invencivel > 0:
                self.invencivel -= 1
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                self.snake.mover(event)

            #controle do tempo
            if self.tp >= 1000:
                self.hora -= 1
                self.tp = 0
            self.snake.atualizar()
            self.hunter.atualizar()
            self.coletar_itens()
            self.verificar_colisoes()
            #derrota
            if self.hora <= 0 and not (self.macas >= ITENS_PARA_VENCER and self.mangas >= ITENS_PARA_VENCER):
                self.morreu = True

            #vitória
            if self.macas >= ITENS_PARA_VENCER and self.mangas >= ITENS_PARA_VENCER:
                self.venceu = True
            self.tela.fill((37, 102, 20))  #fundo verde
            pygame.draw.rect(self.tela, (179, 137, 46), (BASE//2 - 12, 0, 60, HEIGHT))  # Trilha marrom
            #elementos do jogo
            self.snake.desenhar(self.tela)
            self.maca.desenhar(self.tela)
            self.manga.desenhar(self.tela)
            self.rato.desenhar(self.tela)
            self.hunter.desenhar(self.tela)
            self.desenhar_interface()
            pygame.display.update()
            if self.morreu or self.venceu:
                self.tela.fill((255, 255, 255))
                fonte2 = pygame.font.SysFont('arial', 20, True, True)
                if self.morreu:
                    msg = "Game Over! Pressione R para reiniciar"
                else:
                    msg = f"Parabéns! Pontos: {(self.macas + self.mangas) * 10}. Pressione R para reiniciar"
                texto = fonte2.render(msg, True, (0, 0, 0))
                rect = texto.get_rect(center=(BASE//2, HEIGHT//2))
                self.tela.blit(texto, rect)
                pygame.display.update()
                #esperando reinício
                esperando = True
                while esperando:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            exit()
                        elif event.type == KEYDOWN and event.key == K_r:
                            self.reset()
                            esperando = False
# =================== EXECUÇÃO ===================
if __name__ == "__main__":
    Game().loop()