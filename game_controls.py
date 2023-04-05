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

def move_player_with_joystick(joystick, player):
    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1)

    if abs(x_axis) > 0.1:
        new_x = player.rect.x + x_axis * player.speed
        if new_x < 0:
            new_x = 0
        elif new_x > WIDTH - player.rect.width:
            new_x = WIDTH - player.rect.width
        player.rect.x = new_x

    if abs(y_axis) > 0.1:
        new_y = player.rect.y + y_axis * player.speed
        if new_y < 0:
            new_y = 0
        elif new_y > HEIGHT - player.rect.height:
            new_y = HEIGHT - player.rect.height
        player.rect.y = new_y