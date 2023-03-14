import pygame
import random
from constants import WIDTH, HEIGHT, ENEMY_SUM, ENEMY_ROW
from game_objects import Enemy
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullets = pygame.sprite.Group()


def music_background():
    pygame.mixer.music.load('game_sounds/background_music.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)


def show_game_over(score):
    font = pygame.font.SysFont('Impact', 50)
    font_small = pygame.font.SysFont('Impact', 30)
    text = font.render("GAME OVER", True, (139, 0, 0))
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2 - 50))
    score_text = font_small.render(f"Final Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))
    screen.blit(text, text_rect)
    screen.blit(score_text, score_rect)
    pygame.display.flip()
    pygame.mixer.music.load('game_sounds/gameover.mp3')
    pygame.mixer.music.play()
    pygame.time.delay(4000)
    music_background()


def show_game_win():
    font = pygame.font.SysFont('Impact', 50)
    text = font.render("AWESOME! GO ON!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.mixer.music.load('game_sounds/win.mp3')
    pygame.mixer.music.play()
    pygame.time.delay(1000)
    music_background()


def reset_game_state(enemies, enemy_img):
    enemies.empty()
    for j in range(ENEMY_ROW):
        for i in range(ENEMY_SUM):
            img = random.choice(enemy_img)
            enemy = Enemy(i * 100 + 30 + 50, j * 100 + 30, img)
            enemies.add(enemy)

    enemy_group = pygame.sprite.Group()
    for enemy in enemies:
        enemy_group.add(enemy)

    bullets.empty()
    score = 0
    player_life = 100
    bullet_counter = 100

    return enemy_group, bullets, bullet_counter, player_life, score


def create_enemies(enemies, enemy_img):

    for j in range(ENEMY_ROW):
        for i in range(ENEMY_SUM):
            img = random.choice(enemy_img)
            enemy = Enemy(i * 100 + 30 + 50, j * 100 + 30, img)
            enemies.add(enemy)

    enemy_group = pygame.sprite.Group()
    for enemy in enemies:
        enemy_group.add(enemy)

    return enemy_group, bullets
