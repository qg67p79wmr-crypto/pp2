import pygame
from datetime import datetime
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((0, 0, 0))

color = (255, 255, 255)
texts = []
tool = "brush"
text_mode = False
text_input = ""
text_pos = (0, 0)
drawing = False
start_pos = None
last_pos = None  
brush_size = 5
running = True

colors = [
    ((255, 0, 0), pygame.Rect(10, 10, 30, 30)),
    ((0, 255, 0), pygame.Rect(50, 10, 30, 30)),
    ((0, 0, 255), pygame.Rect(90, 10, 30, 30)),
]

tools = [
    ("brush", pygame.Rect(150, 10, 60, 30)),
    ("text", pygame.Rect(570, 10, 60, 30)),
    ("fill", pygame.Rect(500, 10, 60, 30)),
    ("rect", pygame.Rect(220, 10, 60, 30)),
    ("circle", pygame.Rect(290, 10, 60, 30)),
    ("eraser", pygame.Rect(360, 10, 60, 30)),
    ("line", pygame.Rect(430, 10, 60, 30)),  
]

font = pygame.font.SysFont(None, 20)
def flood_fill(surface, x, y, new_color):
    width, height = surface.get_size()
    target_color = surface.get_at((x, y))

    if target_color == new_color:
        return

    stack = [(x, y)]

    while stack:
        x, y = stack.pop()

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        if surface.get_at((x, y)) != target_color:
            continue

        surface.set_at((x, y), new_color)

        stack.append((x+1, y))
        stack.append((x-1, y))
        stack.append((x, y+1))
        stack.append((x, y-1))
while running:
    
    for col, rect in colors:
        pygame.draw.rect(screen, col, rect)

    for name, rect in tools:
        pygame.draw.rect(screen, (200, 200, 200), rect)
        label = font.render(name, True, (0, 0, 0))
        screen.blit(label, (rect.x + 5, rect.y + 5))

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if tool == "text" and mouse_pos[1] > 50:
                text_mode = True
                text_input = ""
                text_pos = mouse_pos
                drawing = False
                continue
            start_pos = mouse_pos
            last_pos = mouse_pos

            for col, rect in colors:
                if rect.collidepoint(mouse_pos):
                    color = col

            for name, rect in tools:
                if rect.collidepoint(mouse_pos):
                    tool = name

            if tool == "fill" and mouse_pos[1] > 50:
                flood_fill(screen, mouse_pos[0], mouse_pos[1], color)
            else:
                drawing = True
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            last_pos = None  

            if tool == "line" and start_pos is not None:
                pygame.draw.line(screen, color, start_pos, mouse_pos, brush_size)

            if tool == "rect" and start_pos is not None:
                pygame.draw.rect(screen, color, (
                    start_pos[0],
                    start_pos[1],
                    mouse_pos[0] - start_pos[0],
                    mouse_pos[1] - start_pos[1]
                    ), brush_size)
            if tool == "circle" and start_pos is not None:
                radius = int(((mouse_pos[0] - start_pos[0])**2 +
                              (mouse_pos[1] - start_pos[1])**2) ** 0.5)
                pygame.draw.circle(screen, color, start_pos, radius, brush_size)


        if event.type == pygame.KEYDOWN:
            if text_mode:
                if event.key == pygame.K_RETURN:
                    texts.append((text_input, text_pos, color))
                    text_mode = False
                    text_input = ""

                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    text_input = ""
                    
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]

                else:
                    text_input += event.unicode

                continue  


            if event.key == pygame.K_DELETE:
                if texts:
                    texts.pop()


            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                filename = datetime.now().strftime("drawing_%Y%m%d_%H%M%S.png")
                pygame.image.save(screen, filename)
                print(f"Saved: {filename}")
            if event.key == pygame.K_l:
                tool = "line"
            if event.key == pygame.K_b:
                tool = "brush"
            if event.key == pygame.K_r:
                tool = "rect"
            if event.key == pygame.K_c:
                tool = "circle"
            if event.key == pygame.K_e:
                tool = "eraser"


            if event.key == pygame.K_1:
                brush_size = 2
            if event.key == pygame.K_2:
                brush_size = 5
            if event.key == pygame.K_3:
                brush_size = 10

  
    if drawing:
        if tool == "brush":
            if last_pos is not None:
                pygame.draw.line(screen, color, last_pos, mouse_pos, brush_size)
            last_pos = mouse_pos

        if tool == "eraser":
            if last_pos is not None:
                pygame.draw.line(screen, (0, 0, 0), last_pos, mouse_pos, brush_size)
            last_pos = mouse_pos

    if drawing and start_pos is not None and tool in ["rect", "circle", "line"]:
        temp = screen.copy()
        if tool == "rect":
            pygame.draw.rect(temp, color, (
                start_pos[0],
                start_pos[1],
                mouse_pos[0] - start_pos[0],
                mouse_pos[1] - start_pos[1]
                ), brush_size)

        if tool == "circle":
            radius = int(((mouse_pos[0] - start_pos[0])**2 +
                          (mouse_pos[1] - start_pos[1])**2) ** 0.5)
            pygame.draw.circle(temp, color, start_pos, radius, brush_size)

        if tool == "line":
            pygame.draw.line(temp, color, start_pos, mouse_pos, brush_size)

        screen.blit(temp, (0, 0))
    if text_mode:

        temp = screen.copy()
        text_surface = font.render(text_input, True, color)
        temp.blit(text_surface, text_pos)
        screen.blit(temp, (0, 0))
    for txt, pos, col in texts:
        text_surface = font.render(txt, True, col)
        screen.blit(text_surface, pos)
    pygame.display.flip()
pygame.quit()