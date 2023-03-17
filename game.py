import pygame
import random

from game_objects import Enemy1, Player, Explosion, BulletRefill, HealthRefill, Meteors, Bullet, DoubleRefill, ExtraScore
from game_controls import move_player
from constants import WIDTH, HEIGHT, FPS
from game_functions import show_game_over, music_background


pygame.init()
music_background()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Capital 2050")
clock = pygame.time.Clock()

explosions = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy1_group = pygame.sprite.Group()
bullet_refill_group = pygame.sprite.Group()
health_refill_group = pygame.sprite.Group()
double_refill_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()
extra_score_group = pygame.sprite.Group()

bg_y_shift = -HEIGHT
background_img = pygame.image.load('images/background.jpg').convert()
background_img_top = background_img.copy()
background_img_top_rect = background_img_top.get_rect(topleft=(0, bg_y_shift))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

explosion_images = [pygame.image.load(f"images/explosion/explosion{i}.png") for i in range(18)]
enemy1_img = [
    pygame.image.load('images/enemy1/enemy1.png').convert_alpha(),
    pygame.image.load('images/enemy1/enemy2.png').convert_alpha(),
    pygame.image.load('images/enemy1/enemy3.png').convert_alpha()
]
health_refill_img = pygame.image.load('images/refill/health_refill.png').convert_alpha()
bullet_refill_img = pygame.image.load('images/refill/bullet_refill.png').convert_alpha()
double_refill_img = pygame.image.load('images/refill/double_refill.png').convert_alpha()
meteor_imgs = [
    pygame.image.load('images/meteors/meteor1.png').convert_alpha(),
    pygame.image.load('images/meteors/meteor2.png').convert_alpha(),
    pygame.image.load('images/meteors/meteor3.png').convert_alpha(),
    pygame.image.load('images/meteors/meteor4.png').convert_alpha()
]
extra_score_img = pygame.image.load('images/score/score_coin.png').convert_alpha()

initial_player_pos = (WIDTH // 2, HEIGHT - 100)

score = 0
hi_score = 0
player = Player()
player_life = 100
bullet_counter = 100

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

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and player.original_image != None:
                player.image = player.original_image.copy()

    keys = pygame.key.get_pressed()
    move_player(keys, player)

    bg_y_shift += 1
    if bg_y_shift >= 0:
        bg_y_shift = -HEIGHT

    if score > 1000:
       bg_y_shift += 2

    screen.blit(background_img, (0, bg_y_shift))
    screen.blit(background_img_top, background_img_top_rect)
    background_img_top_rect.top = bg_y_shift + HEIGHT

    if score > hi_score:
        hi_score = score

    # random objects (BulletRefill, HealthRefill, DoubleRefill, Meteors)
    if random.randint(0, 50) == 0:
        enemy_img = random.choice(enemy1_img)
        enemy_object = Enemy1(
            random.randint(100, WIDTH - 50),
            random.randint(-HEIGHT, -50),
            enemy_img,
        )
        enemy1_group.add(enemy_object)


    if random.randint(0, 50) == 0:
        extra_score = ExtraScore(
            random.randint(50, WIDTH - 50),
            random.randint(-HEIGHT, -50 - extra_score_img.get_rect().height),
            extra_score_img,
        )

        extra_score_group.add(extra_score)

    if random.randint(0, 100) == 0:
        meteor_img = random.choice(meteor_imgs)
        meteor_object = Meteors(
            random.randint(100, WIDTH - 50),
            random.randint(-HEIGHT, -50 - meteor_img.get_rect().height),
            meteor_img,
        )
        meteor_group.add(meteor_object)

    if player_life <= 0:
        show_game_over(score)
        score = 0
        player_life = 100
        bullet_counter = 100
        player.rect.topleft = initial_player_pos
        bullets.empty()
        bullet_refill_group.empty()
        health_refill_group.empty()
        double_refill_group.empty()
        extra_score_group.empty()
        meteor_group.empty()
        enemy1_group.empty()
        explosions.empty()
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

    for extra_score in extra_score_group:
        extra_score.update()
        extra_score.draw(screen)

        if player.rect.colliderect(extra_score.rect):
            score += 10
            extra_score.kill()
            extra_score.sound_effect.play()

        if score >= 1000:
            extra_score.speed = 4
        if score >= 2000:
            extra_score.speed = 6
        if score >= 4000:
            extra_score.speed = 8
        if score >= 6000:
            extra_score.speed = 10

        # print(f"Extra Score speed: {extra_score.speed:.2f}")

    for double_refill in double_refill_group:
        double_refill.update()
        double_refill.draw(screen)

        if player.rect.colliderect(double_refill.rect):
            if player_life < 100:
                player_life += 50
                if player_life > 100:
                    player_life = 100
                bullet_counter += 50
                if bullet_counter > 100:
                    bullet_counter = 100
                double_refill.kill()
                double_refill.sound_effect.play()
            else:
                double_refill.kill()
                double_refill.sound_effect.play()

    for meteor_object in meteor_group:
        meteor_object.update()
        meteor_object.draw(screen)

        if meteor_object.rect.colliderect(player.rect):
            player_life -= 10
            explosion = Explosion(meteor_object.rect.center, explosion_images)
            explosions.add(explosion)
            meteor_object.kill()

        bullet_collisions = pygame.sprite.spritecollide(meteor_object, bullets, True)
        for bullet_collision in bullet_collisions:
            explosion = Explosion(meteor_object.rect.center, explosion_images)
            explosions.add(explosion)
            meteor_object.kill()
            score += 30

            if random.randint(0, 4) == 0:
                double_refill = DoubleRefill(
                    meteor_object.rect.centerx,
                    meteor_object.rect.centery,
                    double_refill_img,
                )
                double_refill_group.add(double_refill)

        if score >= 1000:
            meteor_object.speed = 4
        if score >= 2000:
            meteor_object.speed = 6
        if score >= 4000:
            meteor_object.speed = 8
        if score >= 8000:
            meteor_object.speed = 10
        # print(f"Meteor Score speed: {meteor_object.speed:.2f}")

    for enemy_object in enemy1_group:
        enemy_object.update(enemy1_group)
        enemy1_group.draw(screen)

        if enemy_object.rect.colliderect(player.rect):
            player_life -= 10
            explosion = Explosion(enemy_object.rect.center, explosion_images)
            explosions.add(explosion)
            enemy_object.kill()

        bullet_collisions = pygame.sprite.spritecollide(enemy_object, bullets, True)
        for bullet_collision in bullet_collisions:
            explosion = Explosion(enemy_object.rect.center, explosion_images)
            explosions.add(explosion)
            enemy_object.kill()
            score += 50

            if random.randint(0, 4) == 0:
                bullet_refill = BulletRefill(
                    enemy_object.rect.centerx,
                    enemy_object.rect.centery,
                    bullet_refill_img,
                )
                double_refill_group.add(bullet_refill)

            if random.randint(0, 300) == 0:
                health_refill = HealthRefill(
                    random.randint(50, WIDTH - 30),
                    random.randint(-HEIGHT, -30),
                    health_refill_img,
                )
                health_refill_group.add(health_refill)

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

    player_life_surface = pygame.font.SysFont('Impact', 20).render(f'HEALTH: {player_life}', True, (152, 251, 152))
    life_x_pos = 10
    screen.blit(player_life_surface, (life_x_pos, 10))

    bullet_counter_surface = pygame.font.SysFont('Impact', 20).render(f'BULLETS: {bullet_counter}', True, (176, 196, 222))
    bullet_x_pos = 10
    bullet_y_pos = player_life_surface.get_height() + 20
    screen.blit(bullet_counter_surface, (bullet_x_pos, bullet_y_pos))

    score_surface = pygame.font.SysFont('Impact', 30).render(f'{score}', True, (238, 232, 170))
    score_image_rect = score_surface.get_rect()
    score_image_rect.x, score_image_rect.y = WIDTH - score_image_rect.width - extra_score_img.get_width() - 10, 10

    screen.blit(extra_score_img, (score_image_rect.right + 5, score_image_rect.centery - extra_score_img.get_height()//2))
    screen.blit(score_surface, score_image_rect)

    hi_score_surface = pygame.font.SysFont('Impact', 20).render(f'HI-SCORE: {hi_score}', True, (255, 192, 203))
    hi_score_x_pos = 10
    hi_score_y_pos = bullet_counter_surface.get_height() + 60
    screen.blit(hi_score_surface, (hi_score_x_pos, hi_score_y_pos))

    pygame.display.flip()

    clock.tick(FPS)

pygame.mixer.music.stop()
pygame.quit()
