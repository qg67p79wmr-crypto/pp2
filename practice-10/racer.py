import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

player = pygame.Rect(180, 500, 40, 60)

coins = []
coin_size = 20
coin_delay = 30
frame_cnt = 0

score = 0
font = pygame.font.SysFont(None, 30)

running = True
while running:
    screen.fill((0, 0, 0))

    frame_cnt += 1
    

   
    if frame_cnt % coin_delay == 0:
        x = random.randint(0, WIDTH - coin_size)
        coins.append(pygame.Rect(x, 0, coin_size, coin_size))

    
    for coin in coins:
        coin.y += 5

    
    for coin in coins[:]:
        if player.colliderect(coin):
            coins.remove(coin)
            score += 1
    
    pygame.draw.rect(screen, (0, 255, 0), player)

    for coin in coins:
        pygame.draw.circle(screen, (255, 215, 0), coin.center, coin.width//2)

  
    score_text = font.render(f"Coins: {score}", True, (255, 255, 255))
    screen.blit(score_text, (WIDTH - 120, 10))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

