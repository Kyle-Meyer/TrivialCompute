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
    mDistinct = tileDistinction.NORMAL
    mTrivia = triviaType.RED

    def is_inside_bounding_box(self, point_or_rect):
        """ Check if a point or another rectangle is inside the bounding box. """
        if isinstance(point_or_rect, pygame.Rect):
            return self.box.colliderect(point_or_rect)
        elif isinstance(point_or_rect, tuple):
            return self.box.collidepoint(point_or_rect)
        return False
    
    def __init__(self, inColor=(base0), dist = tileDistinction.NORMAL, inSize = 10):
        self.size = inSize
        self.box = pygame.Rect(300, 200, self.size, self.size)
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
                    case triviaType.BLUE:
                        self.mTrivia = triviaType.BLUE
                        self.mColor = blue
                    case triviaType.YELLOW:
                        self.mTrivia = triviaType.YELLOW
                        self.mColor = yellow
                    case triviaType.GREEN:
                        self.mTrivia = triviaType.GREEN
                        self.mColor = green
        
    def instantiateTile(self, inColor, inSize = 10):
        self.size = inSize
        self.box = pygame.Rect(300, 200, self.size, self.size)
        match inColor:
            case triviaType.RED:
                mColor = red
            case triviaType.BLUE:
                mColor = blue
            case triviaType.YELLOW:
                mColor = yellow
            case triviaType.WHITE:
                mColor = base2
    def setTileSize(inSize):
        tile.size = inSize