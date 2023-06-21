import pygame

pygame.init()


screen = pygame.display.set_mode([500, 500])
screen.fill("white")

dice = pygame.image.load("./dice.png")
dice_rect = dice.get_rect(x=100, y=100)

rect_1 = pygame.Rect(100, 200, 89, 90)
rect_2 = pygame.Rect((100, 200), (89, 90))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(dice, rect_2)
    pygame.display.flip()


pygame.quit()
