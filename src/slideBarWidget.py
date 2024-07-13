import pygame
import sys 
from colors import *

class slideBarWidget(object):

    slider_length = 300 #the background bar
    slider_height = 20 #the 
    thumb_width = 20
    thumb_height = 40
    dragging = False  # To track whether the thumb is being dragged
    ScreenCoords = (0,0)
    width, height = 0,0
    rect = pygame.Rect(ScreenCoords[0], ScreenCoords[1], width, height)
    sliderRect = pygame.Rect(ScreenCoords[0], ScreenCoords[1], slider_length, slider_height)
    thumbRect = pygame.Rect(ScreenCoords[0], ScreenCoords[1], thumb_width, thumb_height)
    value = 50
    storedXVal = 0
    def draw(self, screen):
        pygame.draw.rect(screen, base3, self.sliderRect)
        pygame.draw.rect(screen, debug_red, self.sliderRect, 3)
        pygame.draw.rect(screen, base03, self.thumbRect)
        pygame.draw.rect(screen, debug_red, self.thumbRect, 3 )
        pygame.draw.rect(screen, debug_red, self.rect, 3)

    def get_slider_value(self):
        """ Calculate the slider value based on the thumb's position. """
        range_start = self.sliderRect.x
        range_end = self.sliderRect.x + self.slider_length - self.thumb_width
        return int((self.thumbRect.x - range_start) / (range_end - range_start) * 100)
    
    def listen(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.thumbRect.x <= event.pos[0] <= self.thumbRect.x + self.thumb_width and self.thumbRect.y <= event.pos[1] <= self.thumbRect.y + self.thumb_height:
                    self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # Move the thumb within the slider bounds
                self.thumbRect.x = min(max(event.pos[0] - self.thumb_width // 2, self.sliderRect.x), self.sliderRect.x + self.slider_length - self.thumb_width)
                print(self.thumbRect.x)
       
        self.value = self.get_slider_value()
        #print("X coord of thumb: ", self.thumbRect.centerx, " val: ", self.value)
    
    def moveAll(self, inPos):
        self.rect.center = inPos
        self.sliderRect.centerx = self.rect.centerx
        self.thumbRect.centerx = self.rect.centerx
        self.sliderRect.centery = self.rect.centery
        self.thumbRect.centery = self.rect.centery

    def __init__(self, inPosition, inWidth, inHeight):
        self.ScreenCoords = inPosition
        self.width = inWidth
        self.height = inHeight
        self.rect.width = inWidth
        self.rect.height = inHeight
        print("!!!!!!!!!!!!!!!!!!!", inPosition)
        self.rect.center = inPosition
        self.sliderRect = pygame.Rect(self.ScreenCoords[0], self.ScreenCoords[1], self.slider_length, self.slider_height)
        self.thumbRect = pygame.Rect(self.ScreenCoords[0], self.ScreenCoords[1], self.thumb_width, self.thumb_height)
        self.sliderRect.centerx = self.rect.centerx
        self.thumbRect.centerx = self.rect.centerx
        self.sliderRect.centery = self.rect.centery
        self.thumbRect.centery = self.rect.centery