from variables import screen, direction,player_images, player_x, player_y, counter
import pygame

def draw_player():
    if direction == 0: # RIGHT
        screen.blit(player_images[counter // 5], (player_x, player_y))
    if direction == 1: # LEFT
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    if direction == 2: # UP
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    if direction == 3: # DOWN
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))
