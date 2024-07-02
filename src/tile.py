import sys
import random
from enum import Enum
import pygame
from colors import *

class triviaType(Enum):
    RED = 0 
    BLUE = 1
    YELLOW = 2
    GREEN = 3
    WHITE = 4

class tileDistinction(Enum):
    NORMAL = 0
    HQ = 1
    ROLL = 2
    SPECIAL = 3
    NULL = 4
class tile(object):
    #standard convention in python to mark private variables with "__"
    
    size = 50
    mColor = (base0)
    mComplimentColor = (base0)
    mDistinct = tileDistinction.NORMAL
    mTrivia = triviaType.RED
    title = pygame.font.init()
    title_text = ""
    title_text_size = 40
    title_color = (base0)

    etitle = pygame.font.init()
    etitle_text = ""
    etitle_text_size = 40
    etitle_color = (base0)

    def is_inside_bounding_box(self, point_or_rect):
        """ Check if a point or another rectangle is inside the bounding box. """
        if isinstance(point_or_rect, pygame.Rect):
            return self.box.colliderect(point_or_rect)
        elif isinstance(point_or_rect, tuple):
            return self.box.collidepoint(point_or_rect)
        return False
    
    #def drawTile(self, screen):
    def drawTile(self, screen):
        #TODO move this to the tile class
        pygame.draw.rect(screen, self.mComplimentColor, self.box)
        pygame.draw.rect(screen, self.mColor, self.inner_box)
        pygame.draw.rect(screen, self.mComplimentColor, self.box, 3)
        if self.mDistinct == tileDistinction.HQ:
            text_surface = self.title.render(self.title_text, True, self.title_color)
            text_rect = text_surface.get_rect(center=(self.box.centerx, self.box.centery))
            screen.blit(text_surface, text_rect)
        elif self.mDistinct == tileDistinction.ROLL:
            text_surface = self.title.render(self.title_text, True, self.title_color)
            text_rect = text_surface.get_rect(center=(self.box.centerx, self.box.centery- (self.title_text_size // 2)))
            screen.blit(text_surface, text_rect)
            text_surface2 = self.etitle.render(self.etitle_text, True, self.etitle_color)
            text_rect2 = text_surface2.get_rect(center=(self.box.centerx, self.box.centery+ (self.etitle_text_size // 2)))
            screen.blit(text_surface2, text_rect2)
        #pygame.draw.rect(screen, base3, self.box, 1)

    def updateTile(self, inPosition, inWidth, inHeight):
        self.box = pygame.Rect(inPosition[0], inPosition[1], inWidth, inHeight)
        self.inner_box = pygame.Rect(inPosition[0], inPosition[1], inWidth, inHeight-10)

    def __init__(self, inColor, dist = tileDistinction.NORMAL, inSize = 10):
        self.size = inSize
        self.box = pygame.Rect(300, 200, self.size, self.size)
        self.inner_box = pygame.Rect(300, 200, self.size, self.size-10)
        self.mDistinct = dist
        self.title = pygame.font.Font(None, self.title_text_size)
        self.Randomized=False
        match dist:
            case tileDistinction.NULL:
                self.mColor = null
            case tileDistinction.HQ:
                self.title_text = "HQ"
                self.title_text_size = inSize * 3
                self.title = pygame.font.Font(None, self.title_text_size)
                match inColor:
                    case triviaType.RED:
                        self.mTrivia = triviaType.RED
                        self.mColor = HQ_red
                        self.mComplimentColor = HQ_dark_red                 
                        self.title_color = HQ_dark_red
                    case triviaType.BLUE:
                        self.mTrivia = triviaType.BLUE
                        self.mColor = HQ_blue
                        self.mComplimentColor = HQ_dark_blue
                        self.title_color = HQ_dark_blue
                    case triviaType.GREEN:
                        self.mTrivia = triviaType.GREEN
                        self.mColor = HQ_green
                        self.mComplimentColor = HQ_dark_green
                        self.title_color = HQ_dark_green
                    case triviaType.YELLOW:
                        self.mTrivia = triviaType.YELLOW
                        self.mColor = HQ_yellow
                        self.mComplimentColor = HQ_dark_yellow
                        self.title_color = HQ_dark_yellow
            case tileDistinction.ROLL:
                self.mColor = base3
                self.mComplimentColor=base0
                self.title_text = "Roll"
                self.title_color = base0
                self.title_text_size = inSize * 2
                self.etitle_text = "Again"
                self.etitle_color = base0
                self.etitle_text_size = inSize * 2
                self.etitle = pygame.font.Font(None, self.etitle_text_size)
                self.title = pygame.font.Font(None, self.title_text_size)
            case tileDistinction.SPECIAL:
                self.mColor = base00
            case tileDistinction.NORMAL:
                match inColor:
                    case triviaType.RED:
                        self.mTrivia = triviaType.RED
                        self.mColor = red
                        self.mComplimentColor = darkRed
                    case triviaType.BLUE:
                        self.mTrivia = triviaType.BLUE
                        self.mColor = blue
                        self.mComplimentColor = darkBlue
                    case triviaType.YELLOW:
                        self.mTrivia = triviaType.YELLOW
                        self.mColor = yellow
                        self.mComplimentColor = darkYellow
                    case triviaType.GREEN:
                        self.mTrivia = triviaType.GREEN
                        self.mColor = green
                        self.mComplimentColor = darkGreen

    def setTileSize(inSize):
        tile.size = inSize