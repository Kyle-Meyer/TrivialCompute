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
    CENTER = 4
    NULL = 5
    PLAYER1 = 6
    PLAYER2 = 7
    PLAYER3 = 8
    PLAYER4 = 9

class tile(object):
    #standard convention in python to mark private variables with "__"
    
    optionThreeDimensiaonalTiles = True
    size = 50
    mColor = (base0)
    mComplimentColor = (base0)
    mDistinct = tileDistinction.NORMAL
    mTrivia = triviaType.RED
    title = pygame.font.init()
    title_text = ""
    title_text_size = 40
    title_color = (base0)
    row = 0
    col = 0
    etitle = pygame.font.init()
    etitle_text = ""
    etitle_text_size = 40
    etitle_color = (base0)
    debugMode = True

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
        if(self.optionThreeDimensiaonalTiles):
            if self.mDistinct not in (tileDistinction.PLAYER1,tileDistinction.PLAYER2,
                                      tileDistinction.PLAYER3,tileDistinction.PLAYER4,
                                      tileDistinction.SPECIAL):
                pygame.draw.rect(screen, debug_red, self.box)
                pygame.draw.rect(screen, self.mComplimentColor, self.box)
                pygame.draw.rect(screen, self.mColor, self.inner_box)
                pygame.draw.rect(screen, self.mComplimentColor, self.box, 3)
            else:
                pygame.draw.rect(screen, self.mColor, self.box)
        else:
            pygame.draw.rect(screen, self.mColor, self.box)
        if self.mDistinct in (tileDistinction.SPECIAL,tileDistinction.PLAYER1,
                              tileDistinction.PLAYER2,tileDistinction.PLAYER3,
                              tileDistinction.PLAYER4,tileDistinction.HQ):
            text_surface = self.title.render(self.title_text, True, self.title_color)
            text_rect = text_surface.get_rect(center=(self.box.centerx, self.box.centery))
            screen.blit(text_surface, text_rect)
        elif self.mDistinct == tileDistinction.ROLL or self.mDistinct == tileDistinction.CENTER:
            text_surface = self.title.render(self.title_text, True, self.title_color)
            text_rect = text_surface.get_rect(center=(self.box.centerx, self.box.centery- (self.title_text_size // 2)))
            screen.blit(text_surface, text_rect)
            text_surface2 = self.etitle.render(self.etitle_text, True, self.etitle_color)
            text_rect2 = text_surface2.get_rect(center=(self.box.centerx, self.box.centery+ (self.etitle_text_size // 2)))
            screen.blit(text_surface2, text_rect2)
        elif self.debugMode:
            self.title_color = base3
            self.title_text = str(str(self.row) + ":" + str(self.col))
            text_surface = self.title.render(self.title_text, True, self.title_color)
            text_rect = text_surface.get_rect(center=(self.box.centerx, self.box.centery))
            screen.blit(text_surface, text_rect)
        #pygame.draw.rect(screen, base3, self.box, 1)

    def updateTile(self, inPosition, inWidth, inHeight, row, col):
        self.box = pygame.Rect(inPosition[0], inPosition[1], inWidth, inHeight)
        self.inner_box = pygame.Rect(inPosition[0], inPosition[1], inWidth, inHeight-10)
        self.row = row
        self.col = col

    def __init__(self, inColor, dist = tileDistinction.NORMAL, inSize = 10, row = 0, col = 0):
        self.size = inSize
        self.box = pygame.Rect(300, 200, self.size, self.size)
        self.inner_box = pygame.Rect(300, 200, self.size, self.size-10)
        self.mDistinct = dist
        self.row = row
        self.col = col
        self.title = pygame.font.Font(None, self.title_text_size)
        self.Randomized=False
        match dist:
            case tileDistinction.NULL:
                self.mColor = null
            case tileDistinction.PLAYER1:
                self.title_text = ""
                self.title_text_size = inSize * 3
                self.title = pygame.font.Font(None, self.title_text_size)                
                self.mColor = null
                self.title_color = white
            case tileDistinction.PLAYER2:
                self.title_text = ""
                self.title_text_size = inSize * 3
                self.title = pygame.font.Font(None, self.title_text_size)                
                self.mColor = null
                self.title_color = white
            case tileDistinction.PLAYER3:
                self.title_text = ""
                self.title_text_size = inSize * 3
                self.title = pygame.font.Font(None, self.title_text_size)                
                self.mColor = null
                self.title_color = white
            case tileDistinction.PLAYER4:
                self.title_text = ""
                self.title_text_size = inSize * 3
                self.title = pygame.font.Font(None, self.title_text_size)                
                self.mColor = null
                self.title_color = white                  
            case tileDistinction.HQ:
                self.title_text = "HQ"
                self.title_text_size = inSize * 3
                self.title = pygame.font.Font(None, self.title_text_size)
                match inColor:
                    case triviaType.RED:
                        self.mTrivia = triviaType.RED
                        self.mColor = HQ_red
                        self.mComplimentColor = HQ_dark_red                 
                        self.title_color = black #HQ_dark_red
                    case triviaType.BLUE:
                        self.mTrivia = triviaType.BLUE
                        self.mColor = HQ_blue
                        self.mComplimentColor = HQ_dark_blue
                        self.title_color = black #HQ_dark_blue
                    case triviaType.GREEN:
                        self.mTrivia = triviaType.GREEN
                        self.mColor = HQ_green
                        self.mComplimentColor = HQ_dark_green
                        self.title_color = black #HQ_dark_green
                    case triviaType.YELLOW:
                        self.mTrivia = triviaType.YELLOW
                        self.mColor = HQ_yellow
                        self.mComplimentColor = HQ_dark_yellow
                        self.title_color = black #HQ_dark_yellow
            case tileDistinction.ROLL:
                self.mColor = base3
                self.mComplimentColor=base0
                self.title_text = "Roll"
                self.title_color = black #base0
                self.title_text_size = inSize * 2
                self.etitle_text = "Again"
                self.etitle_color = black #base0
                self.etitle_text_size = inSize * 2
                self.etitle = pygame.font.Font(None, self.etitle_text_size)
                self.title = pygame.font.Font(None, self.title_text_size)
            case tileDistinction.CENTER:
                self.mColor = magenta
                self.mComplimentColor=violet
                self.title_text = "Trivial"
                self.title_color = black #violet
                self.title_text_size = inSize * 2
                self.etitle_text = "Compute"
                self.etitle_color = black #violet
                self.etitle_text_size = inSize * 2
                self.etitle = pygame.font.Font(None, self.etitle_text_size)
                self.title = pygame.font.Font(None, self.title_text_size)
            case tileDistinction.SPECIAL:
                self.mColor = null
                self.title_text = "____"
                self.title_text_size = inSize * 3
                self.title = pygame.font.Font(None, self.title_text_size)                
                self.title_color = null
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