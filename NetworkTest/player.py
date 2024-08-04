import pygame



class player(object):
    def __init__(self, inPos, inWidth, inHeight, inColor):
        self.rect = pygame.Rect(inPos[0], inPos[1], inWidth, inHeight)
        self.color = inColor
        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)