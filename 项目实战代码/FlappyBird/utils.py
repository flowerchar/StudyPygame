import pygame


def load_image(filename, alpha=True):
    s = pygame.image.load(filename)
    if alpha:
        return s.convert_alpha()
    return s.convert()
