import random

import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT

from utils import load_image


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = load_image("./assets/sprites/me1.png")
        self.image2 = load_image("./assets/sprites/me2.png")
        self.rect = self.image.get_rect(midbottom=(
            self.game.width / 2,
            self.game.height - 60
        ))
        self.mask = pygame.mask.from_surface(self.image)
        self.active = True
        self.destroy_images = [
            load_image(f"./assets/sprites/me_destroy_{i + 1}.png")
            for i in range(4)
        ]
        self.destroy_index = 0
        self.life = 3
        self.life_image = load_image("./assets/sprites/life.png")
        self.life_rect = self.life_image.get_rect()
        self.invincible = False

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -10)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 10)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-10, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(10, 0)
        # 不能跑出屏幕外
        if self.rect.right >= self.game.width:
            self.rect.right = self.game.width
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.game.height - 60:
            self.rect.bottom = self.game.height - 60

    def draw(self):
        if self.active:
            if self.invincible:
                if random.choice([True, False]):
                    return
            if random.choice([True, False]):
                self.game.screen.blit(self.image, self.rect)
            else:
                self.game.screen.blit(self.image2, self.rect)
        else:
            if not (self.game.delay % 3):
                self.destroy_index += 1
                if self.destroy_index == 4:
                    self.destroy_index = 0
                self.game.screen.blit(self.destroy_images[self.destroy_index], self.rect)
                if self.destroy_index == 0:
                    if self.life == 1:
                        self.game.status = self.game.STATUS_OVER
                    self.game.me_down_sound.play()
                    self.life -= 1
                    self.reset()

    def reset(self):
        self.active = True
        self.invincible = True
        pygame.time.set_timer(self.game.INVINCIBLE, 3 * 1000)
        self.rect = self.image.get_rect(midbottom=(
            self.game.width / 2,
            self.game.height - 60
        ))


