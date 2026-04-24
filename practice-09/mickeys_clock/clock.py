import pygame
import datetime

class Clock:
    def __init__(self):
        
        self.bg = pygame.image.load("images/clock.png")
        self.bg = pygame.transform.scale(self.bg, (600, 600))

        self.mickey = pygame.image.load("images/mickey.png")
        self.mickey = pygame.transform.scale(self.mickey, (300, 400))

        self.left_hand = pygame.image.load("images/hand_left_centered.png")  
        self.left_hand = pygame.transform.scale(self.left_hand, (150, 150))

        self.right_hand = pygame.image.load("images/hand_right_centered.png") 
        self.right_hand = pygame.transform.scale(self.right_hand, (150, 150))

        self.center = (300, 300)

    def draw(self, screen):
        # фон + микки
        screen.blit(self.bg, (0, 0))
        screen.blit(self.mickey, (150, 150))

       
        now = datetime.datetime.now()
        seconds = now.second
        minutes = now.minute

       
        sec_angle = -seconds * 6
        min_angle = -minutes * 6

    
        sec_hand = pygame.transform.rotate(self.left_hand, sec_angle)
        min_hand = pygame.transform.rotate(self.right_hand, min_angle)

        
        sec_rect = sec_hand.get_rect(center=self.center)
        min_rect = min_hand.get_rect(center=self.center)


        screen.blit(sec_hand, sec_rect)
        screen.blit(min_hand, min_rect)