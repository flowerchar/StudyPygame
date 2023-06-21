import pygame
import sys

# 红橙黄绿蓝青紫
COLORS = ["red", "orange", "yellow", "green", "blue", "cyan", "purple"]
NUM = 7

size = 100
padx = 50 # 方格间的水平间距
cx, cy = 80, 50

WIDTH = cx + NUM * size + padx * (NUM-1) + cx

pygame.init()
win = pygame.display.set_mode((WIDTH,240))
clock = pygame.time.Clock()

# 把点击数也放到专门的列表中
counts = []
for i in range(NUM):
    counts.append(0)

font = pygame.font.SysFont(None, 30)

while True:
    win.fill("black")

    # 使用循环，计算各个矩形和文本的位置，并进行绘制
    for i in range(NUM):
        color = COLORS[i]
        xi = cx + i * (size + padx)
        rect = pygame.Rect(xi, cy, size, size)
        pygame.draw.rect(win, color, rect)
        text = font.render(str(counts[i]), True, color)

        win.blit(text, (xi, cy + size + 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            px, py = event.pos
            for i in range(NUM):
                xi = cx + i * (size + padx)
                if xi <= px < xi + size and cy <= py <= cy +size:
                    counts[i] += 1

    clock.tick(60)
    pygame.display.update()