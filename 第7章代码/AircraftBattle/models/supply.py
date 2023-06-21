import random

import pygame

from utils import load_image


class Supply(pygame.sprite.Sprite):
    def __init__(self, game, filename):
        super().__init__()
        self.game = game
        self.image = load_image(filename)
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(0, self.game.width - self.rect.width)
        self.rect.bottom = -100
        self.speed = 5
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top >= self.game.height:
            self.kill()


class BombSupply(Supply):
    type = "bomb"


class BulletSupply(Supply):
    type = "bullet"
