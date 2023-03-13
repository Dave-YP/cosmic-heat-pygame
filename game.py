import pygame
import random

from game_objects import Enemy, Player, Explosion, BulletRefill
from game_controls import move_player
from constants import WIDTH, HEIGHT, FPS, ENEMY_SUM, ENEMY_ROW
from game_functions import show_game_over, create_enemies, music_background, reset_game_state


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/bullet.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y - 10
        self.speed = 10
        self.shoot_sound = pygame.mixer.Sound('game_sounds/shooting/shoot.wav')
        self.shoot_sound.play()

    def update(self, enemies_group):
        self.rect.move_ip(0, -self.speed)

        for enemy in pygame.sprite.spritecollide(self, enemies_group, True):
            explosion = Explosion(enemy.rect.center, explosion_images)
            explosions.add(explosion)
            self.kill()
            enemy.kill()
            global score
            score += 50

        if self.rect.bottom <= 0:
            self.kill()


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

bg_y_shift = -HEIGHT
background_img = pygame.image.load('images/background.jpg').convert()
background_img_top = background_img.copy()
background_img_top_rect = background_img_top.get_rect(topleft=(0, bg_y_shift))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

explosion_images = [pygame.image.load(f"images/explosion/explosion{i}.png") for i in range(18)]
enemy_img = pygame.image.load('images/enemy.png').convert_alpha()
bullet_refill_img = pygame.image.load('images/ammo.png').convert_alpha()

initial_player_pos = (WIDTH // 2, HEIGHT - 100)
score = 0

for enemy in enemies:
    enemy_group.add(enemy)

for j in range(ENEMY_ROW):
    for i in range(ENEMY_SUM):
        enemy = Enemy(i * 100 + 30 + 50, j * 100 + 30, enemy_img)
        enemies.add(enemy)
enemy_group = pygame.sprite.Group()
for enemy in enemies:
    enemy_group.add(enemy)


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
                if bullet_counter < 100:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    bullets.add(bullet)
                    bullet_counter += 1
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

    if random.randint(0, 400) == 0:
        bullet_refill = BulletRefill(
            random.randint(30, WIDTH - 30),
            random.randint(-HEIGHT, -31),
            bullet_refill_img,
        )
        bullet_refill_group.add(bullet_refill)

    if len(enemy_group) == 10:
        # show_game_win()
        enemy_group, bullets = create_enemies(enemies, enemy_img)
        # player.rect.topleft = initial_player_pos

    # if bullet_counter == 50:
    #    show_game_over(score)
    #    enemy_group, bullets, bullet_counter, player_life, score = reset_game_state(enemies, enemy_img)

    player_life_surface = pygame.font.SysFont('Impact', 20).render(f'HEALTH: {player_life}', True, (255, 255, 255))
    life_x_pos = 10
    screen.blit(player_life_surface, (life_x_pos, 10))

    bullet_counter_surface = pygame.font.SysFont('Impact', 20).render(f'BULLETS: {100 - bullet_counter}', True, (255, 255, 255))
    bullet_x_pos = 10
    bullet_y_pos = player_life_surface.get_height() + 20
    screen.blit(bullet_counter_surface, (bullet_x_pos, bullet_y_pos))

    score_surface = pygame.font.SysFont('Impact', 20).render(f'SCORE: {score}', True, (255, 255, 255))
    score_x_pos = 10
    score_y_pos = bullet_y_pos + bullet_counter_surface.get_height() + 10
    screen.blit(score_surface, (score_x_pos, score_y_pos))

    for bullet_refill in bullet_refill_group:

        bullet_refill.update()
        bullet_refill.draw(screen)

        if player.rect.colliderect(bullet_refill.rect):
            bullet_counter -= 10
            bullet_refill.kill()

    for enemy in enemy_group:
        enemy.update(enemy_group)
        screen.blit(enemy.image, enemy.rect)

        if enemy.rect.colliderect(player.rect):
            player_life -= 10
            if player_life <= 0:
                show_game_over(score)
                enemy_group, bullets, bullet_counter, player_life, score = reset_game_state(enemies, enemy_img)
                player.rect.topleft = initial_player_pos
            else:
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
