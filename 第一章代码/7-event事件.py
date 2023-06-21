import pygame

pygame.init()


screen = pygame.display.set_mode([500, 500])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            print("用户敲了一个A键")

        # print(str(event))

    pygame.display.flip()


pygame.quit()
