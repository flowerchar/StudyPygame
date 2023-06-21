import pygame

pygame.init()


screen = pygame.display.set_mode([500, 500])
screen.fill("white")

dice = pygame.image.load("./dice.png")


rect_1 = pygame.Rect(100, 200, 100, 100)

rect2 = rect_1.move(10, 20)

rect_1.move_ip(10, 20)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(dice, rect_1.topleft)
    pygame.display.flip()


pygame.quit()
