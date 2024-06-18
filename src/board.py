import random
import sys
from tile import tile
from tile import triviaType
from tile import tileDistinction
import numpy
import pygame
import random
class cBoard(object):
    #done with strings for right now, will Tile object in future
    #X = tile
    #P = head quarter tile
    #. = blank space   

    template=[["X","X","X","X","X","X","X","X","X"],
             ["X",".",".",".","X",".",".",".","X"],
             ["X",".","P",".","X",".","P",".","X"],
             ["X",".",".",".","X",".",".",".","X"],
             ["X","X","X","X","X","X","X","X","X"],
             ["X",".",".",".","X",".",".",".","X"],
             ["X",".","P",".","X",".","P",".","X"],
             ["X",".",".",".","X",".",".",".","X"],
             ["X","X","X","X","X","X","X","X","X"],]
    outerBoard = pygame.Rect(0, 0, 720 - 100, 720 - 100)
    outerBoard.center = (1280/2 , 720/2)
    #this will randomly generate tiles in the future
    def create_board(self):
        for i in range(9):
            for j in range(9):
                match self.template[i][j]:
                    case "X":
                        self.board[i][j] = tile(triviaType.RED)
                        roll = True
                        newColor = random.choice(list(triviaType))
                        print("setting new tile at ", i, " , ", j, " to ", newColor, " from ", self.board[i][j].mTrivia)
                        self.board[i][j] = tile(newColor)
                    case "P":
                        self.board[i][j] = tile(triviaType.RED, tileDistinction.HQ)
                    case ".":
                        self.board[i][j] = tile(triviaType.RED, tileDistinction.NULL)
    #def setCore(self, limit : int):
    #    self.board[4][4].box =
    def correctBoard(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j].mDistinct == tileDistinction.NORMAL:
                    possibleColors = [triviaType.RED, triviaType.BLUE, triviaType.GREEN, triviaType.YELLOW]
                    if i - 1 > 0 and self.board[i-1][j].mTrivia in possibleColors:
                        possibleColors.remove(self.board[i-1][j].mTrivia)
                    if i + 1 < 9 and self.board[i+1][j].mTrivia in possibleColors:
                        possibleColors.remove(self.board[i+1][j].mTrivia)
                    if j - 1 > 0 and self.board[i][j-1].mTrivia in possibleColors:
                        possibleColors.remove(self.board[i][j-1].mTrivia)
                    if j + 1 < 9 and self.board[i][j+1].mTrivia in possibleColors:
                        possibleColors.remove(self.board[i][j+1].mTrivia)
                    print("on ", i, " ", j, " colors left: ", possibleColors)
                    #add weight scoring to make sure we get a more even distribution of tiles
                    self.board[i][j] = tile(random.choice(possibleColors))
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.board = [ [tile(triviaType.RED) for j in range(9)] for i in range(9)]
        self.create_board()
        self.correctBoard()