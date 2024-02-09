import pygame

pygame.init()

# screen options 
screen_w = 600
screen_h = 600

screen = pygame.display.set_mode((screen_w, screen_h))

# game loop
running = True
while running:
    
    for event in pygame.event.get():
        if event == pygame.QUIT:
            run = False

pygame.quit()