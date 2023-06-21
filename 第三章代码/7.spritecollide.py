import time

import pygame

pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("me.png")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


clock = pygame.time.Clock()
screen = pygame.display.set_mode((500, 500))

p = Player()
p.rect.midleft = (0, 250)


group = pygame.sprite.Group()
p1 = Player()
p2 = Player()
p3 = Player()
group.add(p1, p2, p3)
p1.rect.x = 100
p2.rect.x = 200
p3.rect.x = 300


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    # 碰撞检测
    collided = pygame.sprite.spritecollide(p, group, True, collided=pygame.sprite.collide_mask)
    print(len(group))

    p.rect.move_ip(1, 0)

    p1.rect.move_ip(0, 1)
    p2.rect.move_ip(0, 1)
    p3.rect.move_ip(0, 1)

    screen.fill("white")
    screen.blit(p.image, p.rect)
    screen.blits([(p1.image, p1.rect), (p2.image, p2.rect), (p3.image, p3.rect)])

    pygame.display.flip()
    clock.tick(60)



