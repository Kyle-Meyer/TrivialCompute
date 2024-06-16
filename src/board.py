import random
import sys
from tile import tile
from tile import triviaType
import numpy
import pygame
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
    board = numpy.empty(shape=(9,9), dtype=tile)
    outerBoard = pygame.Rect(0, 0, 720 - 100, 720 - 100)
    outerBoard.center = (1280/2 , 720/2)
    #this will randomly generate tiles in the future
    def create_board(self):
        for i in range(9):
            for j in range(9):
                match self.template[i][j]:
                    case "X":
                        self.board[i][j] = tile(triviaType.RED)
                    case ".":
                        self.board[i][j] = tile.emptyTile()
    #def setCore(self, limit : int):
    #    self.board[4][4].box = 
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.create_board()