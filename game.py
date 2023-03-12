import pygame
import math

from game_objects import Bullet, Player, Enemy, Explosion
from game_controls import move_player
from constants import WIDTH, HEIGHT, FPS, ENEMY_SPEED, ENEMY_SUM, ENEMY_ROW
from game_functions import show_game_over, show_game_win, music_background, reset_game_state


pygame.init()
music_background()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Capital 2050")
clock = pygame.time.Clock()
background_img = pygame.image.load('images/background.jpg').convert()
bg_y_shift = -HEIGHT
background_img_top = background_img.copy()
background_img_top_rect = background_img_top.get_rect(topleft=(0, bg_y_shift))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
bullets = pygame.sprite.Group()

enemy_img = pygame.image.load('images/enemy.png').convert_alpha()
enemies = pygame.sprite.Group()

for j in range(ENEMY_ROW):
    for i in range(ENEMY_SUM):
        enemy = Enemy(i * 100 + 30 + 50, j * 100 + 30, enemy_img)
        enemies.add(enemy)

enemy_group = pygame.sprite.Group()
for enemy in enemies:
    enemy_group.add(enemy)

explosions = pygame.sprite.Group()
explosion_images = [pygame.image.load(f"images/explosion/explosion{i}.png") for i in range(18)]

player = Player()
player_life = 100

running = True
bullet_counter = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_counter < 80:
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

    bg_y_shift += 2
    if bg_y_shift >= 0:
        bg_y_shift = -HEIGHT

    screen.blit(background_img, (0, bg_y_shift))
    screen.blit(background_img_top, background_img_top_rect)

    background_img_top_rect.top = bg_y_shift + HEIGHT

    if len(enemy_group) == 0:
        show_game_win()
        enemy_group, bullets, bullet_counter, player_life = reset_game_state(enemies, enemy_img)

    if bullet_counter == 70:
        show_game_over()
        enemy_group, bullets, bullet_counter, player_life = reset_game_state(enemies, enemy_img)

    player_life_surface = pygame.font.SysFont('Impact', 20).render(f'ЖИЗНЬ: {player_life}', True, (255, 255, 255))
    life_x_pos = 10
    screen.blit(player_life_surface, (life_x_pos, 10))

    bullet_counter_surface = pygame.font.SysFont('Impact', 20).render(f'ЛАЗЕРЫ: {70 - bullet_counter}/70', True, (255, 255, 255))
    bullet_x_pos = 10
    bullet_y_pos = player_life_surface.get_height() + 20
    screen.blit(bullet_counter_surface, (bullet_x_pos, bullet_y_pos))

    enemy_font = pygame.font.SysFont('Impact', 50)
    enemy_counter_surface = enemy_font.render(f'ВРАГИ: {len(enemy_group)}', True, (255, 255, 255))
    counter_x_pos = WIDTH - enemy_counter_surface.get_width() - 10
    screen.blit(enemy_counter_surface, (counter_x_pos, 10))


    for enemy in enemy_group:
        enemy.update()
        screen.blit(enemy.image, enemy.rect)

        if enemy.rect.colliderect(player.rect):
            player_life -= 20
            if player_life <= 0:
                show_game_over()
                enemy_group, bullets, bullet_counter, player_life = reset_game_state(enemies, enemy_img)
            else:
                dx = enemy.rect.centerx - player.rect.centerx
                dy = enemy.rect.centery - player.rect.centery
                dist = math.hypot(dx, dy)
                angle = math.atan2(dy, dx)
                vx = math.cos(angle) * ENEMY_SPEED
                vy = math.sin(angle) * ENEMY_SPEED
                enemy.rect.x += vx
                enemy.rect.y += vy

                explosion = Explosion(enemy.rect.center, explosion_images)
                explosions.add(explosion)
                enemy.kill()

    player_image_copy = player.image.copy()
    screen.blit(player_image_copy, player.rect)

    for explosion in explosions:
        explosion.update()
        screen.blit(explosion.image, explosion.rect)

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
