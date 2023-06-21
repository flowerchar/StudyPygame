import sys
import random

import pygame

WIDTH = 800
HEIGHT = 600
SIZE = WIDTH, HEIGHT

pygame.init()

screen = pygame.display.set_mode(SIZE)

ADDENEMY = pygame.USEREVENT
pygame.time.set_timer(ADDENEMY, 250)    # 0.25s触发一次ADDENEMY的自定义事件

ADDCLOUD = pygame.USEREVENT + 1
pygame.time.set_timer(ADDCLOUD, 1000)

# 加载背景音乐
pygame.mixer.music.load("assets/sounds/bgm.mp3")

# 加载音效
move_up_sound = pygame.mixer.Sound("assets/sounds/up.ogg")
move_down_sound = pygame.mixer.Sound("assets/sounds/down.ogg")

# 循环播放背景音乐
pygame.mixer.music.play(loops=-1)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load("assets/sprites/jet.png")
        self.surf.set_colorkey("white")
        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_DOWN]:
            move_down_sound.play()
            self.rect.move_ip(0, 10)
        if pressed_keys[pygame.K_UP]:
            move_up_sound.play()
            self.rect.move_ip(0, -10)
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-10, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(10, 0)
        # 限制玩家在屏幕中移动
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <= 0:
            self.rect.left = 0

    def draw(self):
        screen.blit(self.surf, self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/sprites/missile.png")
        self.image.set_colorkey("white")
        self.rect = self.image.get_rect(center=(
            random.randint(WIDTH + 10, WIDTH + 50),
            random.randint(0, HEIGHT)
        ))
        self.speed = random.randint(-10, -5)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.right <= 0:
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/sprites/cloud.png")
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect(center=(
            random.randint(WIDTH + 10, WIDTH + 50),
            random.randint(0, HEIGHT)
        ))

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right <= 0:
            self.kill()


player = Player()
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # quit()
            pygame.quit()
            sys.exit()
        if event.type == ADDENEMY:
            enemies.add(Enemy())
        if event.type == ADDCLOUD:
            clouds.add(Cloud())

    # move
    player.move()
    enemies.update()
    clouds.update()

    # 碰撞检测
    # for enemy in enemies:
    #     if enemy.rect.colliderect(player.rect):
    #         pygame.quit()
    #         sys.exit()
    if pygame.sprite.spritecollideany(player, enemies, pygame.sprite.collide_mask):
        pygame.quit()
        sys.exit()

    # draw
    screen.fill((135, 206, 250))
    player.draw()
    enemies.draw(screen)
    clouds.draw(screen)

    pygame.display.flip()
    clock.tick(60)
