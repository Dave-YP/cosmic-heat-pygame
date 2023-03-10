import pygame
from constants import WIDTH, HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))


def music_background():
    pygame.mixer.music.load('game_sounds/background_music.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)


def show_game_over():
    font = pygame.font.Font(None, 200)
    text = font.render("Game Over", True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.mixer.music.load('game_sounds/gameover.mp3')
    pygame.mixer.music.play()
    pygame.time.delay(3000)
    music_background()


def show_game_win():
    font = pygame.font.Font(None, 200)
    text = font.render("Победа!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.mixer.music.load('game_sounds/win.mp3')
    pygame.mixer.music.play()
    pygame.time.delay(4000)
    music_background()
