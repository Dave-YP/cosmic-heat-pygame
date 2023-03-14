import pygame
from constants import WIDTH, HEIGHT


def move_player(keys, player):
    if keys[pygame.K_LEFT]:
        if player.rect.left > 0:
            player.rect.move_ip(-player.speed, 0)
    if keys[pygame.K_RIGHT]:
        if player.rect.right < WIDTH:
            player.rect.move_ip(player.speed, 0)
    if keys[pygame.K_UP]:
        if player.rect.top > 0:
            player.rect.move_ip(0, -player.speed)
    if keys[pygame.K_DOWN]:
        if player.rect.bottom < HEIGHT:
            player.rect.move_ip(0, player.speed)