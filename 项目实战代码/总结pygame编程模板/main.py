"""
import pygame

pygame.init()

SIZE = WIDTH, HEIGHT = 288, 512

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
player = pygame.Surface((50, 50))
player.fill("red")
player_rect = player.get_rect(center=(WIDTH/2, HEIGHT/2))

while True:
    # 处理输入
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            quit()

    # 游戏逻辑
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_UP]:
        player_rect.top = 0
    player_rect.move_ip(0, 1)

    # 画图
    screen.fill("white")
    screen.blit(player, player_rect)
    pygame.display.flip()
    clock.tick(60)


"""

import pygame

from models import Player


class Game:
    WIDTH = 288
    HEIGHT = 512
    SIZE = WIDTH, HEIGHT
    pygame.init()
    def __init__(self):

        self.screen = pygame.display.set_mode(self.SIZE)
        self.clock = pygame.time.Clock()
        self.player = Player(self)

    def main_loop(self):
        while True:
            self.handle_input()
            self.game_logic()
            self.draw()

    def handle_input(self):
        # 处理输入
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit()

    def game_logic(self):
        # 游戏逻辑
        self.player.update()

    def draw(self):
        # 画图
        self.screen.fill("white")
        self.player.draw()
        pygame.display.flip()
        self.clock.tick(60)


gamer = Game()
gamer.main_loop()