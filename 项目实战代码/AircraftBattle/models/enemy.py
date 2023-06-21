import random

import pygame

from utils import load_image


class SmallEnemy(pygame.sprite.Sprite):
    ENERGY = 1

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = load_image("./assets/sprites/enemy1.png")
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(0, self.game.width - self.rect.width)
        self.rect.bottom = random.randint(-5 * self.game.height, 0)
        self.speed = 2
        self.mask = pygame.mask.from_surface(self.image)
        self.active = True
        self.destroy_images = [
            load_image(f"./assets/sprites/enemy1_down{i + 1}.png")
            for i in range(4)
        ]
        self.destroy_index = 0
        self.energy = self.ENERGY

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top >= self.game.height:
            self.reset()

    def reset(self):
        self.rect.left = random.randint(0, self.game.width - self.rect.width)
        self.rect.bottom = random.randint(-5 * self.game.height, 0)
        self.active = True
        self.energy = self.ENERGY

    def draw(self):
        if self.active:
            self.game.screen.blit(self.image, self.rect)
        else:
            if not (self.game.delay % 3):
                self.destroy_index += 1
                if self.destroy_index == 4:
                    self.destroy_index = 0
                self.game.screen.blit(self.destroy_images[self.destroy_index], self.rect)
                if self.destroy_index == 0:
                    self.reset()
                    self.game.enemy1_down_sound.play()


class MiddleEnemy(pygame.sprite.Sprite):
    ENERGY = 8

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = load_image("./assets/sprites/enemy2.png")
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(0, self.game.width - self.rect.width)
        self.rect.bottom = random.randint(-10 * self.game.height, -self.game.height)
        self.speed = 1
        self.mask = pygame.mask.from_surface(self.image)
        self.active = True
        self.destroy_images = [
            load_image(f"./assets/sprites/enemy2_down{i + 1}.png")
            for i in range(4)
        ]
        self.destroy_index = 0
        self.energy = self.ENERGY
        self.hit_image = load_image("./assets/sprites/enemy2_hit.png")
        self.hit = False

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top >= self.game.height:
            self.reset()

    def reset(self):
        self.rect.left = random.randint(0, self.game.width - self.rect.width)
        self.rect.bottom = random.randint(-10 * self.game.height, -self.game.height)
        self.active = True
        self.energy = self.ENERGY
        self.hit = False

    def draw(self):
        if self.active:
            # 绘制血槽
            self.draw_energy()
            if self.hit:
                self.game.screen.blit(self.hit_image, self.rect)
                self.hit = False
            else:
                self.game.screen.blit(self.image, self.rect)
        else:
            if not (self.game.delay % 3):
                self.destroy_index += 1
                if self.destroy_index == 4:
                    self.destroy_index = 0
                self.game.screen.blit(self.destroy_images[self.destroy_index], self.rect)
                if self.destroy_index == 0:
                    self.reset()
                    self.game.enemy2_down_sound.play()

    def draw_energy(self):
        pygame.draw.line(
            self.game.screen, "black",
            (self.rect.left, self.rect.top - 5),
            (self.rect.right, self.rect.top - 5),
            2
        )
        energy_remain = self.energy / self.ENERGY
        energy_color = "green" if energy_remain > 0.2 else "red"
        pygame.draw.line(
            self.game.screen, energy_color,
            (self.rect.left, self.rect.top - 5),
            (self.rect.left + self.rect.width * energy_remain, self.rect.top - 5),
            2
        )


class BigEnemy(pygame.sprite.Sprite):
    ENERGY = 20

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = load_image("./assets/sprites/enemy3_n1.png")
        self.image2 = load_image("./assets/sprites/enemy3_n2.png")
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(0, self.game.width - self.rect.width)
        self.rect.bottom = random.randint(-15 * self.game.height, -5 * self.game.height)
        self.speed = 1
        self.mask = pygame.mask.from_surface(self.image)
        self.active = True
        self.destroy_images = [
            load_image(f"./assets/sprites/enemy3_down{i + 1}.png")
            for i in range(6)
        ]
        self.destroy_index = 0
        self.energy = self.ENERGY
        self.hit = False
        self.hit_image = load_image("./assets/sprites/enemy3_hit.png")

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom == -50:
            # 屏幕上方50的位置开始播放循环音效
            self.game.enemy3_fly_sound.play(-1)
        if self.rect.top >= self.game.height:
            self.reset()

    def reset(self):
        self.rect.left = random.randint(0, self.game.width - self.rect.width)
        self.rect.bottom = random.randint(-15 * self.game.height, -5 * self.game.height)
        self.game.enemy3_fly_sound.stop()   # 关闭飞行音效
        self.active = True
        self.energy = self.ENERGY
        self.hit = False

    def draw(self):
        if self.active:
            if self.hit:
                self.game.screen.blit(self.hit_image, self.rect)
                self.hit = False
            else:
                # 大飞机突突的感觉
                if random.choice([True, False]):
                    self.game.screen.blit(self.image, self.rect)
                else:
                    self.game.screen.blit(self.image2, self.rect)
            self.draw_energy()
        else:
            if not (self.game.delay % 3):
                self.destroy_index += 1
                if self.destroy_index == 6:
                    self.destroy_index = 0
                self.game.screen.blit(self.destroy_images[self.destroy_index], self.rect)
                if self.destroy_index == 0:
                    self.reset()
                    self.game.enemy3_down_sound.play()

    def draw_energy(self):
        pygame.draw.line(
            self.game.screen, "black",
            (self.rect.left, self.rect.top - 5),
            (self.rect.right, self.rect.top - 5),
            2
        )
        energy_remain = self.energy / self.ENERGY
        energy_color = "green" if energy_remain > 0.2 else "red"
        pygame.draw.line(
            self.game.screen, energy_color,
            (self.rect.left, self.rect.top - 5),
            (self.rect.left + self.rect.width * energy_remain, self.rect.top - 5),
            2
        )
