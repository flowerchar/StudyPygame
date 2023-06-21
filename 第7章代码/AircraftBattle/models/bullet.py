import pygame

from utils import load_image


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = load_image("./assets/sprites/bullet1.png")
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.game.player.rect.midtop
        self.speed = 12
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.top -= self.speed
        if self.rect.top <= 0:
            self.kill()


class SuperBullet(Bullet):
    def __init__(self, game):
        super().__init__(game)
        self.image = load_image("./assets/sprites/bullet2.png")
        self.speed = 15

    @classmethod
    def bulk_create(cls, game):
        left = cls(game)
        right = cls(game)
        left.rect.center = (
            game.player.rect.centerx - 33, game.player.rect.centery
        )
        right.rect.center = (
            game.player.rect.centerx + 30, game.player.rect.centery
        )
        return left, right


