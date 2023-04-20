import pygame
import random

from .constants import WIDTH, HEIGHT


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
        self.sound_effect = pygame.mixer.Sound("game_sounds/refill/bullet_refill.wav")
        self.sound_effect.set_volume(0.4)

    def update(self):
        self.rect.y += self.speed * self.direction_y
        self.rect.x += self.speed * self.direction_x
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, WIDTH)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, HEIGHT)
        if random.randint(0, 50) == 0:
            self.direction_x *= - 1
            self.direction_y *= - 1

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
        self.sound_effect = pygame.mixer.Sound("game_sounds/refill/health_refill.wav")
        self.sound_effect.set_volume(0.4)

    def update(self):
        self.rect.y += self.speed * self.direction_y
        self.rect.x += self.speed * self.direction_x
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, WIDTH)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, HEIGHT)
        if random.randint(0, 50) == 0:
            self.direction_x *= - 1
            self.direction_y *= - 1

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class DoubleRefill(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.direction_x = random.choice([-2, 2])
        self.direction_y = random.choice([-2, 2])
        self.sound_effect = pygame.mixer.Sound("game_sounds/refill/double_refill.mp3")
        self.sound_effect.set_volume(0.4)

    def update(self):
        self.rect.y += self.speed * self.direction_y
        self.rect.x += self.speed * self.direction_x
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, WIDTH)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, HEIGHT)
        if random.randint(0, 50) == 0:
            self.direction_x *= - 1
            self.direction_y *= - 1

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class ExtraScore(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()
        self.original_image = image
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.speed = 2
        self.rect.x = x
        self.rect.y = y
        self.direction_x = 0
        self.direction_y = 1
        self.sound_effect = pygame.mixer.Sound("game_sounds/refill/extra_score.mp3")
        self.sound_effect.set_volume(0.4)

    def update(self):
        self.rect.y += self.speed * self.direction_y

        if self.rect.bottom >= HEIGHT + 100:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
