import sys
import random
from enum import Enum
import pygame
from colors import *

class triviaType(Enum):
    RED = 0 
    BLUE = 1
    YELLOW = 2
    WHITE = 3


class tile(object):
    #standard convention in python to mark private variables with "__"
    
    size = 50
    mColor = (0,0,0)


    def __init__(self, inColor, inSize = 10):
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
    @classmethod
    def emptyTile(cls) -> 'tile':
        print("later")
    def setTileSize(inSize):
        tile.size = inSize