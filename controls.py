import pygame
from classes.constants import WIDTH, HEIGHT


def move_player(keys, player):
    if keys[pygame.K_LEFT]:
        if keys[pygame.K_UP]:
            player.move_up_left()
        elif keys[pygame.K_DOWN]:
            player.move_down_left()
        else:
            player.move_left()
    elif keys[pygame.K_RIGHT]:
        if keys[pygame.K_UP]:
            player.move_up_right()
        elif keys[pygame.K_DOWN]:
            player.move_down_right()
        else:
            player.move_right()
    elif keys[pygame.K_UP]:
        player.move_up()
    elif keys[pygame.K_DOWN]:
        player.move_down()
    else:
        player.stop()


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
