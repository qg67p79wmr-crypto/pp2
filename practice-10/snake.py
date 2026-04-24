import pygame
import random

pygame.init()


WIDTH, HEIGHT = 600, 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


snake = [(100, 100), (80, 100), (60, 100)]
direction = (20, 0)


def spawn_food():
    while True:
        food = (
            random.randint(0, (WIDTH // CELL) - 1) * CELL,
            random.randint(0, (HEIGHT // CELL) - 1) * CELL
        )
        if food not in snake:
            return food

food = spawn_food()


score = 0
level = 1
speed = 10

font = pygame.font.SysFont(None, 30)

running = True
while running:
    screen.fill((0, 0, 0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction = (-CELL, 0)
            if event.key == pygame.K_RIGHT:
                direction = (CELL, 0)
            if event.key == pygame.K_UP:
                direction = (0, -CELL)
            if event.key == pygame.K_DOWN:
                direction = (0, CELL)


    head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    snake.insert(0, head)

    
    if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
        running = False

    
    if head in snake[1:]:
        running = False


    if head == food:
        score += 1
        food = spawn_food()

        
        if score % 4 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()  

    
    for part in snake:
        pygame.draw.rect(screen, (0, 255, 0), (*part, CELL, CELL))

    pygame.draw.rect(screen, (255, 0, 0), (*food, CELL, CELL))


    score_text = font.render(f"Score: {score}", True, (255,255,255))
    level_text = font.render(f"Level: {level}", True, (255,255,255))

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()