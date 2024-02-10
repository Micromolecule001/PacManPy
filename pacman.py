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

# ghosts
ghost_move_delay = 10
last_ghost_move = pygame.time.get_ticks()
ghosts = []
for color in [(255, 0, 0), (255, 165, 0), (255, 192, 203), (173, 216, 230)]:  # Red, Orange, Pink, Lightblue
    ghost = pygame.Rect(screen_w // 2, screen_h // 2, 25, 25)  # Spawn in the center
    ghosts.append((ghost, color))

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

    # Draw ghosts
    for ghost, color in ghosts:
        pygame.draw.rect(screen, color, ghost)

    # THE LOOP 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Ghosts movement
            
    current_time = pygame.time.get_ticks()
    # Calculate time elapsed since the last ghost move
    elapsed_time = current_time - last_ghost_move

    # Check if enough time has passed to move the ghosts
    if elapsed_time >= ghost_move_delay:  
        for ghost, _ in ghosts:
            # List of possible directions to move
            possible_directions = []

            # Get current position of the ghost
            x, y = ghost.x, ghost.y
            
            # Check if moving left is possible
            if game_map[y // cell_size][(x - 1) // cell_size] != '#':
                possible_directions.append('left')
            # Check if moving right is possible
            if game_map[y // cell_size][(x + 1) // cell_size] != '#':
                possible_directions.append('right')
            # Check if moving up is possible
            if game_map[(y - 1) // cell_size][x // cell_size] != '#':
                possible_directions.append('up')
            # Check if moving down is possible
            if game_map[(y + 1) // cell_size][x // cell_size] != '#':
                possible_directions.append('down')
            
            # Choose a random direction from the possible directions
            if possible_directions:
                direction = random.choice(possible_directions)
                if direction == 'left':
                    ghost.x -= 1
                elif direction == 'right':
                    ghost.x += 1
                elif direction == 'up':
                    ghost.y -= 1
                elif direction == 'down':
                    ghost.y += 1
            
            last_ghost_move = current_time  # Update the time of the last ghost move

    # hits
    for ghost, _ in ghosts:
        if pacman.colliderect(ghost):
            hit_counter += 1
            pacman.x = 60 
            pacman.y = 60
            if hit_counter >= 3:
                pacman_lives -= 1
                hit_counter = 0
                if pacman_lives == 0:
                    print("Game Over")
                    running = False
                    break

    # pacman eating points
    if game_map[pacman.centery // cell_size][pacman.centerx // cell_size] == '.':
        game_map[pacman.centery // cell_size][pacman.centerx // cell_size] = ' '

    score += 1
    
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

    # Check if all points have been collected 
    points_left = sum(row.count('.') for row in game_map)
    if points_left == 0:
        print("Congratulations! You've collected all points!")
        running = False

    # if not -- will be nothing 
    pygame.display.update()

pygame.quit()
