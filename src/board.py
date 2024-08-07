import random
import sys
from tile import tile
from tile import triviaType
from tile import tileDistinction
import numpy
import pygame
import random
from colors import *
from configOptions import *
class cBoard(object):
    #done with strings for right now, will Tile object in future
    #X = tile
    #P = head quarter tile
    #. = blank space   

    #TODO add wild card center to template
    template=[["R","X","X","X","H","X","X","X","R"],
             ["X",".",".",".","X",".",".",".","X"],
             ["X","L","P",".","X","M","P",".","X"],
             ["X",".",".",".","X",".",".",".","X"],
             ["H","X","X","X","C","X","X","X","H"],
             ["X",".",".",".","X",".",".",".","X"],
             ["X","N","P",".","X","O","P",".","X"],
             ["X",".",".",".","X",".",".",".","X"],
             ["R","X","X","X","H","X","X","X","R"],]
    
    #TODO add thje ability to save a string here that captures the colors of the board
    HQs = [triviaType.RED, triviaType.BLUE, triviaType.YELLOW, triviaType.GREEN]
    outerBoard = pygame.Rect(0, 0, 720 - 100, 720 - 100)
    outerBoard.center = (1280/2 , 720/2)
    tileSize = 0
    rect_x, rect_y = 140, 130

    def create_board(self):
        self.board = [ [tile(triviaType.RED) for j in range(9)] for i in range(9)]
        if configModule.optionalStaticBoard == True:
            self.template= \
                    [["R","C4","C3","C2","HQ1","C4","C3","C2","R"],
                    ["C1",".",".",".","C2",".",".",".","C1"],
                    ["C2","L","P",".","C3","M","P",".","C4"],
                    ["C3",".",".",".","C4",".",".",".","C3"],
                    ["HQ4","C1","C2","C3","C","C1","C4","C3","HQ2"],
                    ["C1",".",".",".","C2",".",".",".","C1"],
                    ["C2","N","P",".","C1","O","P",".","C4"],
                    ["C3",".",".",".","C4",".",".",".","C3"],
                    ["R","C4","C1","C2","HQ3","C4","C1","C2","R"],]
            

        for i in range(9):
            for j in range(9):
                match self.template[i][j]:
                    case "X":
                        newColor = random.choice(list(triviaType))
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
                    case "L":
                        self.board[i][j] = tile(triviaType.RED, tileDistinction.PLAYER1, 10, i, j)
                    case "M":
                        self.board[i][j] = tile(triviaType.RED, tileDistinction.PLAYER2, 10, i, j)
                    case "N":
                        self.board[i][j] = tile(triviaType.RED, tileDistinction.PLAYER3, 10, i, j)
                    case "O":
                        self.board[i][j] = tile(triviaType.RED, tileDistinction.PLAYER4, 10, i, j)                                                                        
                    case "C4":
                        self.board[i][j] = tile(triviaType.RED, tileDistinction.NORMAL, 10, i, j)
                    case "C3":
                        self.board[i][j] = tile(triviaType.GREEN, tileDistinction.NORMAL, 10, i, j)       
                    case "C2":
                        self.board[i][j] = tile(triviaType.BLUE, tileDistinction.NORMAL, 10, i, j)      
                    case "C1":
                        self.board[i][j] = tile(triviaType.YELLOW, tileDistinction.NORMAL, 10, i, j)    
                    case "HQ4":
                        self.board[i][j] = tile(triviaType.RED, tileDistinction.HQ, 10, i, j)
                    case "HQ3":
                        self.board[i][j] = tile(triviaType.GREEN, tileDistinction.HQ, 10, i, j)       
                    case "HQ2":
                        self.board[i][j] = tile(triviaType.BLUE, tileDistinction.HQ, 10, i, j)      
                    case "HQ1":
                        self.board[i][j] = tile(triviaType.YELLOW, tileDistinction.HQ, 10, i, j)                                                            
                                                                                     

    def drawBoard(self, screen, currentNeighbors):
               
        for col in range(9):
            for row in range(9):
                if self.board[col][row].mDistinct != tileDistinction.NULL:
                    self.board[col][row].drawTile(screen)
                    if (col, row) in currentNeighbors:
                        pygame.draw.rect(screen, base3, self.board[col][row].box, 5)
                else:
                    pygame.draw.rect(screen, self.board[col][row].mColor, self.board[col][row].box)

                # Add optional thin black border around tiles
                if(configModule.optionalTileBlackOutline):
                    if self.board[col][row].mDistinct not in (tileDistinction.NULL,tileDistinction.PLAYER1,
                                                            tileDistinction.PLAYER2,tileDistinction.PLAYER3,
                                                            tileDistinction.PLAYER4,tileDistinction.SPECIAL):
                        pygame.draw.rect(screen, black, self.board[col][row].box, 2)
                
                # Add gray border around score tile for visible player(s)
                if self.board[col][row].mDistinct == tileDistinction.SPECIAL and \
                    self.board[col][row].title_color==white:
                    pygame.draw.rect(screen, player_red, self.board[col][row].box, 4)

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
        length = min(self.width, self.height)
        offset = max(self.width, self.height)
        rect_width, rect_height = length - (.02 * offset), length - (.08 * offset)  # Size of the rectangle
        cell_width = rect_width // self.cols
        cell_height = rect_height // self.rows
        for col in range(self.cols):
            for row in range(self.rows):
                cell_x = self.rect_x + col * cell_width + (length * .4)
                cell_y = self.rect_y + row * cell_height - (length * .15)
                self.board[col][row].updateTile((cell_x, cell_y), cell_width, cell_height, col , row)
    
    def updateTileColors(self):
        for col in range(self.cols):
            for row in range(self.rows):
                if configModule.optionalMatchOriginalColors:
                    if self.board[col][row].mDistinct == tileDistinction.HQ or self.board[col][row].mDistinct == tileDistinction.NORMAL:
                        match self.board[col][row].mTrivia:
                            case triviaType.RED:
                                self.board[col][row].mColor = match_red
                                self.board[col][row].mComplimentColor= darkRed
                            case triviaType.YELLOW:
                                self.board[col][row].mColor = match_yellow
                                self.board[col][row].mComplimentColor = darkYellow
                            case triviaType.BLUE:
                                self.board[col][row].mColor = match_blue
                                self.board[col][row].mComplimentColor = darkBlue
                            case triviaType.GREEN:
                                self.board[col][row].mColor = match_green
                                self.board[col][row].mComplimentColor = darkGreen
                    elif self.board[col][row].mDistinct == tileDistinction.CENTER:
                        self.board[row][col].mColor = match_white
                        self.board[row][col].mComplimentColor = base0
                else:
                    if self.board[col][row].mDistinct == tileDistinction.HQ:
                        match self.board[col][row].mTrivia:
                            case triviaType.RED:
                                self.board[col][row].mColor = HQ_red
                                self.board[col][row].mComplimentColor= HQ_dark_red
                            case triviaType.YELLOW:
                                self.board[col][row].mColor = HQ_yellow
                                self.board[col][row].mComplimentColor = HQ_dark_yellow
                            case triviaType.BLUE:
                                self.board[col][row].mColor = HQ_blue
                                self.board[col][row].mComplimentColor = HQ_dark_blue
                            case triviaType.GREEN:
                                self.board[col][row].mColor = HQ_green
                                self.board[col][row].mComplimentColor = HQ_dark_green
                    if self.board[col][row].mDistinct == tileDistinction.NORMAL:
                        match self.board[col][row].mTrivia:
                            case triviaType.RED:
                                self.board[col][row].mColor = red
                                self.board[col][row].mComplimentColor= darkRed
                            case triviaType.YELLOW:
                                self.board[col][row].mColor = yellow
                                self.board[col][row].mComplimentColor = darkYellow
                            case triviaType.BLUE:
                                self.board[col][row].mColor = blue
                                self.board[col][row].mComplimentColor = darkBlue
                            case triviaType.GREEN:
                                self.board[col][row].mColor = green
                                self.board[col][row].mComplimentColor = darkGreen
                    elif self.board[col][row].mDistinct == tileDistinction.CENTER:
                        self.board[row][col].mColor = magenta
                        self.board[row][col].mComplimentColor =violet

    def __init__(self, width=1280, height=720, cols=9, rows=9):
        self.width = width
        self.height = height
        self.cols = cols
        self.rows = rows
        self.board = [ [tile(triviaType.RED) for j in range(self.cols)] for i in range(self.rows)]
        self.create_board()
        if configModule.optionalStaticBoard == False:
            self.correctBoard()
        self.initializeBoard()
        self.updateTileColors()
        