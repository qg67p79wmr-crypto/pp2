import pygame
from player import Player

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont(None, 30)

player = Player()

running = True
while running:
    screen.fill((255, 255, 255))  

    text = font.render("P-play S-stop N-next B-back", True, (0, 0, 0))
    screen.blit(text, (20, 80))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            if event.key == pygame.K_s:
                player.stop()
            if event.key == pygame.K_n:
                player.next()
            if event.key == pygame.K_b:
                player.prev()

    pygame.display.flip() 

pygame.quit()