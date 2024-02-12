import pygame
import math
from board import boards

pygame.init()


# settings variables: screen, framerates, fonts etc...

# resolution, display
WIDTH = 900
HEIGHT = 950 

num1 = ((HEIGHT - 50) // 32 )
num2 = (WIDTH // 30)
num3 = 15 # fat factor for the player

screen = pygame.display.set_mode([WIDTH, HEIGHT])

# framerate
timer = pygame.time.Clock()
fps = 60

font = pygame.font.Font('freesansbold.ttf', 20) # font: default windows

level = boards # board array imported from board.py

color = 'blue' # color variable

PI = math.pi # pi 
 
player_images = []

# animations
for i in range(1, 5): 
    player_images.append(pygame.transform.scale(pygame.image.load(f'./Pacman Python/assets/player_images/{i}.png'), (45, 45)))

# starting pos
player_x = 450
player_y = 663

# other player variables
direction = 0
counter = 0

flicker = False

turns_allowed = [False, False, False, False]

def draw_board():
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j*num2 + (0.5*num2), i*num1 + (0.5*num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j*num2 + (0.5*num2), i*num1 + (0.5*num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j*num2 + (0.5*num2), i*num1), (j*num2 + (0.5*num2), i*num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j*num2, i*num1 + (0.5*num1)), (j*num2 + num2, i*num1 + (0.5*num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j*num2 - (num2*0.5)) + 2, (i*num1 + (num1*0.5)), num2, num1], 0, PI/2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color, [(j*num2 + (num2*0.5)), (i*num1 + (num1*0.5)), num2, num1], PI/2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j*num2 + (num2*0.5)), (i*num1 - (num1*0.4)), num2, num1], PI, 3*PI/2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color, [(j*num2 - (num2*0.4)) - 2, (i*num1 - (num1*0.4)), num2, num1], 3*PI/2, 2*PI, 3) 
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j*num2, i * num1 + (0.5*num1)), (j*num2 + num2, i*num1 + (0.5*num1)), 3)
                    
def draw_player():
    if direction == 0: # RIGHT
        screen.blit(player_images[counter // 5], (player_x, player_y))
    if direction == 1: # LEFT
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    if direction == 2: # UP
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    if direction == 3: # DOWN
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))

def check_position(centerx, centery):
    turns = [False, False, False, False]
    
    if centerx // 30 < 29:
        if direction == 0: # RIGHT
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1: # LEFT
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2: # UP
            if level[(centery + num3) // num1][(centerx - num3) // num2] < 3:
                turns[3] = True
        if direction == 3: # DOWN
            if level[(centery - num3) // num1][(centerx - num3) // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centerx % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
                    
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centerx % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True          


    else:
        turns[0] = True
        turns[1] = True

    return turns


# main game loop 

run = True
while run:
    timer.tick(fps) # framerateeeee
    screen.fill('black') #bg color

    if counter < 19: 
        counter += 1
        if counter > 5:
            flicker = False
    else:
        counter = 0
        flicker = True

    draw_board()

    draw_player()

    center_x = player_x + 23
    center_y = player_y + 24
    turns_allowed = check_position(center_x, center_y)

    for event in pygame.event.get():
        # to leave loop by cross
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction

    pygame.display.flip()
pygame.quit()