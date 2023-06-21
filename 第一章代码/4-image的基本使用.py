import pygame

pygame.init()


screen = pygame.display.set_mode([500, 500])
screen.fill("white")

dice = pygame.image.load("./dice.png")

pygame.image.save(screen, "screen.png")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(dice, (100, 300))

    pygame.display.flip()


pygame.quit()
