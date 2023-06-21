import pygame

pygame.init()

screen = pygame.display.set_mode((100, 200))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("jet.png")
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)    # 可选

    def update(self):
        print(12345)


p1 = Player()
p2 = Player()

p1.rect.y = 50

p2.rect.y = 150


group_1 = pygame.sprite.Group()
group_2 = pygame.sprite.Group()


group_1.add(p1, p2)
print(group_1.sprites())

# group_1.remove(p1)
#
#
# print(group_1.has(p2))
# print(p1 in group_1)

# group_1.empty()
# print(group_1.sprites())


# group_1.update()

for s in group_1:
    print(s.image)


# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             quit()
#
#     screen.fill("black")
#     group_1.draw(screen)
#
#     pygame.display.flip()



