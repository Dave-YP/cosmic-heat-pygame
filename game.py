import pygame

from game_objects import Bullet, Player, Enemy
from game_controls import move_player
from constants import WIDTH, HEIGHT, FPS
from game_functions import show_game_over, show_game_win, music_background, reset_game_state

pygame.init()
music_background()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Capital 2050")
clock = pygame.time.Clock()
background_img = pygame.image.load('images/background.jpg').convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
bullets = pygame.sprite.Group()

enemy_img = pygame.image.load('images/enemy.png').convert_alpha()
enemies = pygame.sprite.Group()
for j in range(2):
    for i in range(12):
        enemy = Enemy(i * 100 + 30 + 50, j * 100 + 30, enemy_img)
        enemies.add(enemy)

enemy_group = pygame.sprite.Group()
for enemy in enemies:
    enemy_group.add(enemy)

player = Player()

running = True
bullet_counter = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_counter < 40:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    bullets.add(bullet)
                    bullet_counter += 1
                    if player.original_image != None:
                        player.image = player.original_image.copy()
                        player.image.fill((255, 0, 0), special_flags=pygame.BLEND_ADD)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and player.original_image != None:
                player.image = player.original_image.copy()

    keys = pygame.key.get_pressed()

    move_player(keys, player)

    screen.blit(background_img, (0, 0))

    if len(enemy_group) == 0:
        show_game_win()
        enemy_group, bullets, bullet_counter = reset_game_state(enemies, enemy_img)

    if bullet_counter == 40:
        show_game_over()
        enemy_group, bullets, bullet_counter = reset_game_state(enemies, enemy_img)

    bullet_counter_surface = pygame.font.SysFont('Arial', 30).render(f'Запас ракет: {40 - bullet_counter}/40', True, (255, 255, 255))
    screen.blit(bullet_counter_surface, (10, 10))
    for enemy in enemy_group:
        enemy.update()
        screen.blit(enemy.image, enemy.rect)

        if enemy.rect.colliderect(player.rect):
            show_game_over()
            enemy_group, bullets, bullet_counter = reset_game_state(enemies, enemy_img)
    player_image_copy = player.image.copy()
    screen.blit(player_image_copy, player.rect)
    for bullet in bullets:
        bullet.update(enemy_group)
        screen.blit(bullet.image, bullet.rect)
        if bullet.rect.bottom < 0:
            bullet.kill()
            bullet_counter -= 1

    pygame.display.flip()

    clock.tick(FPS)

pygame.mixer.music.stop()
pygame.quit()
