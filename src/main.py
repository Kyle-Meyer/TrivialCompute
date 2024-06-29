import array
import math
import sys
import cairo
import pygame
from pygame.locals import *
sys.path.append('/path/to/application/app/folder')
import wrappers.rsvg as rsvg
import random
from tile import *
from colors import *
from board import cBoard
from pprint import pprint
from boundingBox import boundingBox
from player import player
from button import button
from menu import *

#flesh this out later
class mainMenu(object):
    run = True
    #move stuff like this to be global or wrap everything back into yet another object
    WIDTH = 1280
    HEIGHT = 720
    testButton = button((WIDTH // 2, HEIGHT // 2))
    testButton.button_text = "shadoobie"
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
class pygameMain(object):
    WIDTH = 1280
    HEIGHT = 720
    LENGTH = min(WIDTH, HEIGHT)
    OFFSET = max(WIDTH, HEIGHT)


    #globals are bad, avoid them when we can
    run = True
    moving = False
    color = green

    player = player()
    playBoard = cBoard(WIDTH, HEIGHT)

    testButton = button((10, 10))
    testButton2 = button((WIDTH // 2, HEIGHT // 2))
    testButton2.button_text = "shadoobie"
    testMenu = menu((250, 350), 400, 600) 
    testMenu.title_text = "Example menu"
    testMenu.addChildComponent(button(testMenu.ScreenCoords,  0, 0, "Shadoingle"))
    testMenu.addChildComponent(button(testMenu.ScreenCoords,  0, 0, "Shadoingle2"))
    testMenu.addChildComponent(button(testMenu.ScreenCoords,  0, 0, "Shadoingle2"))
    #testMenu.addChildComponent(button(testMenu.ScreenCoords,  0, 0, "Shadoingle2"))
    testMenu.addChildComponent(menu((250,250), 20, 20))
    #testMenu.offsetButtons(-70, 0)
    #for dice roll in the future
    diceRoll = 1
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Trivial Compute")
    #we could make the screen resizable, but I dont think this is the best way to do it
    #screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.RESIZABLE)

    #TODO Remove later
    #player_size = LENGTH // 16
    #player_size = 40
    #player = pygame.Rect((300, 250, player_size, player_size))
    #checkBox = pygame.Rect((300,250, player_size*4, player_size*4))
    #player = pygame.surface.

    bounding_box = pygame.Rect(300, 200, 200, 200)
    bounding_box2 = pygame.Rect(100, 200, 200, 200)
    clock = pygame.time.Clock()

    def debugButton(self):
        self.testButton.button_text = "this is a test"
        self.testButton.border_thickness = 0
        self.testButton.changeTextSize(20)
        self.testButton.button_text_color = base3
        self.testButton.draw_button(self.screen)

    def initializeBoard(self):
        
        rect_x, rect_y = self.screen.get_width()//4, self.screen.get_height()//4  # Position of the rectangle we always work in quadrants
        self.LENGTH = min(self.screen.get_width(), self.screen.get_height())
        self.OFFSET = max(self.screen.get_width(), self.screen.get_height())
        rect_width, rect_height = self.LENGTH - (.1 * self.OFFSET), self.LENGTH - (.1 * self.OFFSET)  # Size of the rectangle
        cols, rows = 9, 9  # Number of columns and rows in the grid
        cell_width = rect_width // cols
        cell_height = rect_height // rows
        for col in range(cols):
            for row in range(rows):
                cell_x = rect_x + col * cell_width + (self.LENGTH * .4)
                cell_y = rect_y + row * cell_height - (self.LENGTH * .15)
                self.playBoard.board[col][row].box = pygame.Rect(cell_x, cell_y, cell_width, cell_height)
                #pygame.draw.rect(screen, playBoard.board[col][row].mColor, playBoard.board[col][row].box, 1)

    #might come back to this later
    def resizeAll(self, inWidth, inHeight):
        # recalculate our offset
        off = min(inWidth, inHeight) // 2
        #re-adjust position
        print("Height DIFF: ", inHeight)
        print("Wdith DIFF: ", inWidth)
        #adjust the width and height of things
        self.player.x -= inWidth
        self.player.y -= inHeight
        #resize player
        self.player.width = min(self.screen.get_width(), self.screen.get_height()) // 16
        self.player.height = min(self.screen.get_width(), self.screen.get_height()) // 16
        for i in range(9):
            for j in range(9):
                #adjust size
                self.LENGTH = min(self.screen.get_width(), self.screen.get_height())
                self.OFFSET = max(self.screen.get_width(), self.screen.get_height())
                self.playBoard.board[i][j].box.width = ((self.LENGTH - (.1 * self.OFFSET)) // 9)
                self.playBoard.board[i][j].box.height = (self.LENGTH - (.1 * self.OFFSET)) // 9
                #adjust position
                self.playBoard.board[i][j].box.x -=inWidth
                self.playBoard.board[i][j].box.y -=inHeight
        print((self.LENGTH - (.1 * self.OFFSET)) // 9)

    #TODO move this draw over to board class
    def drawBoard(self):
        for col in range(9):
            for row in range(9):
                if self.playBoard.board[col][row].mDistinct == tileDistinction.SPECIAL:
                    pygame.draw.rect(self.screen, self.playBoard.board[col][row].mColor, self.playBoard.board[col][row].box, 4)
                else:
                    if self.playBoard.board[col][row].mDistinct != tileDistinction.NULL:
                        #TODO move this to the tile class
                        pygame.draw.rect(self.screen, self.playBoard.board[col][row].mComplimentColor, self.playBoard.board[col][row].box)
                        testRect = pygame.Rect(self.playBoard.board[col][row].box.x, self.playBoard.board[col][row].box.y, self.playBoard.board[col][row].box.width, self.playBoard.board[col][row].box.height-10)
                        pygame.draw.rect(self.screen, self.playBoard.board[col][row].mColor, testRect)
                        pygame.draw.rect(self.screen, self.playBoard.board[col][row].mComplimentColor, testRect, 3)
                        pygame.draw.rect(self.screen, base3, self.playBoard.board[col][row].box, 1)
                    else:
                        pygame.draw.rect(self.screen, self.playBoard.board[col][row].mColor, self.playBoard.board[col][row].box)

    def initiatePlayers(self):
        self.player = player(10, self.WIDTH // 2, self.HEIGHT // 2, blue)
        #set player relative to the coords of the board
        self.player.updateBoardPos(0, 0)
        self.player.setScreenCoords(self.playBoard.board[0][0].box.centerx, self.playBoard.board[0][0].box.centery)
        self.player.updateBox(self.playBoard.board[0][0].box.centerx, #x position
                              self.playBoard.board[0][0].box.centery, #y position
                              ((self.playBoard.board[0][0].box.size[0]) + (self.playBoard.board[0][0].box.size[0] * self.diceRoll)*2)) #size dependent on dice rolls

    def drawPlayers(self):
        return
    
    def handleCurrentPlayerMoves(self):
        neighbors = []
        self.player.getNeighbors(self.playBoard, self.player.currCordinate, self.diceRoll + 1, neighbors)
        #neighbors.remove(self.player.currCordinate)
        #print(neighbors)
        for i in range(len(neighbors)):
            #if this within our range
            if self.player.checkValidMove(self.playBoard.board[neighbors[i][0]][neighbors[i][1]]):
                #check if the player has moved beyond their starting square
                if self.player.currCordinate != neighbors[i]:
                    #make the call from here to spawn the end turn button
                    print("has changed")
                break
        #reset player position if its invalid
        else:
            self.player.circle_x = self.playBoard.board[0][0].box.centerx
            self.player.circle_y = self.playBoard.board[0][0].box.centery

    def calculateBoundingBox(self):
        self.playBoard.board[0][0].box.size[0]

    def mainMenuLoop(self):
        localRun = True
        while localRun:
            for event in pygame.event.get():
                if event.type == QUIT:
                    localRun= False
                if self.testButton2.isClicked(event):
                    localRun = False
            self.screen.fill((25, 28, 38))
            self.testButton2.draw_button(self.screen)  
            pygame.display.update()
            self.clock.tick(60) #60 fps

    def mainLoop(self):
        while self.run:
          
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.run= False
                
                #get the press hold event for the player
                self.handleCurrentPlayerMoves()
                #update the bounding box, this will move into the endTurn function coming with menus update
                
                self.player.checkIfHeld(event)
                self.player.clampPlayer(self.WIDTH, self.HEIGHT)
                self.testButton.isClicked(event)
                self.testMenu.listen_for_buttons(event)
                #this is getting wonky, and fast, so I'm going to leave this commented out and maybe come back around to it
                '''
                if event.type == pygame.VIDEORESIZE:
                    # addfunctionality to resize everything
                    print("resize grid and player")
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    print("Old WIdth: ", oldWidth, " event Widht: ", event.w)
                    print("old Height: ", oldHeight, " event height: ", event.h)
                    self.resizeAll(oldWidth - event.w, oldHeight - event.h)
            '''
            
            self.screen.fill((25, 28, 38))
            self.drawBoard()
            #self.debugButton()
            self.testMenu.drawMenu(self.screen)
            #draw calls
            pygame.draw.circle(self.screen, self.player.circle_color, (self.player.circle_x, self.player.circle_y), self.player.circle_radius)
            pygame.draw.circle(self.screen, base1, (self.player.circle_x, self.player.circle_y), self.player.circle_radius, 2)
            pygame.draw.rect(self.screen, base1, self.player.clampBox.box, 2)
            pygame.display.update()
            self.clock.tick(60) #60 fps

        pygame.quit()

def main(): 
    #rows = 10  # Number of rows in the board
    #cols = 10  # Number of columns in the board

    # Generate the board
    #game_board = create_board(rows, cols)

    # Print the generated board
    #print_board(game_board)
    # Example usage
    #n = 2  # Depth of recursion, generates a 3**3 x 3**3 grid
    #sierpinski_carpet = generate_sierpinski_carpet(n)
    #print_carpet(sierpinski_carpet)
    pygame.init()
    demo = pygameMain()
    #demo.mainMenuLoop()
    demo.initializeBoard()
    demo.initiatePlayers()
    demo.mainLoop()
    
if __name__=="__main__": 
    main() 