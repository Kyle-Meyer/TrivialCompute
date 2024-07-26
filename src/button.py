import pygame
import sys
from colors import *
from alphaRect import alphaRect

class button(object):

    #member varaibles that are all accessible at any time
    button_width, button_height = 100, 50
    button_Position_Screen = (0,0)
    button_inner_color = null
    button_outline_color = base3
    #button_size = 10
    button_rect = pygame.Rect(100, 100, button_width, button_height)
    border_thickness = 0
    border_radius = 10
    button_font = pygame.font.init()
    button_text_size = 0
    button_text = " place holder "
    button_text_color = yellow#base3
    fadeBox = alphaRect((0,0), 1, 1)
    lockOut = False
    originalX = 0
    savedTextColor = yellow
    originalY = 0
    def draw_rounded_rect(self, surface):
        """ Draw a rectangle with rounded corners.
        If border_thickness is set, it will draw both the border and the fill color.
        """
        if self.border_radius < 0:
            raise ValueError("border_radius must be >= 0")
        if self.border_thickness > 0:
            inner_rect = self.button_rect.inflate(-4 * self.border_thickness, -4 * self.border_thickness)
            pygame.draw.rect(surface, self.button_inner_color, inner_rect, 0, self.border_radius)
            outer_rect = self.button_rect.inflate(self.border_thickness, self.border_thickness)
            pygame.draw.rect(surface, self.button_outline_color, outer_rect, self.border_thickness, self.border_radius)
        else:
            pygame.draw.rect(surface, self.button_inner_color, self.button_rect, 0, self.border_radius)
    
    def draw_button(self, screen):
        screen.set_alpha(10)
        self.draw_rounded_rect(screen)
        text_surf = self.button_font.render(self.button_text, True, self.button_text_color)
        text_rect = text_surf.get_rect(center=self.button_rect.center)
        screen.blit(text_surf, text_rect)
        if self.lockOut:
            self.button_inner_color = null
            self.oldColor = null
            self.button_text_color = base3
            self.oldTextColor = self.savedTextColor
            self.fadeBox.drawAlpha(screen)
    #TODO add lockout state to buttons
    
    def isClicked(self, event):
        if not self.lockOut:
            mouse_pos = pygame.mouse.get_pos()
            #highlight the button white when we hover over it
            if self.button_rect.collidepoint(mouse_pos):
                self.button_inner_color = base3
                self.button_text_color = base03
            else:
                self.button_inner_color = self.oldColor
                self.button_text_color = self.oldTextColor
            if event.type == pygame.QUIT:
                    return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #if event.button == 1:  # Left mouse click
                if self.button_rect.collidepoint(event.pos):
                    print(self.button_text, "clicked!")
                    return True
        
    def updateTextColor(self, inColor):
        self.oldTextColor = inColor
        self.button_text_color = inColor
        self.savedTextColor = inColor
        
    def updateInnerColor(self, inColor):
        self.oldColor = inColor

    def changeTextSize(self, inSize):
        
        self.button_text_size = inSize
        self.button_font = pygame.font.Font(None, inSize)

    def resizeBox(self, width, height):
        self.button_rect = pygame.Rect(self.button_Position_Screen[0], self.button_Position_Screen[1], width, height)
        self.fadeBox.rect_width = width + int(width * .1)
        self.fadeBox.rect_height = height + int(height * .1)

    def moveBox(self, inPosition):
        self.button_rect.centerx = inPosition[0]
        self.originalX = self.button_rect.centerx
        self.originalY = self.button_rect.centery
        self.button_rect.centery = inPosition[1]
        self.fadeBox.x = self.button_rect.x - int(self.button_rect.width * .05)
        self.fadeBox.y = self.button_rect.y - int(self.button_rect.height * .05)
        
    def updateFadeBox(self):
        self.fadeBox.x = self.button_rect.x - int(self.button_rect.width * .05)
        self.fadeBox.y = self.button_rect.y - int(self.button_rect.height * .05)
        
    def __init__(self, inPosition, width = 300, height = 100, inText = "place holder"):
        self.button_Position_Screen = inPosition
        self.button_width = width
        self.button_height = height
        self.border_thickness = 3
        self.button_text_size = max(width, height) // 5
        self.button_font = pygame.font.Font(None, self.button_text_size)
        self.button_text = inText
        self.oldColor = self.button_inner_color
        self.oldTextColor = self.button_text_color
        self.resizeBox(width, height)
        self.moveBox(inPosition)
        #setup the fade out box
        self.fadeBox = alphaRect((self.button_rect.x - int(width * .05), self.button_rect.y - int(height * .05)), width + int(width * .1), height + int(height * .1), 128)
        self.originalX = self.button_rect.centerx
        self.originalY = self.button_rect.centery
        self.savedTextColor = yellow
        
    
