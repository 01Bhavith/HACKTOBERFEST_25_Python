import pygame
import random

pygame.init()

WIDTH, HEIGHT = 480, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Blocks")

WHITE = (255, 255, 255)
PLAYER_COLOR = (0, 128, 255)
BLOCK_COLOR = (220, 20, 60)
BUTTON_COLOR = (76, 175, 80)
BUTTON_HOVER = (46, 200, 95)

# Start Button layout
button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 - 25, 150, 50)
font = pygame.font.SysFont(None, 40)

def draw_start_button():
    mouse_pos = pygame.mouse.get_pos()
    color = BUTTON_HOVER if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, button_rect)
    text = font.render("START", True, WHITE)
    screen.blit(text, (button_rect.x + 35, button_rect.y + 5))

def wait_for_start():
    waiting = True
    while waiting:
        screen.fill(WHITE)
        title = font.render("Dodge the Blocks!", True, (30, 30, 30))
        screen.blit(title, (WIDTH // 2 - 120, HEIGHT // 2 - 100))
        draw_start_button()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False
        pygame.display.flip()

player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 10
player_speed = 7

block_width = 40
block_height = 20
block_speed = 5
block_list = []

score = 0
running = True
clock = pygame.time.Clock()
game_font = pygame.font.SysFont(None, 36)

def spawn_block():
    x = random.randint(0, WIDTH - block_width)
    block_list.append([x, 0])

def draw_player():
    pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, player_size, player_size))

def draw_blocks():
    for block in block_list:
        pygame.draw.rect(screen, BLOCK_COLOR, (block[0], block[1], block_width, block_height))

def detect_collision():
    for block in block_list:
        if (player_y < block[1] + block_height and
            player_y + player_size > block[1] and
            player_x < block[0] + block_width and
            player_x + player_size > block[0]):
            return True
    return False

wait_for_start()   # Show the start button and wait for user

while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed

    if random.randint(1, 30) == 1:
        spawn_block()

    for block in block_list:
        block[1] += block_speed
    block_list = [b for b in block_list if b[1] < HEIGHT]

    if detect_collision():
        running = False

    score += 1

    draw_player()
    draw_blocks()
    score_surface = game_font.render(f"Score: {score}", True, (0,0,0))
    screen.blit(score_surface, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("Game Over! Your Score:", score)
