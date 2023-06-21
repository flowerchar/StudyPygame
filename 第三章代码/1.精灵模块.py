import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("jet.png")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)    # 可选


p = Player()
# print(p.image)
# print(p.rect)
# print(p.mask)

group_1 = pygame.sprite.Group()
group_2 = pygame.sprite.Group()
group_3 = pygame.sprite.Group()

print(p.alive())

print(p.groups())
p.add(group_1, group_2, group_3)          # 加到一个组中
print(p.groups())
#
# print(p.alive())
#
#
# p.remove(group_1, group_3)              # 离开一个组
# print(p.groups())

p.kill()

print(p.groups())
print(p.alive())


