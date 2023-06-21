import pygame

pygame.init()

pygame.display.set_mode((300, 500))
pygame.display.set_caption("我是一个标题")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    print(pygame.display.get_window_size())
    print(pygame.display.get_active())


pygame.quit()
