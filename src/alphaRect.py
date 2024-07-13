import pygame
from colors import *

class alphaRect(object):
    rect_width, rect_height = 400, 200
    rect_surface = pygame.Surface((rect_width, rect_height))
    rect_surface.set_alpha(128)
    color = null
    x, y = 0, 0 

    def setCenter(self, inX, inY):
        self.x = inX
        self.y = inY

    def drawAlpha(self, screen : pygame.Surface):
        #print("Alpha draw called ", self.x,  " ", self.y)
        self.rect_surface = pygame.Surface((self.rect_width, self.rect_height))
        self.rect_surface.set_alpha(self.alpha)
        self.rect_surface.fill(self.color)
        screen.blit(self.rect_surface, (self.x, self.y))
                    
    def __init__(self, inPosition, widht, height, alpha = 128):
        self.rect_width = widht
        self.rect_height = height
        self.x = inPosition[0]
        self.y = inPosition[1]
        self.rect_surface = pygame.Surface((widht, height))
        self.rect_surface.set_alpha(alpha)
        self.alpha = alpha
        self.rect_surface.fill(debug_red)