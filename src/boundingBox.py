import pygame

class boundingBox(object):
    box = pygame.Rect(300, 200, 200, 200)
    def __init__(self, size = 40, center = (10, 10)):
        self.box = pygame.Rect(center[0], center[1], size, size)
        self.box.center = (center)