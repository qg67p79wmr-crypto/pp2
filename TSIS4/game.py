import pygame
import random
import json
import os
from config import *
from db import init_db, save_game, get_top, get_best

def run_game():
    pygame.init()

    BASE_DIR = os.path.dirname(__file__)
    SETTINGS_PATH = os.path.join(BASE_DIR, "settings.json")

    with open(SETTINGS_PATH) as f:
        settings = json.load(f)

    snake_color = settings["snake_color"]

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 30)

    init_db()
    username = input("Enter username: ")

    best = get_best(username)

    snake = [(100, 100), (80, 100), (60, 100)]
    direction = (CELL, 0)

    obstacles = []   #  ДО spawn_food

    def spawn_food():
        while True:
            f = (
                random.randint(0, (WIDTH//CELL)-1)*CELL,
                random.randint(0, (HEIGHT//CELL)-1)*CELL
            )
            if f not in snake and f not in obstacles:
                return f

    food = spawn_food()
    poison = spawn_food()

    powerup = None
    effect = None
    effect_time = 0

    score = 0
    level = 1
    speed = 10

    running = True
    while running:
        screen.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = (-CELL,0)
                if event.key == pygame.K_RIGHT:
                    direction = (CELL,0)
                if event.key == pygame.K_UP:
                    direction = (0,-CELL)
                if event.key == pygame.K_DOWN:
                    direction = (0,CELL)

        head = (snake[0][0]+direction[0], snake[0][1]+direction[1])
        snake.insert(0, head)

        #collisions
        if head[0]<0 or head[0]>=WIDTH or head[1]<0 or head[1]>=HEIGHT:
            break
        if head in snake[1:] or head in obstacles:
            break

        # normal food
        if head == food:
            score += 1
            food = spawn_food()
            if score % 4 == 0:
                level += 1
                speed += 2
        else:
            snake.pop()

        #   poison
        if head == poison:
            snake = snake[:-2]
            if len(snake) <= 1:
                break
            poison = spawn_food()

        #obstacles (level 3+)
        if level >= 3 and len(obstacles) < 5:
            obstacles.append(spawn_food())

        #powerups
        if random.randint(1,100) == 1 and not powerup:
            powerup = spawn_food()

        if powerup and head == powerup:
            effect = random.choice(["speed","slow"])
            effect_time = pygame.time.get_ticks()
            powerup = None

        if effect == "speed":
            speed = 20
        elif effect == "slow":
            speed = 5

        if effect and pygame.time.get_ticks() - effect_time > 5000:
            effect = None
            speed = 10 + level*2

        # draw snake
        for part in snake:
            pygame.draw.rect(screen, snake_color, (*part, CELL, CELL))

        pygame.draw.rect(screen, (255,0,0), (*food, CELL, CELL))
        pygame.draw.rect(screen, (139,0,0), (*poison, CELL, CELL))

        if powerup:
            pygame.draw.rect(screen, (0,255,255), (*powerup, CELL, CELL))

        for o in obstacles:
            pygame.draw.rect(screen, (100,100,100), (*o, CELL, CELL))

        # UI
        screen.blit(font.render(f"Score: {score}",True,(255,255,255)),(10,10))
        screen.blit(font.render(f"Level: {level}",True,(255,255,255)),(10,40))
        screen.blit(font.render(f"Best: {best}",True,(255,255,255)),(10,70))

        pygame.display.flip()
        clock.tick(speed)

    save_game(username, score, level)

    # leaderboard screen
    show = True
    while show:
        screen.fill((0,0,0))

        top = get_top()
        for i, row in enumerate(top):
            txt = f"{i+1}. {row[0]} - {row[1]}"
            screen.blit(font.render(txt, True, (255,255,255)), (100,100+i*30))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show = False

    pygame.quit()