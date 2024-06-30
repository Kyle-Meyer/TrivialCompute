import pygame 
from enum import Enum
from colors import *

class textWidget(object):
    #Member vars same as menu pretty much 
    border_color = base3
    title = pygame.font.init()
    title_text = "place holder"
    title_text_size = 40
    ScreenCoords = (0,0)
    menu_width = 200    
    menu_height = 200
    border_thickness = 3
    rect = pygame.Rect(ScreenCoords[0], ScreenCoords[1], menu_width, menu_height)

    def draw_rounded_rect(self, surface):
        inner_rect = self.rect.inflate(-4 * self.border_thickness, -4 * self.border_thickness)
        pygame.draw.rect(surface, null, inner_rect, 0, 20) #hard setting the border radius as menus should be fixed "roundness"
        outer_rect = self.rect.inflate(self.border_thickness, self.border_thickness)
        pygame.draw.rect(surface, self.border_color, outer_rect, self.border_thickness, 20)
    
    def drawWidget(self, screen):
        if(self.border_thickness > 0):
            self.draw_rounded_rect(screen)
            text_surf = self.title.render(self.title_text, True, base3)
            text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.centery - (self.menu_height // 2) + self.title_text_size))
        else:
            text_surf = self.title.render(self.title_text, True, base3)
            text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.centery - (self.menu_height // 2) + self.title_text_size))
        screen.blit(text_surf, text_rect)

    def changeTextSize(self, inSize):
        self.title = pygame.font.Font(None, inSize)
        self.title_text_size = inSize

    def resizeBox(self, width, height):
        self.rect = pygame.Rect(self.ScreenCoords[0], self.ScreenCoords[1], width, height)
        self.menu_height = height
        self.menu_width = width

    def moveBox(self, inPosition):
        self.rect.centerx = inPosition[0]
        self.rect.centery = inPosition[1]

    def __init__(self, position : tuple[int, ...], width = 200, height = 200, inText = "place holder"):
        self.ScreenCoords = position
        self.menu_width = width
        self.menu_height = height
        self.rect = pygame.Rect(self.ScreenCoords[0], self.ScreenCoords[1], self.menu_width, self.menu_height)
        self.title_text = inText
        self.changeTextSize(height // 4)
        self.title = pygame.font.Font(None, self.title_text_size)
        self.resizeBox(width, height)
        self.moveBox(position)