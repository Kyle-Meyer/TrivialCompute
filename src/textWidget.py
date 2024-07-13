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
    border_thickness = 0
    originalX = 0
    rect = pygame.Rect(ScreenCoords[0], ScreenCoords[1], menu_width, menu_height)

    def draw_rounded_rect(self, surface):
        inner_rect = self.rect.inflate(-4 * self.border_thickness, -4 * self.border_thickness)
        pygame.draw.rect(surface, null, inner_rect, 0, 20) #hard setting the border radius as menus should be fixed "roundness"
        outer_rect = self.rect.inflate(self.border_thickness, self.border_thickness)
        pygame.draw.rect(surface, self.border_color, outer_rect, self.border_thickness, 20)
    
    # def drawWidget(self, screen):
    #     if(self.border_thickness > 0):
    #         self.draw_rounded_rect(screen)
    #         text_surf = self.title.render(self.title_text, True, base3)
    #         text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.centery - (self.menu_height // 2) + self.title_text_size))
    #     else:
    #         text_surf = self.title.render(self.title_text, True, base3)
    #         text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.centery - (self.menu_height // 2) + self.title_text_size))
    #     screen.blit(text_surf, text_rect)

    def drawWidget(self, screen):
        if(self.border_thickness > 0):
            self.draw_rounded_rect(screen)
        
        # Render text with word wrap
        wrapped_lines = self.wrap_text(self.title_text, self.rect.width - self.border_thickness * 2)
        y = self.rect.centery - (self.menu_height // 2) + self.title_text_size
        for line in wrapped_lines:
            if line == '_':
                textCol = null
            else:
                textCol = yellow
            text_surf = self.title.render(line, True, textCol)#base3)
            text_rect = text_surf.get_rect(center=(self.rect.centerx, y))
            screen.blit(text_surf, text_rect)
            y += text_rect.height  # Move to the next line

    def wrap_text(self, text, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''
        
        for word in words:
            test_line = current_line + ' ' + word if current_line != '' else word
            test_size = self.title.size(test_line)
            
            if test_size[0] < max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines

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
        self.originalX = inPosition[0]
        
    def updateText(self, inText):
        self.title_text = inText;        

    def __init__(self, position : tuple[int, ...], width = 200, height = 200, inText = "place holder"):
        self.ScreenCoords = position
        self.originalX = position[0]
        self.menu_width = width
        self.menu_height = height
        self.rect = pygame.Rect(self.ScreenCoords[0], self.ScreenCoords[1], self.menu_width, self.menu_height)
        self.title_text = inText
        self.changeTextSize(height // 4)
        self.title = pygame.font.Font(None, self.title_text_size)
        self.resizeBox(width, height)
        self.moveBox(position)