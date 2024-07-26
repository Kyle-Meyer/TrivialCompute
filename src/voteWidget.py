import sys
import pygame
from colors import *

class voteWidget(object):
    def __init__(self, inPosition, inWidth, inHeight):
        self.outer_rect = pygame.Rect(inPosition[0], inPosition[1], inWidth, inHeight)
        self.originalX = self.outer_rect.centerx
        self.originalY = self.outer_rect.centery
        self.checkbox_rect = pygame.Rect(inPosition[0], inPosition[1], inWidth-10, inHeight-10)
        self.checkbox_rect.center = self.outer_rect.center
        self.voteSubmitted = False

    def drawWidget(self, screen):
        self.checkbox_rect.center = self.outer_rect.center #im so lazy
        pygame.draw.rect(screen, base3, self.outer_rect, 2)
        if self.voteSubmitted:
            pygame.draw.rect(screen, green, self.checkbox_rect)
        else:
            pygame.draw.rect(screen, red, self.checkbox_rect)
        pygame.draw.rect(screen, null, self.checkbox_rect, 2)