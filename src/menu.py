import pygame 
from button import button
from colors import *

class menu(object):

    #member vars
    border_color = base3
    title = pygame.font.init()
    title_text = "place holder"
    title_text_size = 40
    button_list = [] #this can remain empty
    ScreenCoords = (0,0)
    menu_width = 200    
    menu_height = 200
    border_thickness = 3
    rect = pygame.Rect(ScreenCoords[0], ScreenCoords[1], menu_width, menu_height)

    #copy pasted from button class, I should probably separate this out into its own object, but for now its fine
    def draw_rounded_rect(self, surface):
        """ Draw a rectangle with rounded corners.
        If border_thickness is set, it will draw both the border and the fill color.
        """
        if self.border_thickness > 0:
            inner_rect = self.rect.inflate(-4 * self.border_thickness, -4 * self.border_thickness)
            #inner color will always be null
            pygame.draw.rect(surface, null, inner_rect, 0, 20) #hard setting the border radius as menus should be fixed "roundness"
            outer_rect = self.rect.inflate(self.border_thickness, self.border_thickness)
            pygame.draw.rect(surface, self.border_color, outer_rect, self.border_thickness, 20)
        else:
            raise ValueError("border must be >= 0")
    
    def drawMenu(self, screen):
        self.draw_rounded_rect(screen)
        text_surf = self.title.render(self.title_text, True, base3)
        text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.centery - (self.menu_height // 2) + self.title_text_size + 5))
        screen.blit(text_surf, text_rect)

    def resizeBox(self, width, height):
        self.button_rect = pygame.Rect(self.ScreenCoords[0], self.ScreenCoords[1], width, height)
    
    def moveBox(self, inPosition):
        self.button_rect = pygame.Rect(inPosition[0], inPosition[1], self.menu_width, self.menu_height) 

    def __init__(self, position : tuple[int, ...], width = 200, height = 200):
        self.ScreenCoords = position
        self.menu_width = width
        self.menu_height = height
        self.rect = pygame.Rect(self.ScreenCoords[0], self.ScreenCoords[1], self.menu_width, self.menu_height)
        self.title = pygame.font.Font(None, self.title_text_size)
        self.resizeBox(width, height)
        self.moveBox(position)
