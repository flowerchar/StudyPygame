import pygame


class Player:
    def __init__(self, game):
        self.game = game
        self.image = pygame.Surface((50, 50))
        self.image.fill("red")
        self.rect = self.image.get_rect(center=(self.game.WIDTH / 2, self.game.HEIGHT / 2))

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_UP]:
            self.rect.top = 0
        self.rect.move_ip(0, 1)

    def draw(self):
        self.game.screen.blit(self.image, self.rect)


class Enemy:
    pass


class Missile:
    pass