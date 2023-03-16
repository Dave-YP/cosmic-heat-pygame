import pygame
import random

from game_objects import Enemy, Player, Explosion, BulletRefill, HealthRefill, Meteors, Bullet
from game_controls import move_player
from constants import WIDTH, HEIGHT, FPS, ENEMY_SUM, ENEMY_ROW
from game_functions import show_game_over, create_enemies, music_background, reset_game_state


pygame.init()
music_background()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Capital 2050")
clock = pygame.time.Clock()

explosions = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_refill_group = pygame.sprite.Group()
health_refill_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()

bg_y_shift = -HEIGHT
background_img = pygame.image.load('images/background.jpg').convert()
background_img_top = background_img.copy()
background_img_top_rect = background_img_top.get_rect(topleft=(0, bg_y_shift))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

explosion_images = [pygame.image.load(f"images/explosion/explosion{i}.png") for i in range(18)]
enemy_img = [
    pygame.image.load('images/enemy1.png').convert_alpha(),
    pygame.image.load('images/enemy2.png').convert_alpha(),
    pygame.image.load('images/enemy3.png').convert_alpha()
]
health_refill_img = pygame.image.load('images/health.png').convert_alpha()
bullet_refill_img = pygame.image.load('images/bullet_refill.png').convert_alpha()
meteor_imgs = [
    pygame.image.load('images/meteors/meteor1.png').convert_alpha(),
    pygame.image.load('images/meteors/meteor2.png').convert_alpha(),
    pygame.image.load('images/meteors/meteor3.png').convert_alpha()
]

initial_player_pos = (WIDTH // 2, HEIGHT - 100)

score = 0
player = Player()
player_life = 100
bullet_counter = 100

for enemy in enemies:
    enemy_group.add(enemy)

for j in range(ENEMY_ROW):
    for i in range(ENEMY_SUM):
        img = random.choice(enemy_img)
        enemy = Enemy(i * 100 + 30 + 50, j * 100 + 30, img)
        enemies.add(enemy) 
enemy_group = pygame.sprite.Group()
for enemy in enemies:
    enemy_group.add(enemy)

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:

                if bullet_counter > 0:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    bullets.add(bullet)
                    bullet_counter -= 1
                    if player.original_image is not None:
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

    # random objects (BulletRefill, HealthRefill, Meteors)
    if random.randint(0, 500) == 0:
        bullet_refill = BulletRefill(
            random.randint(50, WIDTH - 50),
            random.randint(-HEIGHT, -50),
            bullet_refill_img,
        )
        bullet_refill_group.add(bullet_refill)

    if random.randint(0, 500) == 0:
        health_refill = HealthRefill(
            random.randint(30, WIDTH - 30),
            random.randint(-HEIGHT, -31),
            health_refill_img,
        )
        health_refill_group.add(health_refill)

    if random.randint(0, 200) == 0:
        meteor_img = random.choice(meteor_imgs)
        meteor_object = Meteors(
            random.randint(100, WIDTH - 50),
            random.randint(-HEIGHT, -50 - meteor_img.get_rect().height),
            meteor_img,
        )
        meteor_object.speed = random.randint(4, 10)
        meteor_group.add(meteor_object)

    if player_life <= 0:
        show_game_over(score)
        enemy_group, bullets, bullet_counter, player_life, score = reset_game_state(enemies, enemy_img)
        player.rect.topleft = initial_player_pos
        bullet_refill_group.empty()
        health_refill_group.empty()
        meteor_group.empty()

    if len(enemy_group) == 2:
        # show_game_win()
        enemy_group, bullets = create_enemies(enemies, enemy_img)

# 777
    for bullet_refill in bullet_refill_group:

        bullet_refill.update()
        bullet_refill.draw(screen)

        if player.rect.colliderect(bullet_refill.rect):
            if bullet_counter < 100:
                bullet_counter += 10
                if bullet_counter > 100:
                    bullet_counter = 100
                bullet_refill.kill()
                bullet_refill.sound_effect.play()
            else:
                bullet_refill.kill()
                bullet_refill.sound_effect.play()

    for health_refill in health_refill_group:
        health_refill.update()
        health_refill.draw(screen)

        if player.rect.colliderect(health_refill.rect):
            if player_life < 100:
                player_life += 10
                if player_life > 100:
                    player_life = 100
                health_refill.kill()
                health_refill.sound_effect.play()
            else:
                health_refill.kill()
                health_refill.sound_effect.play()

    for meteor_object in meteor_group:
        meteor_object.update()
        meteor_object.draw(screen)

        if meteor_object.rect.colliderect(player.rect):
            player_life -= 10
            explosion = Explosion(meteor_object.rect.center, explosion_images)
            explosions.add(explosion)
            meteor_object.kill()

    for enemy in enemy_group:
        enemy.update(enemy_group)
        screen.blit(enemy.image, enemy.rect)

        if enemy.rect.colliderect(player.rect):
            player_life -= 10
            explosion = Explosion(enemy.rect.center, explosion_images)
            explosions.add(explosion)
            enemy.kill()

    player_image_copy = player.image.copy()
    screen.blit(player_image_copy, player.rect)

    for explosion in explosions:
        explosion.update()
        screen.blit(explosion.image, explosion.rect)

    for bullet in bullets:
        bullet.update()
        screen.blit(bullet.image, bullet.rect)

        if bullet.rect.bottom < 0:
            bullet.kill()
            bullet_counter -= 1

        enemy_collisions = pygame.sprite.spritecollide(bullet, enemy_group, True)
        for enemy_collision in enemy_collisions:
            explosion = Explosion(enemy_collision.rect.center, explosion_images)
            explosions.add(explosion)
            bullet.kill()
            score += 50

        meteor_collisions = pygame.sprite.spritecollide(bullet, meteor_group, True)
        for meteor_collision in meteor_collisions:
            explosion = Explosion(meteor_collision.rect.center, explosion_images)
            explosions.add(explosion)
            bullet.kill()
            score += 50

    player_life_surface = pygame.font.SysFont('Impact', 30).render(f'HEALTH: {player_life}', True, (255, 255, 255))
    life_x_pos = 10
    screen.blit(player_life_surface, (life_x_pos, 10))

    bullet_counter_surface = pygame.font.SysFont('Impact', 30).render(f'BULLETS: {bullet_counter}', True, (255, 255, 255))
    bullet_x_pos = 10
    bullet_y_pos = player_life_surface.get_height() + 20
    screen.blit(bullet_counter_surface, (bullet_x_pos, bullet_y_pos))

    score_surface = pygame.font.SysFont('Impact', 30).render(f'SCORE: {score}', True, (255, 255, 255))
    score_x_pos = WIDTH - score_surface.get_width() - 10
    score_y_pos = 10
    screen.blit(score_surface, (score_x_pos, score_y_pos))

    pygame.display.flip()

    clock.tick(FPS)

pygame.mixer.music.stop()
pygame.quit()
