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

    #TODO add wild card center to template
    template=[["R","X","X","X","H","X","X","X","R"],
             ["X",".",".",".","X",".",".",".","X"],
             ["X",".","P",".","X",".","P",".","X"],
             ["X",".",".",".","X",".",".",".","X"],
             ["H","X","X","X","C","X","X","X","H"],
             ["X",".",".",".","X",".",".",".","X"],
             ["X",".","P",".","X",".","P",".","X"],
             ["X",".",".",".","X",".",".",".","X"],
             ["R","X","X","X","H","X","X","X","R"],]
    #TODO add thje ability to save a string here that captures the colors of the board
    HQs = [triviaType.RED, triviaType.BLUE, triviaType.YELLOW, triviaType.GREEN]
    outerBoard = pygame.Rect(0, 0, 720 - 100, 720 - 100)
    outerBoard.center = (1280/2 , 720/2)
    tileSize = 0
    def create_board(self):
        for i in range(9):
            for j in range(9):
                match self.template[i][j]:
                    case "X":
                        print("tile size", self.board[i][j].box.size)
                        newColor = random.choice(list(triviaType))
                        print("setting new tile at ", i, " , ", j, " to ", newColor, " from ", self.board[i][j].mTrivia)
                        self.board[i][j] = tile(triviaType.RED, tileDistinction.NORMAL, 10, i, j)
                    case "P":
                        self.board[i][j] = tile(triviaType.RED, tileDistinction.SPECIAL, 10, i, j)
                    case ".":
                        self.board[i][j] = tile(triviaType.RED, tileDistinction.NULL, 10, i, j)
                    case "H":
                        hqChoice = random.choice(self.HQs)
                        self.HQs.remove(hqChoice)
                        self.board[i][j] = tile(hqChoice, tileDistinction.HQ, 10, i, j)
                    case "R":
                        self.board[i][j] = tile(triviaType.RED, tileDistinction.ROLL, 10, i, j)
                    case "C":
                        self.board[i][j] = tile(triviaType.RED, tileDistinction.CENTER, 10, i, j)

    def drawBoard(self, screen, currentNeighbors):
        for col in range(9):
            for row in range(9):
                if self.board[col][row].mDistinct == tileDistinction.SPECIAL:
                    pygame.draw.rect(screen, self.board[col][row].mColor, self.board[col][row].box, 4)
                else:
                    if self.board[col][row].mDistinct != tileDistinction.NULL:
                        self.board[col][row].drawTile(screen)
                        if (col, row) in currentNeighbors:
                            pygame.draw.rect(screen, base3, self.board[col][row].box, 3)
                    else:
                        pygame.draw.rect(screen, self.board[col][row].mColor, self.board[col][row].box)

    def correctBoard(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j].mDistinct == tileDistinction.NORMAL:
                    possibleColors = [triviaType.BLUE, triviaType.GREEN, triviaType.YELLOW, triviaType.RED, triviaType.RED, triviaType.RED]
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
    def initializeBoard(self):
        rect_x, rect_y = self.width//4, self.height//4  # Position of the rectangle we always work in quadrants
        length = min(self.width, self.height)
        offset = max(self.width, self.height)
        rect_width, rect_height = length - (.1 * offset), length - (.1 * offset)  # Size of the rectangle
        cols, rows = 9, 9  # Number of columns and rows in the grid
        cell_width = rect_width // cols
        cell_height = rect_height // rows
        for col in range(cols):
            for row in range(rows):
                cell_x = rect_x + col * cell_width + (length * .4)
                cell_y = rect_y + row * cell_height - (length * .15)
                self.board[col][row].updateTile((cell_x, cell_y), cell_width, cell_height, col , row)

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [ [tile(triviaType.RED) for j in range(9)] for i in range(9)]
        self.create_board()
        self.correctBoard()
        self.initializeBoard()
        