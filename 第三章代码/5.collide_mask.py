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

p1 = Player()
p2 = Player()
p1.rect.midtop = (250, 0)
p2.rect.midleft = (0, 250)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    if pygame.sprite.collide_mask(p1, p2):
        time.sleep(1000)

    p1.rect.move_ip(0, 1)
    p2.rect.move_ip(1, 0)

    screen.fill("white")
    screen.blit(p1.image, p1.rect)
    screen.blit(p2.image, p2.rect)

    pygame.display.flip()
    clock.tick(60)



