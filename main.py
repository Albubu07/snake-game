import pygame
from pygame.locals import *
from sys import exit
from cobra import Snake
from itens import Item
from hunter import Hunter

pygame.init()
pygame.mixer.init()
BASE, HEIGHT = 800, 600
TELA = pygame.display.set_mode((BASE, HEIGHT))
fonte = pygame.font.Font('fonte/Horta demo.otf', 45)
BG_START = pygame.image.load('images/menus/menu.png')
BG_SELECT = pygame.image.load('images/menus/select.png')
BG_WIN = pygame.image.load('images/menus/win.png')
BG_OVER = pygame.image.load('images/menus/die.png')

def hora_str(hora):
    min, sec = divmod(hora, 60)
    return '{:02}:{:02}'.format(min, sec)

def music_load(MUSICA, repetir):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(MUSICA)
    pygame.mixer.music.play(repetir)
    pygame.mixer.music.set_volume(0.50)
    
def fx_load(SOM):
    efeito = pygame.mixer.Sound(SOM)
    efeito.set_volume(0.5)
    efeito.play()

def nivel_um():
    VELOCIDADE_INICIAL = 5   
    ITENS_PARA_VENCER = 5   
    TEMPO_INICIAL = 30
    COR = (92, 225, 230)
    MUSICA = 'musica/nivel1.wav'
    music_load(MUSICA, repetir = -1)    
    BG = pygame.image.load('images/bgs/1.png')
    class Game:
            def __init__(self):
                self.tela = pygame.display.set_mode((BASE, HEIGHT))
                pygame.display.set_caption("Nivel 1")
                self.relogio = pygame.time.Clock()
                self.fonte = fonte
                self.reset()
            
            def reset(self):
                music_load(MUSICA, repetir = -1) 
                self.snake = Snake(VELOCIDADE_INICIAL, COR, 1)
                #criar itens garantindo que não coincidam entre si:
                self.manga = Item((255, 255, 0))
                self.maca = Item((255, 0, 0), exclusoes=[(self.manga.x, self.manga.y)])
                self.macas = 0
                self.mangas = 0
                self.hora = TEMPO_INICIAL
                self.tp = 0  #contador de tempo 
                self.invencivel = 0
                self.venceu = False
                self.morreu = False

            def coletar_itens(self):
                if self.maca.colidiu(self.snake):
                    SOM = 'fx/item.wav'
                    fx_load(SOM)
                    self.macas += 1
                    self.snake.crescer()
                    exclusoes = [(self.manga.x, self.manga.y)]
                    self.maca.reposicionar(exclusoes=exclusoes)
                
                if self.manga.colidiu(self.snake):
                    SOM = 'fx/item.wav'
                    fx_load(SOM)
                    self.mangas += 1
                    self.snake.crescer()
                    exclusoes = [(self.maca.x, self.maca.y)]
                    self.manga.reposicionar(exclusoes=exclusoes)
            
            def verificar_colisoes(self):
                """verifica colisões da cobra com ela mesma"""
                #colisão com ela mesma
                if self.snake.colidiu_com_corpo():
                    self.morreu = True
            
            def desenhar_interface(self):
                itens_text = self.fonte.render(f"Maçãs: {self.macas}/{ITENS_PARA_VENCER}     Mangas: {self.mangas}/{ITENS_PARA_VENCER}", True, ("black"))
                rect = itens_text.get_rect(center=(BASE // 2, 560))
                self.tela.blit(itens_text, rect)
                hora_texto = self.fonte.render(hora_str(self.hora), True, COR)
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
                    self.coletar_itens()
                    self.verificar_colisoes()
                    #derrota
                    if self.hora <= 0 and not (self.macas >= ITENS_PARA_VENCER and self.mangas >= ITENS_PARA_VENCER):
                        self.morreu = True

                    #vitória
                    if self.macas >= ITENS_PARA_VENCER and self.mangas >= ITENS_PARA_VENCER:
                        self.venceu = True
                    self.tela.blit(BG, (0, 0))  #fundo verde
                    #elementos do jogo
                    self.snake.desenhar(self.tela)
                    self.maca.desenhar(self.tela)
                    self.manga.desenhar(self.tela)
                    self.desenhar_interface()
                    pygame.display.update()
                    if self.morreu or self.venceu:
                        if self.morreu:
                            MUSICA = 'musica/lose.wav'
                            TELA.blit(BG_OVER, (0,0))
                        else:
                            MUSICA = 'musica/win.wav'
                            TELA.blit(BG_WIN, (0,0))
                        pygame.display.update()
                        #esperando reinício
                        esperando = True
                        music_load(MUSICA, repetir=0)
                        while esperando:
                            for event in pygame.event.get():
                                if event.type == QUIT:
                                    pygame.quit()
                                    exit()
                                elif event.type == KEYDOWN:
                                    if event.key == K_r and self.morreu:
                                        self.reset()
                                    elif event.key == K_RETURN and not self.morreu:
                                        nivel_dois()
                                    esperando = False

        # =================== EXECUÇÃO ===================
    if __name__ == "__main__":
        Game().loop()

def nivel_dois():
    VELOCIDADE_INICIAL = 5   
    ITENS_PARA_VENCER = 10  
    TEMPO_INICIAL = 60
    COR = (9, 89, 209)
    MUSICA = 'musica/nivel2.wav'   
    music_load(MUSICA, repetir = -1)  
    BG = pygame.image.load('images/bgs/2.png')
    class Game:
        def __init__(self):
            self.tela = pygame.display.set_mode((BASE, HEIGHT))
            pygame.display.set_caption("Nivel 2")
            self.relogio = pygame.time.Clock()
            self.fonte = fonte
            self.reset()
        
        def reset(self):
            music_load(MUSICA, repetir = -1) 
            self.snake = Snake(VELOCIDADE_INICIAL, COR, 2)
            #criar itens garantindo que não coincidam entre si:
            self.vida = Item((166, 232, 138))
            self.manga = Item((255, 255, 0), exclusoes=[(self.vida.x, self.vida.y)])
            self.maca = Item((255, 0, 0), exclusoes=[(self.vida.x, self.vida.y), (self.manga.x, self.manga.y)])
            self.hunter = Hunter((BASE // 2), 5)
            self.macas = 0
            self.mangas = 0
            self.vidas = 0
            self.hora = TEMPO_INICIAL
            self.tp = 0  #contador de tempo 
            self.invencivel = 0
            self.venceu = False
            self.morreu = False

        def coletar_itens(self):
            if self.maca.colidiu(self.snake):
                SOM = 'fx/item.wav'
                fx_load(SOM)
                self.macas += 1
                self.snake.crescer()
                exclusoes = [(self.vida.x, self.vida.y), (self.manga.x, self.manga.y)]
                self.maca.reposicionar(exclusoes=exclusoes)
            if self.manga.colidiu(self.snake):
                SOM = 'fx/item.wav'
                fx_load(SOM)
                self.mangas += 1
                self.snake.crescer()
                exclusoes = [(self.vida.x, self.vida.y), (self.maca.x, self.maca.y)]
                self.manga.reposicionar(exclusoes=exclusoes)
            if self.vida.colidiu(self.snake):
                SOM = 'fx/vida.wav'
                fx_load(SOM)
                self.vidas += 1
                exclusoes = [(self.maca.x, self.maca.y), (self.manga.x, self.manga.y)]
                self.vida.reposicionar(exclusoes=exclusoes)
        
        def verificar_colisoes(self):
            """verifica colisões da cobra com o caçador ou com ela mesma"""
            #colisão com caçador
            if self.hunter.colidiu_com_snake(self.snake):
                if self.invencivel == 0:
                    if self.vidas > 0:
                        SOM = 'fx/perder_vida.wav'
                        fx_load(SOM)
                        self.vidas -= 1
                        self.invencivel = 60  #tempo de invencibilidade
                    else:
                        self.morreu = True
            #colisão com ela mesma
            if self.snake.colidiu_com_corpo():
                self.morreu = True
        
        def desenhar_interface(self):
            itens_text = self.fonte.render(f"Maçãs: {self.macas}/{ITENS_PARA_VENCER}     Mangas: {self.mangas}/{ITENS_PARA_VENCER}     Vidas: {self.vidas}", True, ("black"))
            rect = itens_text.get_rect(center=(BASE // 2, 560))
            self.tela.blit(itens_text, rect)
            hora_texto = self.fonte.render(hora_str(self.hora), True, COR)
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
                self.tela.blit(BG, (0,0))  #fundo verde
                #elementos do jogo
                self.snake.desenhar(self.tela)
                self.maca.desenhar(self.tela)
                self.manga.desenhar(self.tela)
                self.vida.desenhar(self.tela)
                self.hunter.desenhar(self.tela)
                self.desenhar_interface()
                pygame.display.update()
                if self.morreu or self.venceu:
                    if self.morreu:
                        MUSICA = 'musica/lose.wav'
                        TELA.blit(BG_OVER, (0,0))
                    else:
                        MUSICA = 'musica/win.wav'
                        TELA.blit(BG_WIN, (0,0))
                    pygame.display.update()
                    #esperando reinício
                    esperando = True
                    music_load(MUSICA, repetir=0)
                    while esperando:
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                exit()
                            elif event.type == KEYDOWN:
                                    if event.key == K_r and self.morreu:
                                        self.reset()
                                    elif event.key == K_RETURN:
                                        nivel_tres()
                                    esperando = False

    # =================== EXECUÇÃO ===================
    if __name__ == "__main__":
        Game().loop()

def nivel_tres():
    VELOCIDADE_INICIAL = 5   
    ITENS_PARA_VENCER = 15   
    TEMPO_INICIAL = 90
    COR = (0, 255, 0)
    MUSICA = 'musica/nivel3.wav'
    music_load(MUSICA, repetir = -1)     
    BG = pygame.image.load('images/bgs/3.png')
    class Game:
        def __init__(self):
            self.tela = pygame.display.set_mode((BASE, HEIGHT))
            pygame.display.set_caption("Nivel 3")
            self.relogio = pygame.time.Clock()
            self.fonte = fonte
            self.reset()
        
        def reset(self):
            music_load(MUSICA, repetir = -1) 
            self.snake = Snake(VELOCIDADE_INICIAL, COR, 3)
            #criar itens garantindo que não coincidam entre si:
            self.vida = Item((166, 232, 138))
            self.manga = Item((255, 255, 0), exclusoes=[(self.vida.x, self.vida.y)])
            self.maca = Item((255, 0, 0), exclusoes=[(self.vida.x, self.vida.y), (self.manga.x, self.manga.y)])
            self.hunter1, self.hunter2 = Hunter(200, 5), Hunter(600, 6)
            self.macas = 0
            self.mangas = 0
            self.vidas = 0
            self.hora = TEMPO_INICIAL
            self.tp = 0  #contador de tempo 
            self.invencivel = 0
            self.venceu = False
            self.morreu = False

        def coletar_itens(self):
            if self.maca.colidiu(self.snake):
                SOM = 'fx/item.wav'
                fx_load(SOM)
                self.macas += 1
                self.snake.crescer()
                exclusoes = [(self.vida.x, self.vida.y), (self.manga.x, self.manga.y)]
                self.maca.reposicionar(exclusoes=exclusoes)
            if self.manga.colidiu(self.snake):
                SOM = 'fx/item.wav'
                fx_load(SOM)
                self.mangas += 1
                self.snake.crescer()
                exclusoes = [(self.vida.x, self.vida.y), (self.maca.x, self.maca.y)]
                self.manga.reposicionar(exclusoes=exclusoes)
            if self.vida.colidiu(self.snake):
                SOM = 'fx/vida.wav'
                fx_load(SOM)
                self.vidas += 1
                exclusoes = [(self.maca.x, self.maca.y), (self.manga.x, self.manga.y)]
                self.vida.reposicionar(exclusoes=exclusoes)
        
        def verificar_colisoes(self):
            """verifica colisões da cobra com o caçador ou com ela mesma"""
            #colisão com caçador
            for hunter in [self.hunter1, self.hunter2]:
                if hunter.colidiu_com_snake(self.snake):
                    if self.invencivel == 0:
                        if self.vidas > 0:
                            SOM = 'fx/perder_vida.wav'
                            fx_load(SOM)
                            self.vidas -= 1
                            self.invencivel = 60  #tempo de invencibilidade
                        else:
                            self.morreu = True
            #colisão com ela mesma
            if self.snake.colidiu_com_corpo():
                self.morreu = True
        
        def desenhar_interface(self):
            itens_text = self.fonte.render(f"Maçãs: {self.macas}/{ITENS_PARA_VENCER}     Mangas: {self.mangas}/{ITENS_PARA_VENCER}     Vidas: {self.vidas}", True, ("black"))
            rect = itens_text.get_rect(center=(BASE // 2, 560))
            self.tela.blit(itens_text, rect)
            hora_texto = self.fonte.render(hora_str(self.hora), True, COR)
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
                for hunter in [self.hunter1, self.hunter2]:
                    hunter.atualizar()
                self.coletar_itens()
                self.verificar_colisoes()
                #derrota
                if self.hora <= 0 and not (self.macas >= ITENS_PARA_VENCER and self.mangas >= ITENS_PARA_VENCER):
                    self.morreu = True

                #vitória
                if self.macas >= ITENS_PARA_VENCER and self.mangas >= ITENS_PARA_VENCER:
                    self.venceu = True
                self.tela.blit(BG, (0,0))  #fundo verde
                #elementos do jogo
                self.snake.desenhar(self.tela)
                self.maca.desenhar(self.tela)
                self.manga.desenhar(self.tela)
                self.vida.desenhar(self.tela)
                for hunter in [self.hunter1, self.hunter2]:
                    hunter.desenhar(self.tela)
                self.desenhar_interface()
                pygame.display.update()
                if self.morreu or self.venceu:
                    if self.morreu:
                            MUSICA = 'musica/lose.wav'
                            TELA.blit(BG_OVER, (0,0))
                    else:
                            MUSICA = 'musica/win.wav'
                            TELA.blit(BG_WIN, (0,0))
                    pygame.display.update()
                    #esperando reinício
                    esperando = True
                    music_load(MUSICA, repetir=0)
                    while esperando:
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                exit()
                            elif event.type == KEYDOWN:
                                    if event.key == K_r and self.morreu:
                                        self.reset()
                                    elif event.key == K_RETURN:
                                        nivel_quatro()
                                    esperando = False

    # =================== EXECUÇÃO ===================
    if __name__ == "__main__":
        Game().loop()

def nivel_quatro():
    VELOCIDADE_INICIAL = 5   
    ITENS_PARA_VENCER = 20  
    TEMPO_INICIAL = 120
    COR = (255, 0, 0)
    MUSICA = 'musica/nivel4.wav' 
    music_load(MUSICA, repetir = -1)    
    BG = pygame.image.load('images/bgs/4.png')
    class Game:
        def __init__(self):
            self.tela = pygame.display.set_mode((BASE, HEIGHT))
            pygame.display.set_caption("Nivel 4")
            self.relogio = pygame.time.Clock()
            self.fonte = fonte
            self.reset()
        
        def reset(self):
            music_load(MUSICA, repetir = -1) 
            self.snake = Snake(VELOCIDADE_INICIAL, COR, 4)
            #criar itens garantindo que não coincidam entre si:
            self.vida = Item((166, 232, 138))
            self.manga = Item((255, 255, 0), exclusoes=[(self.vida.x, self.vida.y)])
            self.maca = Item((255, 0, 0), exclusoes=[(self.vida.x, self.vida.y), (self.manga.x, self.manga.y)])
            self.hunter1, self.hunter2, self.hunter3 = Hunter(180, 6), Hunter((BASE // 2), 7), Hunter(620, 8)
            self.macas = 0
            self.mangas = 0
            self.vidas = 0
            self.hora = TEMPO_INICIAL
            self.tp = 0  #contador de tempo 
            self.invencivel = 0
            self.venceu = False
            self.morreu = False

        def coletar_itens(self):
            if self.maca.colidiu(self.snake):
                SOM = 'fx/item.wav'
                fx_load(SOM)
                self.macas += 1
                self.snake.crescer()
                exclusoes = [(self.vida.x, self.vida.y), (self.manga.x, self.manga.y)]
                self.maca.reposicionar(exclusoes=exclusoes)
            if self.manga.colidiu(self.snake):
                SOM = 'fx/item.wav'
                fx_load(SOM)
                self.mangas += 1
                self.snake.crescer()
                exclusoes = [(self.vida.x, self.vida.y), (self.maca.x, self.maca.y)]
                self.manga.reposicionar(exclusoes=exclusoes)
            if self.vida.colidiu(self.snake):
                SOM = 'fx/vida.wav'
                fx_load(SOM)
                self.vidas += 1
                exclusoes = [(self.maca.x, self.maca.y), (self.manga.x, self.manga.y)]
                self.vida.reposicionar(exclusoes=exclusoes)
        
        def verificar_colisoes(self):
            """verifica colisões da cobra com o caçador ou com ela mesma"""
            #colisão com caçador
            for hunter in [self.hunter1, self.hunter2, self.hunter3]:
                if hunter.colidiu_com_snake(self.snake):
                    if self.invencivel == 0:
                        if self.vidas > 0:
                            SOM = 'fx/perder_vida.wav'
                            fx_load(SOM)
                            self.vidas -= 1
                            self.invencivel = 60  #tempo de invencibilidade
                        else:
                            self.morreu = True
            #colisão com ela mesma
            if self.snake.colidiu_com_corpo():
                self.morreu = True
        
        def desenhar_interface(self):
            itens_text = self.fonte.render(f"Maçãs: {self.macas}/{ITENS_PARA_VENCER}     Mangas: {self.mangas}/{ITENS_PARA_VENCER}     Vidas: {self.vidas}", True, ("black"))
            rect = itens_text.get_rect(center=(BASE // 2, 560))
            self.tela.blit(itens_text, rect)
            hora_texto = self.fonte.render(hora_str(self.hora), True, COR)
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
                for hunter in [self.hunter1, self.hunter2, self.hunter3]:
                    hunter.atualizar()
                self.coletar_itens()
                self.verificar_colisoes()
                #derrota
                if self.hora <= 0 and not (self.macas >= ITENS_PARA_VENCER and self.mangas >= ITENS_PARA_VENCER):
                    self.morreu = True

                #vitória
                if self.macas >= ITENS_PARA_VENCER and self.mangas >= ITENS_PARA_VENCER:
                    self.venceu = True
                self.tela.blit(BG, (0,0))  #fundo verde
                #elementos do jogo
                self.snake.desenhar(self.tela)
                self.maca.desenhar(self.tela)
                self.manga.desenhar(self.tela)
                self.vida.desenhar(self.tela)
                for hunter in [self.hunter1, self.hunter2, self.hunter3]:
                    hunter.desenhar(self.tela)
                self.desenhar_interface()
                pygame.display.update()
                if self.morreu or self.venceu:
                    BG_WIN = pygame.image.load('images/menus/final.png')
                    if self.morreu:
                            MUSICA = 'musica/lose.wav'
                            TELA.blit(BG_OVER, (0,0))
                    else:
                            MUSICA = 'musica/win.wav'
                            TELA.blit(BG_WIN, (0,0))
                    pygame.display.update()
                    #esperando reinício
                    esperando = True
                    music_load(MUSICA, repetir=0)
                    while esperando:
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                exit()
                            elif event.type == KEYDOWN:
                                    if event.key == K_r and self.morreu:
                                        self.reset()
                                    elif event.key == K_RETURN:
                                        main_menu()
                                    esperando = False

    # =================== EXECUÇÃO ===================
    if __name__ == "__main__":
        Game().loop()

def selecao_nivel():
    while True:
        pygame.display.set_caption('Main Menu')
        TELA.blit(BG_SELECT, (0,0))
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
            if event.type == KEYDOWN:
                if event.key == K_1 or event.key == K_2 or event.key == K_3 or event.key == K_4:
                    SOM = 'fx/click.mp3'
                    fx_load(SOM)
                    if event.key == K_1:
                        nivel_um()
                    elif event.key == K_2:
                        nivel_dois() 
                    elif event.key == K_3:
                        nivel_tres() 
                    elif event.key == K_4:
                        nivel_quatro()    
        
        pygame.display.update()

def main_menu():
    MUSICA = 'musica/tela_inicial.wav'
    music_load(MUSICA, repetir=-1)
    while True:
        pygame.display.set_caption('Main Menu')
        TELA.blit(BG_START, (0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN or event.key == K_KP_ENTER:
                    SOM = 'fx/click.mp3'
                    fx_load(SOM)
                    selecao_nivel()
        
        pygame.display.update()

main_menu() 