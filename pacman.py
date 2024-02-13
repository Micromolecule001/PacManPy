import pygame
import math
from board import boards

pygame.init()



# settings variables: screen, framerates, fonts etc...

# resolution, display
WIDTH = 900
HEIGHT = 950 
screen = pygame.display.set_mode([WIDTH, HEIGHT])

num1 = ((HEIGHT - 50) // 32 ) # column constant
num2 = (WIDTH // 30) # row constant
num3 = 15 # fat factor for the player
font = pygame.font.Font('freesansbold.ttf', 20) # font: default windows
level = boards # board array imported from board.py
color = 'blue' # color variable
PI = math.pi # pi 
flicker = False # blinker variable
turns_allowed = [False, False, False, False] # allowed way to turn
score = 0 # score 
powerup = False # state
power_counter = 0 # timer
eaten_ghosts = [False, False, False, False] # ghost states
moving = False # moving state
startup_counter = 0 # counter
lives = 3
blinky_dead = False
inky_dead = False
pinky_dead = False
clyde_dead = False
blinky_box = False
inky_box = False
pinky_box = False
clyde_box = False
ghost_speed = 2

# starting pos, speed
player_x = 450
player_y = 663
player_speed = 2

# targets of ghosts
targets = [
    (player_x, player_y),
    (player_x, player_y),
    (player_x, player_y),
    (player_x, player_y)
]

# other player variables
direction = 0
counter = 0
direction_command = 0

# framerate
timer = pygame.time.Clock()
fps = 60

# animations
player_images = []

for i in range(1, 5): 
    player_images.append(pygame.transform.scale(pygame.image.load(f'./Pacman Python/assets/player_images/{i}.png'), (45, 45)))

# ghost assets
blinky_img = pygame.transform.scale(pygame.image.load("./Pacman Python/assets/ghost_images/red.png"), (45, 45))
blinky_x = 56
blinky_y = 58
blinky_direction = 0

pinky_img = pygame.transform.scale(pygame.image.load("./Pacman Python/assets/ghost_images/pink.png"), (45, 45))
pinky_x = 440
pinky_y = 438
pinky_direction = 2

inky_img = pygame.transform.scale(pygame.image.load("./Pacman Python/assets/ghost_images/blue.png"), (45, 45))
inky_x = 440
inky_y = 388
inky_direction = 2

clyde_img = pygame.transform.scale(pygame.image.load("./Pacman Python/assets/ghost_images/orange.png"), (45, 45))
clyde_x = 440
clyde_y = 438
clyde_direction = 2

spooked_img = pygame.transform.scale(pygame.image.load("./Pacman Python/assets/ghost_images/powerup.png"), (45, 45))
dead_img = pygame.transform.scale(pygame.image.load("./Pacman Python/assets/ghost_images/dead.png"), (45, 45))





# Ghost class

class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.diretion = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()
         
    def draw(self):
        if (not powerup and not self.dead) or (eaten_ghost[self.id]):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect    

    def check_collisions(self):
        self.turns = [False, False, False, False]
        self.in_box = True
        return self.turns, self.in_box
    
# functions

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
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15
    # check collisions based on center x and center y of player +/- fudge number
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
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
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns

def move_player(play_x, play_y):
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y

def check_collisions(scor, power, power_count, eaten_ghosts):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            scor += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            scor += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
    return scor, power, power_count, eaten_ghosts

def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))

# main game loop 

run = True
while run:
    timer.tick(fps) # framerate

    if counter < 19: 
        counter += 1
        if counter > 6:
            flicker = False
    else:
        counter = 0
        flicker = True
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]
    if startup_counter < 180: 
        moving = False
        startup_counter += 1
    else: 
        moving = True
    

    screen.fill('black') #bg color
    draw_board()
    draw_player()
    draw_misc()

    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speed, blinky_img, blinky_direction, blinky_dead, blinky_box, 0)
    inky = Ghost(inky_x, inky_y, targets[0], ghost_speed, inky_img, inky_direction, inky_dead, inky_box, 0)
    pinky = Ghost(pinky_x, pinky_y, targets[0], ghost_speed, pinky_img, pinky_direction, pinky_dead, pinky_box, 0)
    clyde = Ghost(clyde_x, clyde_y, targets[0], ghost_speed, clyde_img, clyde_direction, clyde_dead, clyde_box, 0)

    center_x = player_x + 23
    center_y = player_y + 24

    turns_allowed = check_position(center_x, center_y)

    if moving: 
        player_x, player_y = move_player(player_x, player_y)

    score, powerup, power_counter, eaten_ghosts = check_collisions(score, powerup, power_counter, eaten_ghosts) # score
    

    for event in pygame.event.get():
        # to leave loop by cross
        if event.type == pygame.QUIT:
            run = False
        # event keypushing
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
        

 
    if direction_command == 0 and turns_allowed[0]:
        direction = 0 
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3

    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897

    pygame.display.flip()
pygame.quit()