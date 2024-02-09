import pygame

pygame.init()

# screen options 
screen_w = 600
screen_h = 600

screen = pygame.display.set_mode((screen_w, screen_h))

# pacman object
pacman = pygame.Rect((100, 100, 10, 10))

# game loop
running = True
while running:
    
    # no trails 
    screen.fill((0, 0, 0))

    # drawing "pacman"
    pygame.draw.rect(screen, (0, 100, 0), pacman)

    for event in pygame.event.get():

        if event == pygame.QUIT:
            running = False

    # PAC's MOVING
            
    # get the key from user
    key = pygame.key.get_pressed()

    # moving system ( strong )
    if key[pygame.K_LEFT] == True:
        pacman.move_ip(-1, 0)
    elif key[pygame.K_RIGHT] == True:
        pacman.move_ip(1, 0)
    elif key[pygame.K_UP] == True:
        pacman.move_ip(0, 1)
    elif key[pygame.K_DOWN] == True:
        pacman.move_ip(0, -1)

    # if not -- will be nothing 
    pygame.display.update()

pygame.quit()