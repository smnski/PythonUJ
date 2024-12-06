import pygame
import random
import sys
import time

WIDTH, HEIGHT = 1000, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (148, 148, 148)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Snow Game")
clock = pygame.time.Clock()

square_size = 45
current_squares = []
fallen_squares = []
speed = 2
spawn_rate = 20
score = 0
difficulty_epoch = time.time()

def draw_button(text, x, y, w, h):
    font = pygame.font.Font(None, 40)
    pygame.draw.rect(screen, GRAY, (x, y, w, h))
    pygame.draw.rect(screen, WHITE, (x, y, w, h), 3)
    label = font.render(text, True, WHITE)
    screen.blit(label, ( x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2) )
    return pygame.Rect(x, y, w, h)

def title_screen():
    screen.fill(BLACK)
    while True:
        font = pygame.font.Font(None, 64)
        title_text = font.render("Click the snowflakes before they fall!", True, WHITE)
        screen.blit( title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3) )

        start_button = draw_button("Start", WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return
        pygame.display.flip()
        clock.tick(60)

def collision_check(falling_square):
    for stacked_square in fallen_squares:
        if falling_square.colliderect(stacked_square):
            return True
    return False

def spawn_snowflake():
    x = random.randint(0, WIDTH - square_size)
    y = -square_size
    current_squares.append(pygame.Rect(x, y, square_size, square_size))

def raise_difficulty():
    global speed, spawn_rate, difficulty_epoch
    speed += 1
    spawn_rate = max(5, spawn_rate - 1)
    difficulty_epoch = time.time()

def game_over():
    font = pygame.font.Font(None, 64)
    text = font.render(f"Game Over! Score obtained: {score}", True, WHITE)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

title_screen()
while True:
    screen.fill(BLACK)

    if time.time() - difficulty_epoch >= 10:
        raise_difficulty()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for square in current_squares[:]:
                if square.collidepoint(pos):
                    current_squares.remove(square)
                    score += 1

    if random.randint(1, spawn_rate) == 1:
        spawn_snowflake()

    for square in current_squares[:]:
        square.y += speed
        if square.y + square_size >= HEIGHT or collision_check(square):
            current_squares.remove(square)
            fallen_squares.append(square)

    for square in fallen_squares:
        if square.y <= 0:
            game_over()
    for square in current_squares:
        pygame.draw.rect(screen, WHITE, square)
    for square in fallen_squares:
        pygame.draw.rect(screen, GRAY, square)

    font = pygame.font.Font(None, 40)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)