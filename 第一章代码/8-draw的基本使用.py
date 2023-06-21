import pygame

pygame.init()

WHITE = (0, 0, 0)


screen = pygame.display.set_mode([500, 500])
# screen.fill(WHITE)
# screen.fill((125, 21, 219))     # rgb(red, green, blue) 0-255
# screen.fill((125, 21, 219, 0))     # rgba(red, green, blue, alpha) 0-255

a = pygame.Color(125, 21, 219)
screen.fill(a)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()


pygame.quit()
