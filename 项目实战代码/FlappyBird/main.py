import datetime

import pygame
import pygame.constants

from models import Bird, Pipe, Score
from utils import load_image


class FlappyBird:
    WIDTH = 288
    HEIGHT = 512
    SIZE = WIDTH, HEIGHT
    ADDPIPE = pygame.USEREVENT

    STATUS_INIT = 0
    STATUS_RUN = 1
    STATUS_OVER = 2

    def __init__(self):
        pygame.init()
        pygame.time.set_timer(self.ADDPIPE, 1800)
        self.status = self.STATUS_INIT
        self.screen = pygame.display.set_mode(self.SIZE)
        self.clock = pygame.time.Clock()
        self.bg_image = self.get_bg_by_time()
        self.base = load_image("./assets/sprites/base.png")
        self.base_rect = self.base.get_rect(bottom=self.HEIGHT)
        self.welcome = load_image("./assets/sprites/message.png")
        self.game_over = load_image("./assets/sprites/gameover.png")
        # 音效
        self.sound_die = pygame.mixer.Sound("./assets/sounds/die.wav")
        self.sound_hit = pygame.mixer.Sound("./assets/sounds/hit.wav")
        self.sound_point = pygame.mixer.Sound("./assets/sounds/point.wav")
        self.sound_swoosh = pygame.mixer.Sound("./assets/sounds/swoosh.wav")
        self.sound_wing = pygame.mixer.Sound("./assets/sounds/wing.wav")

        self.delay = 100
        self.count = 0

        self.bird = Bird(self)
        self.score = Score(self)
        self.pipes = pygame.sprite.Group()

    @staticmethod
    def get_bg_by_time():
        h = datetime.datetime.now().hour
        if 8 <= h <= 18:
            return load_image("./assets/sprites/background-day.png")
        return load_image("./assets/sprites/background-night.png")

    def main_loop(self):
        while True:
            self.handle_input()
            self.game_logic()
            self.draw()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit()
            if self.status == self.STATUS_RUN and event.type == self.ADDPIPE:
                # 管道一对一对增加
                pipe = Pipe(self)
                self.pipes.add(pipe, pipe.flip())
            # 点击空格键开始游戏
            if self.status == self.STATUS_INIT and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.status = self.STATUS_RUN
            # 点击空格键再来一次
            if self.status == self.STATUS_OVER and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.status = self.STATUS_INIT
                self.reset()

    def reset(self):
        self.bird = Bird(self)
        self.pipes.empty()
        self.score.score = 0
        self.count += 1

    def game_logic(self):
        if self.status == self.STATUS_RUN:
            self.bird.update()
            for pipe in self.pipes:
                pipe.update()
                if pipe.rect.right <= 0:
                    pipe.kill()
            self.score.update(self.bird, self.pipes)
            # 地板向左移动
            self.base_rect.move_ip(-2, 0)
            if self.base_rect.right <= self.WIDTH:
                self.base_rect.left = 0
            # 碰撞检测
            if pygame.sprite.spritecollideany(self.bird, self.pipes, collided=pygame.sprite.collide_mask):
                self.status = self.STATUS_OVER
                self.sound_hit.play()
            if self.bird.rect.top <= 0 or self.bird.rect.bottom >= self.base_rect.top:
                self.sound_hit.play()
                self.status = self.STATUS_OVER
        elif self.status == self.STATUS_OVER:
            self.bird.update()

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        if self.status == self.STATUS_INIT:
            self.screen.blit(self.welcome, self.welcome.get_rect(center=(self.WIDTH/2, self.HEIGHT/2)))
        elif self.status == self.STATUS_RUN:
            self.bird.draw()
            for pipe in self.pipes:
                pipe.draw()
            self.score.draw()
        elif self.status == self.STATUS_OVER:
            for pipe in self.pipes:
                pipe.draw()
            self.bird.draw()
            self.screen.blit(self.game_over, self.game_over.get_rect(center=(self.WIDTH/2, self.HEIGHT/2)))
        self.screen.blit(self.base, self.base_rect)
        pygame.display.flip()
        self.clock.tick(60)
        self.delay -= 1
        if self.delay == 0:
            self.delay = 100


if __name__ == '__main__':
    fb = FlappyBird()
    fb.main_loop()

