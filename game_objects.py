import pygame
from constants import WIDTH, HEIGHT, ENEMY_FORCE
import random


class BulletRefill(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1
        self.direction_x = random.choice([-2, 2])
        self.direction_y = random.choice([-2, 2])
        self.sound_effect = pygame.mixer.Sound("game_sounds/bullet_refill.wav")

    def update(self):
        self.rect.y += self.speed * self.direction_y
        self.rect.x += self.speed * self.direction_x

        if random.randint(0, 100) == 0:
            self.direction_x *= -1
            self.direction_y *= -1

        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, WIDTH)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, HEIGHT)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class HealthRefill(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1
        self.direction_x = random.choice([-2, 2])
        self.direction_y = random.choice([-2, 2])
        self.sound_effect = pygame.mixer.Sound("game_sounds/health_refill.wav")

    def update(self):
        self.rect.y += self.speed * self.direction_y
        self.rect.x += self.speed * self.direction_x

        if random.randint(0, 100) == 0:
            self.direction_x *= -1
            self.direction_y *= -1

        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, WIDTH)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, HEIGHT)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Speed(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1
        self.direction_x = random.choice([-2, 2])
        self.direction_y = random.choice([-2, 2])
        self.sound_effect = pygame.mixer.Sound("game_sounds/health_refill.wav")

    def update(self):
        self.rect.y += self.speed * self.direction_y
        self.rect.x += self.speed * self.direction_x

        if random.randint(0, 100) == 0:
            self.direction_x *= -1
            self.direction_y *= -1

        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, WIDTH)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, HEIGHT)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - 100, HEIGHT - 100, 100, 100)
        self.speed = 10
        self.image = pygame.image.load('images/player.png').convert_alpha()
        self.original_image = self.image.copy()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, explosion_images):
        super().__init__()
        self.explosion_images = explosion_images
        self.image = self.explosion_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
        self.explosion_sounds = [
            pygame.mixer.Sound('game_sounds/explosions/explosion1.wav'),
            pygame.mixer.Sound('game_sounds/explosions/explosion2.wav'),
            pygame.mixer.Sound('game_sounds/explosions/explosion3.wav')
        ]
        self.explosion_sound = random.choice(self.explosion_sounds)
        self.sound_played = False

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosion_images):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_images[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
                if not self.sound_played:
                    self.explosion_sound.play()
                    self.sound_played = True


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 4
        self.direction = random.choice([(-1, -1), (-1, 1), (1, -1), (1, 1)])

    def update(self, enemy_group):
        dx, dy = self.direction
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        if self.rect.left < 5:
            self.rect.left = 5
            self.direction = random.choice([(1, 0), (0, -1), (0, 1), (1, -1), (1, 1)])
        elif self.rect.right > WIDTH - 5:
            self.rect.right = WIDTH - 5
            self.direction = random.choice([(-1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1)])

        if self.rect.top < 5:
            self.rect.top = 5
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (1, 1), (-1, 1)])
        elif self.rect.bottom > HEIGHT - 5:
            self.rect.bottom = HEIGHT - 5
            self.direction = random.choice([(1, 0), (-1, 0), (0, -1), (1, -1), (-1, -1)])

        collided_with = pygame.sprite.spritecollide(self, enemy_group, False)
        for other_enemy in collided_with:
            if other_enemy != self:
                distance_vec = pygame.math.Vector2(other_enemy.rect.center) - pygame.math.Vector2(self.rect.center)
                distance = distance_vec.length()
                angle = distance_vec.angle_to(pygame.math.Vector2(1, 0))

                repel_vec = pygame.math.Vector2(1, 0).rotate(angle)
                repel_vec *= (1 - (distance / (self.rect.width + other_enemy.rect.width)))
                repel_vec *= ENEMY_FORCE

                self_dir = pygame.math.Vector2(self.direction)
                other_dir = pygame.math.Vector2(other_enemy.direction)

                if distance != 0:
                    new_dir = self_dir.reflect(distance_vec).normalize()
                    other_new_dir = other_dir.reflect(-distance_vec).normalize()

                    self.direction = new_dir.x, new_dir.y
                    other_enemy.direction = other_new_dir.x, other_new_dir.y

                self.rect.move_ip(-repel_vec.x, -repel_vec.y)
                other_enemy.rect.move_ip(repel_vec.x, repel_vec.y)
