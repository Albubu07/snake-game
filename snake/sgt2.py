import pygame, sys, random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

        # Carregar imagens da cobra
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)

    def update_head_graphics(self):
        if len(self.body) > 1:
            head_relation = self.body[1] - self.body[0]
            if head_relation == Vector2(1,0): 
                self.head = self.head_left
            elif head_relation == Vector2(-1,0): 
                self.head = self.head_right
            elif head_relation == Vector2(0,1): 
                self.head = self.head_up
            elif head_relation == Vector2(0,-1): 
                self.head = self.head_down

    def update_tail_graphics(self):
        if len(self.body) > 1:
            tail_relation = self.body[-2] - self.body[-1]
            if tail_relation == Vector2(1,0): 
                self.tail = self.tail_left
            elif tail_relation == Vector2(-1,0): 
                self.tail = self.tail_right
            elif tail_relation == Vector2(0,1): 
                self.tail = self.tail_up
            elif tail_relation == Vector2(0,-1): 
                self.tail = self.tail_down

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True
        self.play_crunch_sound()

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)

class FRUIT:
    def __init__(self, fruit_type):
        self.type = fruit_type  # 0: maçã, 1: manga, 2: rato
        self.randomize()
        
    def randomize(self):
        # Evitar spawn sob o placar (primeiras 2 linhas)
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(2, cell_number - 1)  # Começa na linha 2
        self.pos = Vector2(self.x, self.y)
        
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        if self.type == 0:
            # Centralizar a maçã
            offset_x = (cell_size - apple.get_width()) // 2
            offset_y = (cell_size - apple.get_height()) // 2
            screen.blit(apple, (fruit_rect.x + offset_x, fruit_rect.y + offset_y))
        elif self.type == 1:
            # Centralizar a manga (agora maior)
            offset_x = (cell_size - mango.get_width()) // 2
            offset_y = (cell_size - mango.get_height()) // 2
            screen.blit(mango, (fruit_rect.x + offset_x, fruit_rect.y + offset_y))
        else:
            # Centralizar o rato (agora maior)
            offset_x = (cell_size - rat.get_width()) // 2
            offset_y = (cell_size - rat.get_height()) // 2
            screen.blit(rat, (fruit_rect.x + offset_x, fruit_rect.y + offset_y))

class HUNTER:
    def __init__(self):
        self.x = cell_number // 2
        self.y = 0
        self.speed = 0.25  # Velocidade aumentada
        
    def move(self):
        self.y += self.speed
        if self.y >= cell_number:
            self.y = 0
            
    def draw(self):
        # Caçador com o dobro do tamanho
        center_x = self.x * cell_size + cell_size // 2
        center_y = self.y * cell_size + cell_size // 2
        screen.blit(hunter_img, (center_x - hunter_img.get_width() // 2, 
                                center_y - hunter_img.get_height() // 2))
        
    def get_pos(self):
        return Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruits = [FRUIT(0), FRUIT(1), FRUIT(2)]  # Maçã, manga, rato
        self.hunter = HUNTER()
        self.scores = [0, 0, 0]  # Maçãs, mangas, ratos
        self.game_over = False
        self.path_rect = pygame.Rect((cell_number // 2 - 1) * cell_size, 0, 3 * cell_size, cell_number * cell_size)
        self.game_over_played = False
        self.crunch_sound = crunch_sound 
        
        # Tocar música de fundo
        pygame.mixer.music.load('Sound/game.wav')
        pygame.mixer.music.play(-1)  # -1 para loop infinito
        
    def update(self):
        if not self.game_over:
            self.snake.move_snake()
            self.check_collision()
            self.check_hunter_collision()
            self.check_wall_collision()
            self.check_self_collision()
            self.hunter.move()
        else:
            # Parar música de fundo e tocar game over
            pygame.mixer.music.stop()
            if not self.game_over_played:
                game_over_sound.play()
                self.game_over_played = True
            
    def check_wall_collision(self):
        head = self.snake.body[0]
        if head.x < 0 or head.x >= cell_number or head.y < 0 or head.y >= cell_number:
            self.game_over = True
            
    def check_self_collision(self):
        # Verifica se a cabeça colidiu com qualquer parte do corpo
        head = self.snake.body[0]
        for segment in self.snake.body[1:]:
            if head == segment:
                self.game_over = True
                break
            
    def draw_elements(self):
        self.draw_grass()
        self.draw_path()
        for fruit in self.fruits:
            fruit.draw_fruit()
        self.snake.draw_snake()
        self.hunter.draw()
        self.draw_score()
        
    def draw_grass(self):
        grass_color = (167, 209, 61)
        
        for row in range(cell_number):
            for col in range(cell_number):
                if (row + col) % 2 == 0:
                    grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)
        
    def draw_path(self):
        path_color = (179, 137, 46)
        pygame.draw.rect(screen, path_color, self.path_rect)
        
    def check_collision(self):
        for i, fruit in enumerate(self.fruits):
            if fruit.pos == self.snake.body[0]:
                fruit.randomize()
                self.snake.add_block()
                self.scores[i] += 1
                
                # Verificar se a nova posição não está no corpo da cobra
                while any(fruit.pos == block for block in self.snake.body):
                    fruit.randomize()
                
                # Verificar se não está no caminho do caçador
                while self.path_rect.collidepoint(fruit.pos.x * cell_size, fruit.pos.y * cell_size):
                    fruit.randomize()
    
    def check_hunter_collision(self):
        # Colisão com o caçador causa morte imediata
        hunter_pos = self.hunter.get_pos()
        head_pos = self.snake.body[0]
        
        # Verifica colisão considerando o tamanho maior do caçador
        hunter_rect = pygame.Rect(
            (self.hunter.x - 0.5) * cell_size,  # Ajuste para o centro
            (self.hunter.y - 0.5) * cell_size, 
            cell_size * 2, 
            cell_size * 2
        )
        head_rect = pygame.Rect(
            head_pos.x * cell_size, 
            head_pos.y * cell_size, 
            cell_size, 
            cell_size
        )
        
        if hunter_rect.colliderect(head_rect):
            self.game_over = True
                
    def draw_score(self):
        # Placar unificado no estilo do primeiro código
        items = [
            {"text": f'Maçãs: {self.scores[0]}', "image": apple_small},
            {"text": f'Mangas: {self.scores[1]}', "image": mango_small},
            {"text": f'Ratos: {self.scores[2]}', "image": rat_small}
        ]
        
        # Calcular altura total do placar
        item_height = 40
        total_height = len(items) * item_height
        padding = 10
        
        # Calcular largura máxima
        max_width = 0
        for item in items:
            text_width = game_font.size(item["text"])[0]
            total_width = 30 + text_width + 6  # 30 para imagem + texto + 6px extra
            if total_width > max_width:
                max_width = total_width
        
        # Posição do placar (canto superior direito)
        score_x = screen_width - max_width - 20
        score_y = 20
        
        # Fundo único para todo o placar
        bg_rect = pygame.Rect(
            score_x - padding, 
            score_y - padding, 
            max_width + 2 * padding, 
            total_height + 2 * padding
        )
        
        # Desenhar fundo e borda
        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)
        
        # Desenhar cada item do placar
        for i, item in enumerate(items):
            y_pos = score_y + i * item_height
            
            # Imagem (25x25)
            img_rect = item["image"].get_rect(topleft=(score_x, y_pos + 7))
            screen.blit(item["image"], img_rect)
            
            # Texto
            text_surface = game_font.render(item["text"], True, (56, 74, 12))
            text_rect = text_surface.get_rect(midleft=(score_x + 30, y_pos + 20))
            screen.blit(text_surface, text_rect)
        
    def reset(self):
        # Reiniciar o jogo
        self.__init__()

# Inicialização do Pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Carregar sons (IMPORTANTE: colocar ANTES de criar main_game)
try:
    pygame.mixer.music.load('Sound/game.wav')
    game_over_sound = pygame.mixer.Sound('Sound/game_over.wav')
    crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')
    print("Todos os sons carregados!")
    pygame.mixer.music.play(-1)  # Loop infinito
except Exception as e:
    print(f"AVISO: Erro nos sons - {e}")
    # Criar sons vazios para evitar erros
    game_over_sound = pygame.mixer.Sound(buffer=bytearray())
    crunch_sound = pygame.mixer.Sound(buffer=bytearray())

# No método __init__ da classe MAIN (remova o carregamento de sons daqui)
 # Usa o som carregado globalmente
# Configurações do jogo
cell_size = 30
cell_number = 20
screen_width = cell_number * cell_size
screen_height = cell_number * cell_size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Forest')
relogio = pygame.time.Clock()

# Carregar imagens para o jogo
# Carregar imagens originais
apple_orig = pygame.image.load('Graphics/apple.png').convert_alpha()
mango_orig = pygame.image.load('Graphics/mango.png').convert_alpha()
rat_orig = pygame.image.load('Graphics/rat.png').convert_alpha()
hunter_orig = pygame.image.load('Graphics/hunter.png').convert_alpha()

# Aumentar tamanho dos itens (dobro do atual)
# Tamanhos anteriores: manga 24x24, rato 26x26 -> Dobro: manga 48x48, rato 52x52
apple = pygame.transform.scale(apple_orig, (cell_size, cell_size))  # Maçã 30x30
mango = pygame.transform.scale(mango_orig, (cell_size * 1.6, cell_size * 1.6))  # Manga 48x48
rat = pygame.transform.scale(rat_orig, (cell_size * 1.73, cell_size * 1.73))    # Rato 52x52

# Caçador gigante
hunter_img = pygame.transform.scale(hunter_orig, (cell_size * 2, cell_size * 2))  # Caçador 60x60

# Criar versões pequenas para o placar (25x25)
apple_small = pygame.transform.scale(apple_orig, (25, 25))
mango_small = pygame.transform.scale(mango_orig, (25, 25))
rat_small = pygame.transform.scale(rat_orig, (25, 25))

# Fonte
try:
    game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
    game_over_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 36)
except:
    game_font = pygame.font.SysFont('monospace', 25, bold=True)
    game_over_font = pygame.font.SysFont('monospace', 36, bold=True)

# Configuração do evento de atualização (mais rápido)
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)  # Mais rápido que 150

# Carregar sons
try:
    game_over_sound = pygame.mixer.Sound('Sound/game_over.wav')
    print("Som de game over carregado com sucesso!")
except Exception as e:
    print(f"Erro ao carregar som de game over: {e}")
    # Criar um som vazio se não conseguir carregar
    game_over_sound = pygame.mixer.Sound(buffer=bytearray())

main_game = MAIN()

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if main_game.game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                main_game.reset()
        else:
            if event.type == SCREEN_UPDATE:
                main_game.update()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
    
    # Desenhar fundo
    screen.fill((175, 215, 70))  # Cor de fundo original
    
    # Desenhar caminho central
    path_rect = pygame.Rect((cell_number // 2 - 1) * cell_size, 0, 3 * cell_size, screen_height)
    pygame.draw.rect(screen, (179, 137, 46), path_rect)
    
    # Desenhar grama (padrão xadrez)
    grass_color = (167, 209, 61)
    for row in range(cell_number):
        for col in range(cell_number):
            # Não desenhar grama no caminho
            if not path_rect.collidepoint(col * cell_size, row * cell_size):
                if (row + col) % 2 == 0:
                    grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)
    
    # Desenhar elementos do jogo
    for fruit in main_game.fruits:
        fruit.draw_fruit()
    main_game.snake.draw_snake()
    main_game.hunter.draw()
    main_game.draw_score()
    
    if main_game.game_over:
        # Fundo escuro semi-transparente
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # Mensagem de game over
        game_over_text = game_over_font.render("GAME OVER", True, (200, 30, 30))
        restart_text = game_font.render("Pressione R para reiniciar", True, (255, 255, 255))
        
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 30))
        restart_rect = restart_text.get_rect(center=(screen_width // 2, screen_height // 2 + 30))
        
        screen.blit(game_over_text, game_over_rect)
        screen.blit(restart_text, restart_rect)
    
    pygame.display.update()
    relogio.tick(60)