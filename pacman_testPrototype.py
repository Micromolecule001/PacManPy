import pygame
import random

pygame.init()

# pygame options
pygame.display.set_caption('Pacman')

# screen options 
screen_w = 950
screen_h = 950
cell_size = 50 
score = 0

screen = pygame.display.set_mode((screen_w, screen_h))

# Define the game map
game_map = [
    list("###################"),
    list("#.......#.....#...#"),
    list("#.#.###...###.#.#.#"),
    list("#.......#.......#.#"),
    list("###.#.#####.#####.#"),
    list("#...#...#.........#"),
    list("#.#.###.#.###.###.#"),
    list("#.#...........#...#"),
    list("#.###.### ###...###"),
    list("#.#...### ###.#...#"),
    list("#.#.#.#######.#.#.#"),
    list("#...............#.#"),
    list("###.###.#.###.###.#"),
    list("#...#...#.........#"),
    list("#.#.#.#####.#.###.#"),
    list("#.#.#...#...#...#.#"),
    list("###.#.#...#.#.#.#.#"),
    list("#.....#.#.#...#...#"),
    list("###################")
]

# Count the number of points on the map
total_points = sum(row.count('.') for row in game_map)

# Draw the game map
def draw_map():
    for y, row in enumerate(game_map):
        for x, char in enumerate(row):
            if char == '#':  # wall
                pygame.draw.rect(screen, (20, 20, 100), (x * cell_size, y * cell_size, cell_size, cell_size))
            elif char == '.':  # point
                pygame.draw.circle(screen, (255, 255, 255), (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), 3)
            elif char == 'o':  # empty space
                pygame.draw.rect(screen, (0, 0, 40), (x * cell_size, y * cell_size, cell_size, cell_size))
            

# pacman object
pacman = pygame.Rect((60, 60, 25, 25))
speed = 3
pacman_lives = 3
hit_counter = 0

# game loop
running = True
while running: 
    
    # no trails 
    screen.fill((0, 0, 40))

    # limit frame rate to control speed
    pygame.time.Clock().tick(60)

    # Draw game map
    draw_map()

    # Draw "pacman"
    pygame.draw.rect(screen, (255, 255, 0), pacman)

    # THE LOOP 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    
    
    # PAC's MOVING
            
    # get the key from user
    key = pygame.key.get_pressed()

    # moving system (strong)
    if key[pygame.K_LEFT] and pacman.left > 0 and game_map[(pacman.top + pacman.height // 2) // cell_size][(pacman.left - speed) // cell_size] != '#':
        pacman.move_ip(-speed, 0)
    elif key[pygame.K_RIGHT] and pacman.right < screen_w and game_map[(pacman.top + pacman.height // 2) // cell_size][(pacman.right + speed) // cell_size] != '#':
        pacman.move_ip(speed, 0)
    elif key[pygame.K_UP] and pacman.top > 0 and game_map[(pacman.top - speed) // cell_size][(pacman.left + pacman.width // 2) // cell_size] != '#':
        pacman.move_ip(0, -speed)
    elif key[pygame.K_DOWN] and pacman.bottom < screen_h and game_map[(pacman.bottom + speed) // cell_size][(pacman.left + pacman.width // 2) // cell_size] != '#':
        pacman.move_ip(0, speed)


    # POINTS

    # pacman eating points
    if game_map[pacman.centery // cell_size][pacman.centerx // cell_size] == '.':
        game_map[pacman.centery // cell_size][pacman.centerx // cell_size] = ' '

    # score...
    score += 1

    # Check if all points have been collected 
    points_left = sum(row.count('.') for row in game_map)
    if points_left == 0:
        print("Congratulations! You've collected all points!")
        running = False

    # if not -- will be nothing 
    pygame.display.update()

pygame.quit()
