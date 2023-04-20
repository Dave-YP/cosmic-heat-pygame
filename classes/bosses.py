import pygame
import random
import math

from .constants import WIDTH, HEIGHT


class Boss1(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 6
        self.direction = random.choice([(-1, 0), (1, 0)])
        self.shoot_timer = 0
        self.shots_fired = 0

    def update(self, enemy_bullets_group, player):
        self.rect.x += math.sin(pygame.time.get_ticks() * 0.01) * 3
        self.rect.y += math.sin(pygame.time.get_ticks() * 0.01) * 3
        if self.shots_fired < 20:
            dx, dy = self.direction
            self.rect.x += dx * self.speed
            self.rect.y = max(self.rect.y, 50)

            if self.rect.left < 5:
                self.rect.left = 5
                self.direction = (1, 0)
            elif self.rect.right > WIDTH - 5:
                self.rect.right = WIDTH - 5
                self.direction = (-1, 0)

            self.shoot_timer += 1
            if self.shoot_timer >= 60:
                bullet1 = Boss1Bullet(self.rect.centerx - 20, self.rect.bottom)
                bullet2 = Boss1Bullet(self.rect.centerx + 20, self.rect.bottom)
                bullet3 = Boss1Bullet(self.rect.centerx, self.rect.bottom)
                enemy_bullets_group.add(bullet1, bullet2, bullet3)
                self.shoot_timer = 0
                self.shots_fired += 1
        else:
            self.speed = 10
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            direction = pygame.math.Vector2(dx, dy).normalize()

            self.rect.x += direction.x * self.speed
            self.rect.y += direction.y * self.speed


class Boss1Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/bullets/bulletboss1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y + 10
        self.speed = 10
        self.shoot_sound = pygame.mixer.Sound('game_sounds/shooting/boss1shoot.mp3')
        self.shoot_sound.set_volume(0.4)
        self.shoot_sound.play()

    def update(self):
        self.rect.move_ip(0, self.speed)

        if self.rect.top > HEIGHT:
            self.kill()


class Boss2(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.direction = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)])
        self.direction_x, self.direction_y = self.direction
        self.shoot_timer = 0
        self.shots_fired = 0

    def update(self, enemy_bullets_group, player):
        self.rect.x += math.sin(pygame.time.get_ticks() * 0.01) * 2
        self.rect.y += math.sin(pygame.time.get_ticks() * 0.01) * 2
        if self.shots_fired < 20:
            dx, dy = self.direction
            if self.direction in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                self.speed = 5 / math.sqrt(2)
            else:
                self.speed = 5
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

            if self.rect.left < 5:
                self.rect.left = 5
                self.direction_x = 1
                if self.direction_y == 0:
                    self.direction_y = 1
            elif self.rect.right > WIDTH - 5:
                self.rect.right = WIDTH - 5
                self.direction_x = -1
                if self.direction_y == 0:
                    self.direction_y = 1
            elif self.rect.top < 70:
                self.rect.top = 70
                self.direction_y = 1
                if self.direction_x == 0:
                    self.direction_x = 1
            elif self.rect.bottom > HEIGHT - 5:
                self.rect.bottom = HEIGHT - 5
                self.direction_y = -1
                if self.direction_x == 0:
                    self.direction_x = 1

            self.direction = (self.direction_x, self.direction_y)
            self.shoot_timer += 1
            if self.shoot_timer >= 100:
                dx = player.rect.centerx - self.rect.centerx
                dy = player.rect.centery - self.rect.centery
                direction = pygame.math.Vector2(dx, dy).normalize()
                bullet = Boss2Bullet(self.rect.centerx, self.rect.bottom, direction)
                enemy_bullets_group.add(bullet)
                self.shoot_timer = 0
                self.shots_fired += 1
        else:
            if self.speed != 5:
                self.speed = 5 / math.sqrt(2)
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            direction = pygame.math.Vector2(dx, dy).normalize()

            self.rect.x += direction.x * self.speed
            self.rect.y += direction.y * self.speed

            self.direction_x = direction.x / abs(direction.x) if direction.x != 0 else 0
            self.direction_y = direction.y / abs(direction.y) if direction.y != 0 else 0
            self.direction = (self.direction_x, self.direction_y)


class Boss2Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, direction):
        super().__init__()
        self.image_orig = pygame.image.load('images/bullets/bulletboss2.png').convert_alpha()
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y + 10
        self.speed = 11
        self.direction = direction
        self.shoot_sound = pygame.mixer.Sound('game_sounds/shooting/boss2shoot.mp3')
        self.shoot_sound.set_volume(0.4)
        self.shoot_sound.play()

    def update(self):
        self.rect.move_ip(self.direction.x * self.speed, self.direction.y * self.speed)

        angle = math.atan2(self.direction.y, self.direction.x)
        angle = math.degrees(angle)

        self.image = pygame.transform.rotate(self.image_orig, -angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.rect.top > HEIGHT:
            self.kill()


class Boss3(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.direction = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)])
        self.direction_x, self.direction_y = self.direction
        self.shoot_timer = 0
        self.shots_fired = 0
        self.teleport_timer = 0
        self.teleport_interval = 160

    def update(self, enemy_bullets_group, player):
        self.rect.x += math.sin(pygame.time.get_ticks() * 0.01) * 2
        self.rect.y += math.sin(pygame.time.get_ticks() * 0.01) * 2
        if self.shots_fired < 20:
            dx, dy = self.direction
            if self.direction in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                self.speed = 5 / math.sqrt(2)
            else:
                self.speed = 5
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

            if self.rect.left < 5:
                self.rect.left = 5
                self.direction_x = 1
                if self.direction_y == 0:
                    self.direction_y = 1
            elif self.rect.right > WIDTH - 5:
                self.rect.right = WIDTH - 5
                self.direction_x = -1
                if self.direction_y == 0:
                    self.direction_y = 1
            elif self.rect.top < 70:
                self.rect.top = 70
                self.direction_y = 1
                if self.direction_x == 0:
                    self.direction_x = 1
            elif self.rect.bottom > HEIGHT - 5:
                self.rect.bottom = HEIGHT - 5
                self.direction_y = -1
                if self.direction_x == 0:
                    self.direction_x = 1

            self.direction = (self.direction_x, self.direction_y)
            self.shoot_timer += 1
            if self.shoot_timer >= 120:
                dx = player.rect.centerx - self.rect.centerx
                dy = player.rect.centery - self.rect.centery
                direction = pygame.math.Vector2(dx, dy).normalize()
                bullet = Boss3Bullet(self.rect.centerx, self.rect.bottom, direction)
                enemy_bullets_group.add(bullet)
                self.shoot_timer = 0
                self.shots_fired += 1
        else:
            if self.speed != 5:
                self.speed = 5 / math.sqrt(2)
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            direction = pygame.math.Vector2(dx, dy).normalize()

            self.rect.x += direction.x * self.speed
            self.rect.y += direction.y * self.speed

            self.direction_x = direction.x / abs(direction.x) if direction.x != 0 else 0
            self.direction_y = direction.y / abs(direction.y) if direction.y != 0 else 0
            self.direction = (self.direction_x, self.direction_y)

        self.teleport_timer += 1
        if self.teleport_timer >= self.teleport_interval:
            self.rect.centerx = random.randint(50, WIDTH - 50)
            self.rect.centery = random.randint(100, HEIGHT - 100)
            self.teleport_timer = 0


class Boss3Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, direction):
        super().__init__()
        self.image_orig = pygame.image.load('images/bullets/bulletboss3.png').convert_alpha()
        self.image = self.image_orig
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y + 10
        self.speed = 15
        self.direction = direction
        self.shoot_sound = pygame.mixer.Sound('game_sounds/shooting/boss2shoot.mp3')
        self.shoot_sound.set_volume(0.4)
        self.shoot_sound.play()

    def update(self):
        self.rect.move_ip(self.direction.x * self.speed, self.direction.y * self.speed)

        angle = math.atan2(self.direction.y, self.direction.x)
        angle = math.degrees(angle)

        self.image = pygame.transform.rotate(self.image_orig, -angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.rect.top > HEIGHT:
            self.kill()
