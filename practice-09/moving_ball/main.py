import pygame
from ball import Ball

pygame.init()
screen = pygame.display.set_mode((600, 400))

ball = Ball()

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    ball.move(keys)
    ball.draw(screen)

    pygame.display.flip()

pygame.quit()