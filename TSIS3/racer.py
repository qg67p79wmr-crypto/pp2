import pygame
import random
from persistence import load_leaderboard, save_score
pygame.init()

WIDTH, HEIGHT=400, 600
screen= pygame.display.set_mode((WIDTH, HEIGHT))
username= input("Enter your name: ")
player=pygame.Rect(180, 500, 40, 60)
player_speed =5

shield_active= False
repair_available = False

coins =[]    
enemies=[]   
obstacles = []     
powerups = []      

frame_cnt = 0

score = 0
distance = 0        

font = pygame.font.SysFont(None, 30)

nitro_active = False
nitro_timer = 0

running =True
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
    distance += 1   


    if frame_cnt % 20 == 0:
        x = random.randint(0, WIDTH - 20)
        coins.append(pygame.Rect(x, 0, 20, 20))

    if frame_cnt % 100 == 0:
        x = random.randint(0, WIDTH - 40)
        enemies.append(pygame.Rect(x, 0, 40, 80))

    if frame_cnt % 100 == 0:
        x = random.randint(0, WIDTH - 40)
        obstacles.append(pygame.Rect(x, 0, 40, 40))

    if frame_cnt % 200 == 0:
        x = random.randint(0, WIDTH - 20)
        ptype = random.choice(["nitro", "shield", "repair"])
        powerups.append({"rect": pygame.Rect(x, 0, 20, 20), "type": ptype})


   
    for coin in coins:
        coin.y += 3

    for enemy in enemies:
        enemy.y += 5

    for obs in obstacles:
        obs.y += 4

    for p in powerups:
        p["rect"].y += 3


   
    for coin in coins[:]:
        if coin.y > HEIGHT:
            coins.remove(coin)

    for enemy in enemies[:]:
        if enemy.y > HEIGHT:
            enemies.remove(enemy)

    for obs in obstacles[:]:
        if obs.y > HEIGHT:
            obstacles.remove(obs)

    for p in powerups[:]:
        if p["rect"].y > HEIGHT:   # FIX
            powerups.remove(p)


    # collisions
    for coin in coins[:]:
        if player.colliderect(coin):
            coins.remove(coin)
            score += 1

    for enemy in enemies:
        if player.colliderect(enemy):
            if shield_active:
                shield_active = False
            elif repair_available:
                repair_available = False
            else:
                save_score(username, score, distance)
                running = False

    for obs in obstacles:
        if player.colliderect(obs):
            if shield_active:
                shield_active = False
            elif repair_available:
                repair_available = False
            else:
                save_score(username, score, distance)
                running = False
    for p in powerups[:]:
        if player.colliderect(p["rect"]):
            if p["type"] == "nitro":
                nitro_active = True
                nitro_timer = 120
            elif p["type"] == "shield":
                shield_active = True
            elif p["type"] == "repair":
                repair_available = True

            powerups.remove(p)


 
    if nitro_active:
        player_speed = 8
        nitro_timer -= 1
        if nitro_timer <= 0:
            nitro_active = False
            player_speed = 5


   
    if score % 5 == 0 and score != 0:
        for enemy in enemies:
            enemy.y += 1


    
    pygame.draw.rect(screen, (0, 255, 0), player)

    for coin in coins:
        pygame.draw.circle(screen, (255, 215, 0), coin.center, coin.width // 2)

    for enemy in enemies:
        pygame.draw.rect(screen, (255, 0, 0), enemy)

    for obs in obstacles:
        pygame.draw.rect(screen, (100, 100, 100), obs)

    for p in powerups:
        if p["type"] == "nitro":
            color = (0, 255, 255)
        elif p["type"] == "shield":
            color = (0, 0, 255)
        else:
            color = (255, 255, 0)

        pygame.draw.rect(screen, color, p["rect"])


    # UI 
    score_text = font.render(f"Coins: {score}", True, (255, 255, 255))
    dist_text = font.render(f"Dist: {distance}", True, (255, 255, 255))

    screen.blit(score_text, (WIDTH - 120, 10))
    screen.blit(dist_text, (10, 10))

    if nitro_active:
        screen.blit(font.render("NITRO!", True, (0, 255, 255)), (WIDTH//2 - 40, 10))

    if shield_active:
        screen.blit(font.render("SHIELD", True, (0, 0, 255)), (WIDTH//2 - 40, 40))

    if repair_available:
        screen.blit(font.render("REPAIR", True, (255, 255, 0)), (WIDTH//2 - 40, 70))


    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
