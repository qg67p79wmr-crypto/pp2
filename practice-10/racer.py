import pygame
import random

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

player = pygame.Rect(180, 500, 40, 60)
player_speed = 5

coins = []    
enemies = []   

frame_cnt = 0

score = 0
font = pygame.font.SysFont(None, 30)

running = True
while running:
    keys = pygame.key.get_pressed()


    if keys[pygame.K_LEFT]:
        player.x -= player_speed

    if keys[pygame.K_RIGHT]:
        player.x += player_speed

  
    if player.x < 0:
        player.x = 0
    if player.x > WIDTH - player.width:
        player.x = WIDTH - player.width

    screen.fill((0, 0, 0))

    frame_cnt += 1

    
    if frame_cnt % 20 == 0:
        x = random.randint(0, WIDTH - 20)
        coins.append(pygame.Rect(x, 0, 20, 20))


    if frame_cnt % 10 == 0:
        x = random.randint(0, WIDTH - 40)
        enemies.append(pygame.Rect(x, 0, 40, 80))

   
    for coin in coins:
        coin.y += 3

    for enemy in enemies:
        enemy.y += 5


    for coin in coins[:]:
        if coin.y > HEIGHT:
            coins.remove(coin)

    for enemy in enemies[:]:
        if enemy.y > HEIGHT:
            enemies.remove(enemy)


    for coin in coins[:]:
        if player.colliderect(coin):
            coins.remove(coin)
            score += 1


    for enemy in enemies:
        if player.colliderect(enemy):
            running = False


    pygame.draw.rect(screen, (0, 255, 0), player)


    for coin in coins:
        pygame.draw.circle(screen, (255, 215, 0), coin.center, coin.width // 2)


    for enemy in enemies:
        pygame.draw.rect(screen, (255, 0, 0), enemy)


    score_text = font.render(f"Coins: {score}", True, (255, 255, 255))
    screen.blit(score_text, (WIDTH - 120, 10))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()