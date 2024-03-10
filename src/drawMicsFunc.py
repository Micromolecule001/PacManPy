from .variables import font, screen, powerup, lives, score, player_images
import pygame

def draw_misc():

    """
        drawing blue ghosts while powerup and showing lives, score, and other UI texts
    """
    
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))
