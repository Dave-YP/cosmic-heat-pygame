import pygame
from game_objects import Bullet, Player, Enemy
from constants import WIDTH, HEIGHT, FPS
from game_functions import show_game_over, show_game_win, music_background

pygame.init()
music_background()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
background_img = pygame.image.load('images/background.jpg').convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
bullets = pygame.sprite.Group()

enemy_img = pygame.image.load('images/enemy.png').convert_alpha()
enemies = pygame.sprite.Group()
for j in range(3):
    for i in range(6):
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
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bullet_counter < 100:
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
    if keys[pygame.K_LEFT]:
        if player.rect.left > 0:
            player.rect.move_ip(-player.speed, 0)
    if keys[pygame.K_RIGHT]:
        if player.rect.right < WIDTH:
            player.rect.move_ip(player.speed, 0)

    screen.blit(background_img, (0, 0))

    if len(enemy_group) == 0:
        show_game_win()
        enemies = pygame.sprite.Group()
        for j in range(3):
            for i in range(6):
                enemy = Enemy(i * 100 + 30 + 50, j * 100 + 30, enemy_img)
                enemies.add(enemy)
        enemy_group = pygame.sprite.Group()
        for enemy in enemies:
            enemy_group.add(enemy)
        bullets.empty()
        bullet_counter = 0

    bullet_counter_surface = pygame.font.SysFont('Arial', 30).render(f'Запас снарядов: {100 - bullet_counter}/100', True, (255, 255, 255))
    screen.blit(bullet_counter_surface, (10, 10))
    for enemy in enemy_group:
        enemy.update()
        screen.blit(enemy.image, enemy.rect)

        if enemy.rect.colliderect(player.rect):
            show_game_over()
            bullets.empty()
            bullet_counter = 0
            running = True
            enemies = pygame.sprite.Group()
            for j in range(3):
                for i in range(6):
                    enemy = Enemy(i * 100 + 30 + 50, j * 100 + 30, enemy_img)
                    enemies.add(enemy)
        enemy_group = pygame.sprite.Group()
        for enemy in enemies:
            enemy_group.add(enemy)
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
