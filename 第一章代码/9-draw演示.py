import pygame

pygame.init()


screen = pygame.display.set_mode([500, 500])
screen.fill("white")

# 绘制普通直线
pygame.draw.line(screen, "black", (300, 100), (400, 150))

# 绘制抗锯齿直线
pygame.draw.aaline(screen, "black", (300, 150), (400, 200))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 绘制矩形
    pygame.draw.rect(screen, "black", (100, 100, 50, 50), width=1, border_radius=10)

    # 绘制圆形
    pygame.draw.circle(screen, "orange", (300, 300), 75, width=2)

    pygame.display.flip()


pygame.quit()
