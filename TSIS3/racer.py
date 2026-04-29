def run_game():
    import pygame
    import random
    import os
    from persistence import load_leaderboard, save_score, load_settings, save_settings

    pygame.init()

    BASE_DIR = os.path.dirname(__file__)
    SOUND_DIR = os.path.join(BASE_DIR, "assets", "sounds")

    def load_sound(name):
        try:
            return pygame.mixer.Sound(os.path.join(SOUND_DIR, name))
        except:
            return None

    coin_sound = load_sound("coin.wav")
    crash_sound = load_sound("crash.wav")
    nitro_sound = load_sound("nitro.wav")

    settings = load_settings()
    sound_on = settings["sound"]
    difficulty = settings["difficulty"]
    car_color = settings["car_color"]

    WIDTH, HEIGHT = 400, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.SysFont(None, 30)

    username = input("Enter your name: ")

    state = "menu"
    running = True

    # game variables
    def reset_game():
        return {
            "player": pygame.Rect(180, 500, 40, 60),
            "player_speed": 5,
            "coins": [],
            "enemies": [],
            "obstacles": [],
            "powerups": [],
            "score": 0,
            "distance": 0,
            "frame_cnt": 0,
            "shield": False,
            "repair": False,
            "nitro": False,
            "nitro_timer": 0
        }

    game = reset_game()

    while running:

        # menu
        if state == "menu":
            screen.fill((0,0,0))
            screen.blit(font.render("1 - Play", True, (255,255,255)), (120,200))
            screen.blit(font.render("2 - Leaderboard", True, (255,255,255)), (120,250))
            screen.blit(font.render("3 - Settings", True, (255,255,255)), (120,300))
            screen.blit(font.render("Q - Quit", True, (255,255,255)), (120,350))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        game = reset_game()
                        state = "game"
                    if event.key == pygame.K_2:
                        state = "leaderboard"
                    if event.key == pygame.K_3:
                        state = "settings"
                    if event.key == pygame.K_q:
                        running = False
            continue

        # g
        if state == "game":
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                game["player"].x -= game["player_speed"]
            if keys[pygame.K_RIGHT]:
                game["player"].x += game["player_speed"]

            game["player"].x = max(0, min(WIDTH - 40, game["player"].x))

            screen.fill((0, 0, 0))

            game["frame_cnt"] += 1
            game["distance"] += 1

            # spawn
            if game["frame_cnt"] % 20 == 0:
                game["coins"].append(pygame.Rect(random.randint(0, WIDTH-20), 0, 20, 20))

            if game["frame_cnt"] % 80 == 0:
                game["enemies"].append(pygame.Rect(random.randint(0, WIDTH-40), 0, 40, 80))

            if game["frame_cnt"] % 120 == 0:
                game["obstacles"].append(pygame.Rect(random.randint(0, WIDTH-40), 0, 40, 40))

            if game["frame_cnt"] % 200 == 0:
                ptype = random.choice(["nitro","shield","repair"])
                game["powerups"].append({"rect": pygame.Rect(random.randint(0, WIDTH-20),0,20,20),"type":ptype})

            # movement
            for c in game["coins"]: c.y += 3
            for e in game["enemies"]: e.y += 5 + difficulty
            for o in game["obstacles"]: o.y += 4
            for p in game["powerups"]: p["rect"].y += 3

            # collisions
            for c in game["coins"][:]:
                if game["player"].colliderect(c):
                    game["coins"].remove(c)
                    game["score"] += 1
                    if sound_on and coin_sound: coin_sound.play()

            for e in game["enemies"]:
                if game["player"].colliderect(e):
                    if game["shield"]: game["shield"]=False
                    elif game["repair"]: game["repair"]=False
                    else:
                        if sound_on and crash_sound: crash_sound.play()
                        save_score(username, game["score"], game["distance"])
                        state="gameover"

            for o in game["obstacles"]:
                if game["player"].colliderect(o):
                    if game["shield"]: game["shield"]=False
                    elif game["repair"]: game["repair"]=False
                    else:
                        if sound_on and crash_sound: crash_sound.play()
                        save_score(username, game["score"], game["distance"])
                        state="gameover"

            for p in game["powerups"][:]:
                if game["player"].colliderect(p["rect"]):
                    if p["type"]=="nitro":
                        game["nitro"]=True
                        game["nitro_timer"]=120
                        if sound_on and nitro_sound: nitro_sound.play()
                    elif p["type"]=="shield":
                        game["shield"]=True
                    else:
                        game["repair"]=True
                    game["powerups"].remove(p)

            # nitro
            if game["nitro"]:
                game["player_speed"]=8
                game["nitro_timer"]-=1
                if game["nitro_timer"]<=0:
                    game["nitro"]=False
                    game["player_speed"]=5

            # draw
            pygame.draw.rect(screen, car_color, game["player"])

            for c in game["coins"]:
                pygame.draw.circle(screen,(255,215,0),c.center,c.width//2)
            for e in game["enemies"]:
                pygame.draw.rect(screen,(255,0,0),e)
            for o in game["obstacles"]:
                pygame.draw.rect(screen,(100,100,100),o)

            for p in game["powerups"]:
                col=(0,255,255) if p["type"]=="nitro" else (0,0,255) if p["type"]=="shield" else (255,255,0)
                pygame.draw.rect(screen,col,p["rect"])

            screen.blit(font.render(f"Coins: {game['score']}",True,(255,255,255)),(260,10))
            screen.blit(font.render(f"Dist: {game['distance']}",True,(255,255,255)),(10,10))

            pygame.display.flip()

        # gameover
        if state == "gameover":
            screen.fill((0,0,0))
            screen.blit(font.render("GAME OVER",True,(255,0,0)),(120,200))
            screen.blit(font.render("R - Retry",True,(255,255,255)),(120,260))
            screen.blit(font.render("M - Menu",True,(255,255,255)),(120,300))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game = reset_game()
                        state="game"
                    if event.key == pygame.K_m:
                        state="menu"
            continue
#leader
        
        if state == "leaderboard":
            screen.fill((0,0,0))
            data = load_leaderboard()

            for i, e in enumerate(data):
                screen.blit(font.render(f"{i+1}. {e['name']} - {e['score']}",True,(255,255,255)),(60,100+i*30))

            screen.blit(font.render("B - Back",True,(200,200,200)),(120,500))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                    state="menu"
            continue

        
        if state == "settings":
            screen.fill((0,0,0))
            screen.blit(font.render(f"Sound: {sound_on} (S)",True,(255,255,255)),(80,200))
            screen.blit(font.render(f"Difficulty: {difficulty} (D)",True,(255,255,255)),(80,250))

            screen.blit(font.render("B - Back",True,(200,200,200)),(120,500))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        sound_on = not sound_on
                    if event.key == pygame.K_d:
                        difficulty = difficulty%3+1
                    if event.key == pygame.K_b:
                        state="menu"
            continue

    save_settings({
        "sound": sound_on,
        "difficulty": difficulty,
        "car_color": car_color
    })

    pygame.quit()


if __name__ == "__main__":
    run_game()