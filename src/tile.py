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

class tileDistinction(Enum):
    NORMAL = 0
    HQ = 1
    NULL = 2
class tile(object):
    #standard convention in python to mark private variables with "__"
    
    size = 50
    mColor = (base0)
    mDistinct = tileDistinction.NORMAL
    mTrivia = triviaType.RED
    def __init__(self, inColor=(base0), dist = tileDistinction.NORMAL, inSize = 10):
        self.size = inSize
        self.box = pygame.Rect(300, 200, self.size, self.size)
        self.mDistinct = dist
        self.Randomized=False
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
        match dist:
            case tileDistinction.NULL:
                self.mColor = null
            case tileDistinction.HQ:
                self.mColor = base3
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