import pygame
import sys
from colors import *

class checkBoxWidget(object):

    checkbox_rect = pygame.Rect(150, 100, 40, 40)
    outer_rect = pygame.Rect(160, 110, 50, 50)
    checked = False
    originalX = 0
    def listen(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Check if the mouse click is within the checkbox rectangle
                if self.outer_rect.collidepoint(event.pos):
                    self.checked = not self.checked
                    return self.checked

    def drawWidget(self, screen):
        pygame.draw.rect(screen, base3, self.outer_rect, 2)
        if self.checked:
            pygame.draw.rect(screen, base3, self.checkbox_rect)
            pygame.draw.rect(screen, null, self.checkbox_rect, 2)

    def __init__(self, inPosition, inWidth, inHeight):
        self.outer_rect = pygame.Rect(inPosition[0], inPosition[1], inWidth, inHeight)
        self.originalX = self.outer_rect.centerx
        self.checkbox_rect = pygame.Rect(inPosition[0], inPosition[1], inWidth-10, inHeight-10)
        self.checkbox_rect.center = self.outer_rect.center