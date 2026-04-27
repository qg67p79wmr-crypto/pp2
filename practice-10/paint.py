import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((0, 0, 0))

color = (255, 255, 255)
tool = "brush"
drawing = False
start_pos = None
last_pos = None  

running = True

colors = [
    ((255, 0, 0), pygame.Rect(10, 10, 30, 30)),
    ((0, 255, 0), pygame.Rect(50, 10, 30, 30)),
    ((0, 0, 255), pygame.Rect(90, 10, 30, 30)),
]

tools = [
    ("brush", pygame.Rect(150, 10, 60, 30)),
    ("rect", pygame.Rect(220, 10, 60, 30)),
    ("circle", pygame.Rect(290, 10, 60, 30)),
    ("eraser", pygame.Rect(360, 10, 60, 30)),
]

font = pygame.font.SysFont(None, 20)

while running:

  
    for col, rect in colors:
        pygame.draw.rect(screen, col, rect)

    for name, rect in tools:
        pygame.draw.rect(screen, (200, 200, 200), rect)
        text = font.render(name, True, (0, 0, 0))
        screen.blit(text, (rect.x + 5, rect.y + 5))

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = mouse_pos
            last_pos = mouse_pos 

            for col, rect in colors:
                if rect.collidepoint(mouse_pos):
                    color = col

            for name, rect in tools:
                if rect.collidepoint(mouse_pos):
                    tool = name

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            last_pos = None  

            if tool == "rect":
                pygame.draw.rect(screen, color, (
                    start_pos[0],
                    start_pos[1],
                    mouse_pos[0] - start_pos[0],
                    mouse_pos[1] - start_pos[1]
                ), 2)

            if tool == "circle":
                radius = int(((mouse_pos[0] - start_pos[0])**2 +
                              (mouse_pos[1] - start_pos[1])**2) ** 0.5)
                pygame.draw.circle(screen, color, start_pos, radius, 2)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                tool = "brush"
            if event.key == pygame.K_r:
                tool = "rect"
            if event.key == pygame.K_c:
                tool = "circle"
            if event.key == pygame.K_e:
                tool = "eraser"

            if event.key == pygame.K_1:
                color = (255, 0, 0)
            if event.key == pygame.K_2:
                color = (0, 255, 0)
            if event.key == pygame.K_3:
                color = (0, 0, 255)

  
    if drawing:
        if tool == "brush":
            if last_pos is not None:
                pygame.draw.line(screen, color, last_pos, mouse_pos, 5)
            last_pos = mouse_pos

        if tool == "eraser":
            if last_pos is not None:
                pygame.draw.line(screen, (0, 0, 0), last_pos, mouse_pos, 60)
            last_pos = mouse_pos

    pygame.display.flip()
pygame.quit()