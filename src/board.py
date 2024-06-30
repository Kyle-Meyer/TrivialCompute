import random
import sys
from tile import tile
from tile import triviaType
from tile import tileDistinction
import numpy
import pygame
import random
from colors import *
class cBoard(object):
    #done with strings for right now, will Tile object in future
    #X = tile
    #P = head quarter tile
    #. = blank space   

    template=[["R","X","X","X","H","X","X","X","R"],
             ["X",".",".",".","X",".",".",".","X"],
             ["X",".","P",".","X",".","P",".","X"],
             ["X",".",".",".","X",".",".",".","X"],
             ["H","X","X","X","X","X","X","X","H"],
             ["X",".",".",".","X",".",".",".","X"],
             ["X",".","P",".","X",".","P",".","X"],
             ["X",".",".",".","X",".",".",".","X"],
             ["R","X","X","X","H","X","X","X","R"],]
    #TODO add thje ability to save a string here that captures the colors of the board
    
    outerBoard = pygame.Rect(0, 0, 720 - 100, 720 - 100)
    outerBoard.center = (1280/2 , 720/2)
    tileSize = 0
    def create_board(self):
        for i in range(9):
            for j in range(9):
                match self.template[i][j]:
                    case "X":
                        print("tile size", self.board[i][j].box.size)
                        self.board[i][j] = tile(triviaType.RED)
                        roll = True
                        newColor = random.choice(list(triviaType))
                        print("setting new tile at ", i, " , ", j, " to ", newColor, " from ", self.board[i][j].mTrivia)
                        self.board[i][j] = tile(newColor)
                    case "P":
                        self.board[i][j] = tile(triviaType.RED, tileDistinction.SPECIAL)
                    case ".":
                        self.board[i][j] = tile(triviaType.RED, tileDistinction.NULL)
                    case "H":
                        self.board[i][j] = tile(triviaType.RED, tileDistinction.HQ)

    def drawBoard(self, screen, currentNeighbors):
        for col in range(9):
            for row in range(9):
                if self.board[col][row].mDistinct == tileDistinction.SPECIAL:
                    pygame.draw.rect(screen, self.board[col][row].mColor, self.board[col][row].box, 4)
                else:
                    if self.board[col][row].mDistinct != tileDistinction.NULL:
                        self.board[col][row].drawTile(screen)
                        if (col, row) in currentNeighbors:
                            pygame.draw.rect(screen, base3, self.board[col][row].box, 2)
                    else:
                        pygame.draw.rect(screen, self.board[col][row].mColor, self.board[col][row].box)

    def correctBoard(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j].mDistinct == tileDistinction.NORMAL:
                    possibleColors = [triviaType.BLUE, triviaType.GREEN, triviaType.YELLOW, triviaType.RED, triviaType.RED]
                    if i - 1 > 0 and self.board[i-1][j].mTrivia in possibleColors:
                        possibleColors.remove(self.board[i-1][j].mTrivia)
                    if i + 1 < 9 and self.board[i+1][j].mTrivia in possibleColors:
                        possibleColors.remove(self.board[i+1][j].mTrivia)
                    if j - 1 > 0 and self.board[i][j-1].mTrivia in possibleColors:
                        possibleColors.remove(self.board[i][j-1].mTrivia)
                    if j + 1 < 9 and self.board[i][j+1].mTrivia in possibleColors:
                        possibleColors.remove(self.board[i][j+1].mTrivia)
                    #add weight scoring to make sure we get a more even distribution of tiles
                    self.board[i][j] = tile(random.choice(possibleColors))
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.board = [ [tile(triviaType.RED) for j in range(9)] for i in range(9)]
        self.create_board()
        self.correctBoard()