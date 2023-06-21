import pygame

pygame.init()


screen = pygame.display.set_mode([500, 500])

face = pygame.Surface((50, 50))
face.fill("gold")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    screen.blit(face, (100, 100))
    # screen.blits()

    print(face.get_size())
    print(face.get_height())
    print(face.get_width())

    pygame.display.flip()

pygame.quit()
