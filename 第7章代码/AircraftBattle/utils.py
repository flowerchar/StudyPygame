import pygame


def load_image(filename, alpha=True):
    surf = pygame.image.load(filename)
    if alpha:
        return surf.convert_alpha()
    return surf.convert()
