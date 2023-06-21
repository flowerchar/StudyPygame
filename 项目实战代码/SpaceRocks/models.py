import pygame.sprite
from pygame.math import Vector2

from utils import wrap_position

UP = Vector2(0, -1)


class GameObject(pygame.sprite.Sprite):
    def __init__(self, position, velocity):
        super().__init__()
        self.position = Vector2(position)
        self.velocity = Vector2(velocity)
        self.radius = self.image.get_width() / 2

    def update(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.image, blit_position)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius


class Ship(GameObject):
    ROTATE_FACTOR = 3
    ACCELERATION = 0.25
    BULLET_SPEED = 3

    def __init__(self, position, velocity):
        self.image = pygame.image.load("./assets/sprites/spaceship.png").convert_alpha()
        self.direction = Vector2(UP)
        super().__init__(position, velocity)

    def draw(self, surface):
        # 旋转角度变化
        angle = self.direction.angle_to(UP)
        rotated_surface = pygame.transform.rotozoom(self.image, angle, 1.0)
        # 画图
        blit_position = self.position - Vector2(rotated_surface.get_width()) * 0.5
        surface.blit(rotated_surface, blit_position)

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        self.direction.rotate_ip(sign * self.ROTATE_FACTOR)

    def accelerate(self):
        if self.velocity.length() >= 4:
            return
        self.velocity = self.velocity + self.direction * self.ACCELERATION


class Asteroid(GameObject):
    def __init__(self, position, velocity, size=3):
        self.size = size
        size_to_scale = {
            3: 1,
            2: 0.5,
            1: 0.25,
        }
        scale = size_to_scale[self.size]
        image = pygame.image.load("./assets/sprites/asteroid.png").convert_alpha()
        self.image = pygame.transform.rotozoom(image, 0, scale)
        super().__init__(position, velocity)


class Bullet(GameObject):
    def __init__(self, position, velocity):
        self.image = pygame.image.load("./assets/sprites/bullet.png").convert_alpha()
        super().__init__(position, velocity)

    def update(self, surface):
        self.position = self.position + self.velocity
        # 子弹需要回收
        if not surface.get_rect().collidepoint(self.position):
            self.kill()
