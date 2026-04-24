import pygame
from clock import Clock

pygame.init()

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Mickey Clock")
icon = pygame.image.load('images/clock.png')
pygame.display.set_icon(icon)
clock_obj = Clock()
timer = pygame.time.Clock()

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock_obj.draw(screen)

    pygame.display.flip()
    timer.tick(60)  # обновление

pygame.quit()