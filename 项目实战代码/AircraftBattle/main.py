import random
from itertools import chain

import pygame
import pygame.color

from models.player import Player
from models.enemy import SmallEnemy, MiddleEnemy, BigEnemy
from models.bullet import Bullet, SuperBullet
from models.supply import BombSupply, BulletSupply
from utils import load_image


class AircraftBattle:
    ADD_BULLET = pygame.USEREVENT   # 增加普通子弹
    ADD_SUPPLY = pygame.USEREVENT + 1   # 增加补给包
    ADD_SUPER_BULLET = pygame.USEREVENT + 2
    USE_SUPER_BULLET = pygame.USEREVENT + 3
    INVINCIBLE = pygame.USEREVENT + 4    # 无敌时间
    # 游戏状态
    STATUS_INIT = 0
    STATUS_RUN = 1
    STATUS_OVER = 2
    STATUS_PAUSE = 3

    def __init__(self):
        pygame.init()
        self.width = 480
        self.height = 700
        self.size = self.width, self.height
        self.screen = pygame.display.set_mode(self.size)
        self.bg_image = load_image("./assets/sprites/background.png")
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("飞机大战")
        pygame.display.set_icon(load_image("./assets/sprites/battle.ico", False))
        self.status = self.STATUS_INIT

        self.player = Player(self)
        self.small_enemies = pygame.sprite.Group()
        self.mid_enemies = pygame.sprite.Group()
        self.big_enemies = pygame.sprite.Group()
        self.all_enemies = pygame.sprite.Group()

        # 子弹
        self.bullets = pygame.sprite.Group()

        self.init_enemies()
        self.load_sounds()

        self.delay = 100

        self.score = 0
        self.FONT = pygame.font.Font(None, 40)
        self.level = 1

        # 全屏炸弹
        self.bomb_nums = 3
        self.bomb_image = load_image("./assets/sprites/bomb.png")
        self.bomb_rect = self.bomb_image.get_rect(topleft=(10, self.height - 60))

        self.supplies = pygame.sprite.Group()

        # 开始页面
        self.desc_image = load_image("./assets/sprites/desc.png")
        self.desc_rect = self.desc_image.get_rect(center=(self.width/2, self.height - 180))
        self.over_image = load_image("./assets/sprites/gameover.png")
        self.over_rect = self.over_image.get_rect(center=(self.width/2, self.height - 200))
        self.again_image = load_image("./assets/sprites/again.png")
        self.again_rect = self.again_image.get_rect(center=(self.width/2, self.height - 250))
        self.mouse_image = load_image("./assets/sprites/check.png")
        # 暂停游戏
        self.pause_nor_image = load_image("./assets/sprites/pause_nor.png")
        self.pause_pressed_image = load_image("./assets/sprites/pause_pressed.png")
        self.resume_nor_image = load_image("./assets/sprites/resume_nor.png")
        self.resume_pressed_image = load_image("./assets/sprites/resume_pressed.png")

        self.pause_image = self.pause_nor_image
        self.pause_rect = self.pause_image.get_rect(topright=(self.width - 10, 10))

    @staticmethod
    def inc_speed(enemy_group, nums):
        for e in enemy_group:
            e.speed += nums

    def upgrade_level(self):
        if self.level == 1 and self.score > 50000:
            self.level = 2
            self.upgrade_sound.play()
            self.add_enemies(SmallEnemy, 3)
            self.add_enemies(MiddleEnemy, 2)
            self.add_enemies(BigEnemy, 1)
            self.inc_speed(self.small_enemies, 1)
        elif self.level == 2 and self.score > 300000:
            self.level = 3
            self.upgrade_sound.play()
            self.add_enemies(SmallEnemy, 5)
            self.add_enemies(MiddleEnemy, 3)
            self.add_enemies(BigEnemy, 2)
            self.inc_speed(self.small_enemies, 1)
            self.inc_speed(self.mid_enemies, 1)
        elif self.level == 3 and self.score > 600000:
            self.level = 4
            self.upgrade_sound.play()
            self.add_enemies(SmallEnemy, 5)
            self.add_enemies(MiddleEnemy, 3)
            self.add_enemies(BigEnemy, 2)
            self.inc_speed(self.small_enemies, 1)
            self.inc_speed(self.mid_enemies, 1)
        elif self.level == 4 and self.score > 1000000:
            self.level = 5
            self.upgrade_sound.play()
            self.add_enemies(SmallEnemy, 5)
            self.add_enemies(MiddleEnemy, 3)
            self.add_enemies(BigEnemy, 2)
            self.inc_speed(self.small_enemies, 1)
            self.inc_speed(self.mid_enemies, 1)

    def load_sounds(self):
        pygame.mixer.init()
        pygame.mixer.music.load("./assets/sounds/game_music.ogg")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

        self.bullet_sound = pygame.mixer.Sound("./assets/sounds/bullet.wav")
        self.button_sound = pygame.mixer.Sound("./assets/sounds/button.wav")
        self.bomb_sound = pygame.mixer.Sound("./assets/sounds/use_bomb.wav")
        self.supply_sound = pygame.mixer.Sound("./assets/sounds/supply.wav")
        self.get_bomb_sound = pygame.mixer.Sound("./assets/sounds/get_bomb.wav")
        self.get_bullet_sound = pygame.mixer.Sound("./assets/sounds/get_bullet.wav")
        self.upgrade_sound = pygame.mixer.Sound("./assets/sounds/upgrade.wav")
        self.enemy3_fly_sound = pygame.mixer.Sound("./assets/sounds/enemy3_flying.wav")
        self.enemy1_down_sound = pygame.mixer.Sound("./assets/sounds/enemy1_down.wav")
        self.enemy2_down_sound = pygame.mixer.Sound("./assets/sounds/enemy2_down.wav")
        self.enemy3_down_sound = pygame.mixer.Sound("./assets/sounds/enemy3_down.wav")
        self.me_down_sound = pygame.mixer.Sound("./assets/sounds/me_down.wav")
        # 设置音效音量大小，范围: 0-1
        self.bullet_sound.set_volume(0.1)
        self.button_sound.set_volume(0.1)
        self.bomb_sound.set_volume(0.2)
        self.supply_sound.set_volume(0.2)
        self.get_bomb_sound.set_volume(0.2)
        self.get_bullet_sound.set_volume(0.2)
        self.upgrade_sound.set_volume(0.2)
        self.enemy3_fly_sound.set_volume(0.8)
        self.enemy1_down_sound.set_volume(0.2)
        self.enemy2_down_sound.set_volume(0.2)
        self.enemy3_down_sound.set_volume(0.2)
        self.me_down_sound.set_volume(0.2)

    def init_enemies(self):
        # 初始敌机的数量
        self.add_enemies(SmallEnemy, 15)
        self.add_enemies(MiddleEnemy, 5)
        self.add_enemies(BigEnemy, 2)

    def add_enemies(self, enemy_class, nums):
        for _ in range(nums):
            e = enemy_class(self)
            self.all_enemies.add(e)
            if enemy_class.__name__ == "SmallEnemy":
                self.small_enemies.add(e)
            elif enemy_class.__name__ == "MiddleEnemy":
                self.mid_enemies.add(e)
            elif enemy_class.__name__ == "BigEnemy":
                self.big_enemies.add(e)

    def main_loop(self):
        while True:
            self.handle_input()
            self.game_logic()
            self.draw()

    def reset(self):
        self.status = self.STATUS_INIT
        self.score = 0
        self.level = 1
        self.bomb_nums = 3
        self.player = Player(self)
        self.all_enemies.empty()
        self.small_enemies.empty()
        self.mid_enemies.empty()
        self.big_enemies.empty()
        self.init_enemies()
        pygame.mixer.music.play(-1)
        pygame.mouse.set_visible(True)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif self.status == self.STATUS_INIT and event.type == pygame.KEYDOWN:
                self.status = self.STATUS_RUN
                pygame.time.set_timer(self.ADD_BULLET, 150)
                pygame.time.set_timer(self.ADD_SUPPLY, 30 * 1000)
            elif self.status == self.STATUS_OVER and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.over_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    pygame.quit()
                    quit()
                elif event.button == 1 and self.again_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.reset()

            elif self.status == self.STATUS_RUN and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.bomb_nums:
                    self.bomb_nums -= 1
                    self.bomb_sound.play()
                    for e in self.all_enemies:
                        if e.active and e.rect.bottom > 0:
                            e.active = False
                            if e in self.small_enemies:
                                self.score += 1000
                            elif e in self.mid_enemies:
                                self.score += 5000
                            else:
                                self.score += 10000
            elif self.status == self.STATUS_RUN and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.pause_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.pause_image = self.resume_pressed_image
                    self.status = self.STATUS_PAUSE
                    pygame.mixer.pause()
                    pygame.mixer.music.pause()
                    pygame.time.set_timer(self.ADD_SUPPLY, 0)
                    pygame.time.set_timer(self.ADD_BULLET, 0)
                    pygame.time.set_timer(self.ADD_SUPER_BULLET, 0)
            elif self.status == self.STATUS_PAUSE and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.pause_rect.collidepoint(event.pos):
                    self.button_sound.play()
                    self.status = self.STATUS_RUN
                    self.pause_image = self.pause_pressed_image
                    pygame.mixer.unpause()
                    pygame.mixer.music.unpause()
                    pygame.time.set_timer(self.ADD_BULLET, 150)
                    pygame.time.set_timer(self.ADD_SUPPLY, 30 * 10000)
            elif self.status == self.STATUS_RUN and event.type == pygame.MOUSEMOTION:
                if self.pause_rect.collidepoint(event.pos):
                    self.pause_image = self.pause_pressed_image
                else:
                    self.pause_image = self.pause_nor_image
            elif self.status == self.STATUS_PAUSE and event.type == pygame.MOUSEMOTION:
                if self.pause_rect.collidepoint(event.pos):
                    self.pause_image = self.resume_pressed_image
                else:
                    self.pause_image = self.resume_nor_image

            if event.type == self.ADD_BULLET:
                self.bullets.add(Bullet(self))
                self.bullet_sound.play()
            if event.type == self.ADD_SUPPLY:
                self.supply_sound.play()
                self.supplies.add(random.choice([
                    BombSupply(self, "./assets/sprites/bomb_supply.png"),
                    BulletSupply(self, "./assets/sprites/bullet_supply.png")
                ]))
            if event.type == self.ADD_SUPER_BULLET:
                self.bullets.add(SuperBullet.bulk_create(self))
            if event.type == self.USE_SUPER_BULLET:
                # 结束使用超级子弹
                pygame.time.set_timer(self.USE_SUPER_BULLET, 0)
                pygame.time.set_timer(self.ADD_SUPER_BULLET, 0)
            if event.type == self.INVINCIBLE:
                self.player.invincible = False
                pygame.time.set_timer(self.INVINCIBLE, 0)

    def game_logic(self):
        if self.status == self.STATUS_OVER:
            pygame.mixer.stop()
            pygame.mixer.music.stop()
            pygame.time.set_timer(self.ADD_BULLET, 0)
            pygame.time.set_timer(self.ADD_SUPER_BULLET, 0)
            pygame.time.set_timer(self.ADD_SUPPLY, 0)
            pygame.time.set_timer(self.USE_SUPER_BULLET, 0)
            pygame.time.set_timer(self.INVINCIBLE, 0)
            return
        if self.status != self.STATUS_RUN:
            return

        self.player.update()
        self.all_enemies.update()
        self.bullets.update()
        self.supplies.update()

        # 子弹和敌机做碰撞检测
        collided = pygame.sprite.groupcollide(
            self.bullets, self.all_enemies, True, False,
            pygame.sprite.collide_mask
        )
        if collided:
            for es in collided.values():
                for e in es:
                    if not e.active:
                        continue
                    if e in self.small_enemies:
                        e.active = False
                        self.score += 1000
                    elif e in self.mid_enemies:
                        e.hit = True
                        e.energy -= 1
                        if e.energy == 0:
                            e.active = False
                            self.score += 5000
                    else:
                        e.hit = True
                        e.energy -= 1
                        if e.energy == 0:
                            e.active = False
                            self.score += 10000

        # 我方飞机和敌机之间的碰撞检测
        collied_enemies = pygame.sprite.spritecollide(
            self.player, self.all_enemies, False,
            pygame.sprite.collide_mask
        )
        if not self.player.invincible and collied_enemies:
            self.player.active = False
            for e in collied_enemies:
                if not e.active:
                    continue
                e.active = False
                if e in self.small_enemies:
                    self.score += 1000
                elif e in self.mid_enemies:
                    self.score += 5000
                else:
                    self.score += 10000
        # 领取补给包的碰撞检测
        collided = pygame.sprite.spritecollide(
            self.player, self.supplies, True,
            pygame.sprite.collide_mask
        )
        if collided:
            for s in collided:
                if s.type == "bomb":
                    self.get_bomb_sound.play()
                    if self.bomb_nums < 3:
                        self.bomb_nums += 1
                elif s.type == "bullet":
                    self.get_bullet_sound.play()
                    pygame.time.set_timer(self.ADD_SUPER_BULLET, 150)
                    pygame.time.set_timer(self.USE_SUPER_BULLET, 18 * 1000)

        self.upgrade_level()

        self.delay -= 1
        if self.delay == 0:
            self.delay = 100

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        if self.status == self.STATUS_INIT:
            self.draw_desc()
            self.player.draw()
        elif self.status == self.STATUS_OVER:
            self.draw_game_over()
            self.draw_confirm_mouse()
        elif self.status == self.STATUS_PAUSE:
            self.screen.blit(self.pause_image, self.pause_rect)
        elif self.status == self.STATUS_RUN:
            self.screen.blit(self.pause_image, self.pause_rect)
            self.player.draw()
            for e in chain(self.big_enemies, self.mid_enemies, self.small_enemies):
                e.draw()
            self.bullets.draw(self.screen)
            self.supplies.draw(self.screen)

            # 分数
            score_surf = self.FONT.render(f"Score: {self.score}", True, "white")
            self.screen.blit(score_surf, (10, 10))
            # 全屏炸弹
            bomb_nums_surf = self.FONT.render(f" x {self.bomb_nums}", True, "white")
            bomb_nums_rect = bomb_nums_surf.get_rect(center=(
                self.bomb_rect.centerx + 60,
                self.bomb_rect.centery
            ))
            self.screen.blit(self.bomb_image, self.bomb_rect)
            self.screen.blit(bomb_nums_surf, bomb_nums_rect)

            # 玩家生命值
            if self.player.life > 0:
                for i in range(self.player.life):
                    self.screen.blit(self.player.life_image, (
                        self.width - 10 - (i + 1) * self.player.life_rect.width,
                        self.height - 10 - self.player.life_rect.height
                    ))

        pygame.display.flip()
        self.clock.tick(60)

    def draw_desc(self):
        text1 = 'Welcome to Aircraft-Battle'
        text2 = 'Press any key to start the game'
        text1_surf = self.FONT.render(text1, False, "white")
        text1_rect = text1_surf.get_rect(center=(self.width / 2, self.height - 340))
        text2_surf = self.FONT.render(text2, False, "white")
        text2_rect = text2_surf.get_rect(center=(self.width / 2, self.height - 300))
        self.screen.blit(text1_surf, text1_rect)
        self.screen.blit(text2_surf, text2_rect)
        desc_rect = self.desc_image.get_rect(center=(self.width / 2, self.height - 180))
        self.screen.blit(self.desc_image, desc_rect)

    def draw_game_over(self):
        self.screen.blit(self.again_image, self.again_rect)
        self.screen.blit(self.over_image, self.over_rect)
        # 分数
        score_surf = self.FONT.render(f"Your Score: {self.score}", True, "white")
        score_rect = score_surf.get_rect(center=(self.width/2, self.height/2))
        self.screen.blit(score_surf, score_rect)

    def draw_confirm_mouse(self):
        # 鼠标check
        mouse_rect = pygame.mouse.get_pos()
        if self.again_rect.collidepoint(mouse_rect) or self.over_rect.collidepoint(mouse_rect):
            pygame.mouse.set_visible(False)
            self.screen.blit(self.mouse_image, pygame.mouse.get_pos())
        else:
            pygame.mouse.set_visible(True)


if __name__ == '__main__':
    ab = AircraftBattle()
    ab.main_loop()
