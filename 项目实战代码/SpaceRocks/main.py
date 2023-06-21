import sys

import pygame
from pygame.math import Vector2

from models import Ship, Asteroid, Bullet
from utils import get_random_position, get_random_velocity


class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self):
        self.width = 800
        self.height = 600
        pygame.init()
        pygame.display.set_caption("Space Rocks")
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.bg_image = pygame.image.load("./assets/sprites/space.png")
        self.load_music()
        self.message = ""
        pygame.font.init()
        self.FONT = pygame.font.Font(None, 40)

        self.ship = Ship((self.width/2, self.height/2), Vector2(0))
        self.asteroids = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        for _ in range(6):
            while True:
                velocity = get_random_velocity(1, 3)
                position = get_random_position(self.screen)
                if position.distance_to(self.ship.position) > self.MIN_ASTEROID_DISTANCE:
                    break
            self.asteroids.add(Asteroid(position, velocity))

    def load_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load("./assets/sounds/bgm.mp3")
        self.shoot_sound = pygame.mixer.Sound("./assets/sounds/laser.wav")
        pygame.mixer.music.play(-1)

    def main_loop(self):
        while True:
            self.handle_input()
            self.game_logic()
            self.draw()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif self.ship and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                velocity = self.ship.direction * self.ship.BULLET_SPEED + self.ship.velocity
                bullet = Bullet(self.ship.position, velocity)
                self.bullets.add(bullet)
                self.shoot_sound.play()
        if self.ship:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_LEFT]:
                self.ship.rotate(False)
            elif pressed_keys[pygame.K_RIGHT]:
                self.ship.rotate(True)
            if pressed_keys[pygame.K_UP]:
                self.ship.accelerate()

    def game_logic(self):
        for obj in self.get_game_objects():
            obj.update(self.screen)
        # 飞船和行星碰撞检测
        if self.ship:
            for a in self.asteroids:
                if self.ship.collides_with(a):
                    self.ship = None
                    self.message = "You lost!"
                    break
        # 子弹和行星碰撞检测
        for bullet in self.bullets:
            for a in self.asteroids:
                if bullet.collides_with(a):
                    bullet.kill()
                    a.kill()
                    # 分裂
                    if a.size > 1:
                        for _ in range(2):
                            asteroid = Asteroid(a.position, get_random_velocity(1, 3), a.size - 1)
                            self.asteroids.add(asteroid)
        if not self.asteroids and self.ship:
            self.message = "You won!"

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        for obj in self.get_game_objects():
            obj.draw(self.screen)
        if self.message:
            message_surf = self.FONT.render(self.message, True, "white")
            message_rect = message_surf.get_rect(center=(self.width/2, self.height/2))
            self.screen.blit(message_surf, message_rect)

        pygame.display.flip()
        self.clock.tick(60)

    def get_game_objects(self):
        objs = [*self.asteroids, *self.bullets]
        if self.ship:
            objs.append(self.ship)
        return objs


if __name__ == '__main__':
    game = SpaceRocks()
    game.main_loop()