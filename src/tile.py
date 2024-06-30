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
        #pygame.draw.rect(screen, base3, self.box, 1)

    def updateTile(self, inPosition, inWidth, inHeight):
        self.box = pygame.Rect(inPosition[0], inPosition[1], inWidth, inHeight)
        self.inner_box = pygame.Rect(inPosition[0], inPosition[1], inWidth, inHeight-10)

    def __init__(self, inColor=(base0), dist = tileDistinction.NORMAL, inSize = 10):
        self.size = inSize
        self.box = pygame.Rect(300, 200, self.size, self.size)
        self.inner_box = pygame.Rect(300, 200, self.size, self.size-10)
        self.mDistinct = dist
        self.Randomized=False
        match dist:
            case tileDistinction.NULL:
                self.mColor = null
            case tileDistinction.HQ:
                self.mColor = base3
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