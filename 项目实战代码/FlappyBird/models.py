import random

import pygame.sprite

from utils import load_image


class Bird(pygame.sprite.Sprite):
    GRAVITY = 1

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image_index = 0
        self.images = self.get_images()
        self.rect = self.image.get_rect(center=(self.game.WIDTH/2, self.game.HEIGHT/2))
        self.movement = 0   # 小鸟向下移动的距离
        self.mask = pygame.mask.from_surface(self.image)
        self.on_earth = False

    @staticmethod
    def get_images():
        b = random.choice(["bluebird", "redbird", "yellowbird"])
        return [
            load_image(f"./assets/sprites/{b}-{i}flap.png")
            for i in ("down", "mid", "up")
        ]

    @property
    def image(self):
        if self.game.status == self.game.STATUS_OVER:
            return self.images[0]
        if not (self.game.delay % 5):
            self.image_index += 1
            if self.image_index == 3:
                self.image_index = 0
        return self.images[self.image_index]

    @property
    def rotated_image(self):
        # return pygame.transform.rotate(self.image, -3 * self.movement)
        return pygame.transform.rotozoom(self.image, -3 * self.movement, 1)

    def draw(self):
        self.game.screen.blit(self.rotated_image, self.rect)

    def update(self):
        if not self.on_earth:
            self.movement += self.GRAVITY   # movement 越来越大的
            self.rect.move_ip(0, self.movement)

        if self.game.status == self.game.STATUS_RUN:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_SPACE]:
                if self.movement > 0:
                    # 保证只响一次
                    self.game.sound_wing.play()
                self.movement = 0   # 优化小鸟跳跃的瞬间
                self.movement -= 7
        elif self.game.status == self.game.STATUS_OVER:
            if self.rect.centery >= 400:
                self.rect.centery = 390
                self.on_earth = True
                self.game.sound_die.play()


class Pipe(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = self.get_image()
        self.rect = self.image.get_rect(x=self.game.WIDTH, y=random.randint(200, 360))
        self.mask = pygame.mask.from_surface(self.image)

    def get_image(self):
        cs = ["green", "red"]
        i = self.game.count % 2
        return load_image(f"./assets/sprites/pipe-{cs[i]}.png")

    def update(self):
        self.rect.move_ip(-2, 0)

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

    def flip(self):
        new = Pipe(self.game)
        new.image = pygame.transform.flip(self.image, False, True)
        new.rect = new.image.get_rect(midbottom=(self.rect.centerx, self.rect.top - 150))
        new.mask = pygame.mask.from_surface(new.image)
        return new


class Score:
    pygame.font.init()
    FONT = pygame.font.Font(None, 40)

    def __init__(self, game):
        self.game = game
        self.score = 0
        self.image = self.FONT.render(str(self.score), True, "white")
        self.rect = self.image.get_rect(center=(self.game.WIDTH/2, 40))

    def draw(self):
        self.image = self.FONT.render(str(self.score), True, "white")
        self.game.screen.blit(self.image, self.rect)

    def update(self, bird, pipes):
        # old_score = self.score
        for i, p in enumerate(pipes):
            if i % 2 == 0 and bird.rect.left > p.rect.right and not hasattr(p, "passed"):
                self.score += 1
                self.game.sound_point.play()
                setattr(p, "passed", True)
        #
        # if self.score > old_score:
        #     self.game.sound_point.play()






