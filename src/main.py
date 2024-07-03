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
from textWidget import textWidget
from dice import dice
from particleMgr import particleManager
from databaseConnection import databaseConnection

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
    run = True
    moving = False
    color = green
    playBoard = cBoard(WIDTH, HEIGHT)
    player = player()
    
    #the playground
    boundingDraw = True
    testParticle = particleManager(WIDTH, HEIGHT)
    testDice = dice((350, 450), 150, 100)
    testDice.diceMenu.changeTextSize(25)
    testDice.diceMenu.moveBox((testDice.diceMenu.rect.centerx, testDice.diceMenu.rect.centery -30))
    testDice.diceText.changeTextSize(30)
    testDice.diceText.moveBox((testDice.diceText.rect.centerx, testDice.diceText.rect.centery + 60))
    testWidget = textWidget((350, 400), 100, 100, "Text Widget")
    testWidget.border_thickness = 0
    testButton = button((10, 10))
    testButton2 = button((WIDTH // 2, HEIGHT // 2))
    testButton2.button_text = "locked button"
    testButton2.lockOut = True
    testMenu = menu((250, 350), 400, 600) 
    testMenu.title_text = "Example menu"
    testMenu.addChildComponent(button(testMenu.ScreenCoords,  0, 0, "Test Button1"))
    testMenu.addChildComponent(button(testMenu.ScreenCoords,  0, 0, "Draw Bounding Box"))
    testMenu.addChildComponent(button(testMenu.ScreenCoords,  0, 0, "Roll dice"))
    testMenu.addChildComponent(testButton2)
    testMenu.addChildComponent(menu((250,250), 20, 20, "sub-menu example"))
    testMenu.addChildComponent(testWidget)
    #for dice roll in the future
    diceRoll = 3
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Trivial Compute")

    bounding_box = pygame.Rect(300, 200, 200, 200)
    bounding_box2 = pygame.Rect(100, 200, 200, 200)
    clock = pygame.time.Clock()

    def debugButton(self):
        self.testButton.button_text = "this is a test"
        self.testButton.border_thickness = 0
        self.testButton.changeTextSize(20)
        self.testButton.button_text_color = base3
        self.testButton.draw_button(self.screen)
        
   #TODO encapsulate this so that it can draw mutliple players
    def initiatePlayers(self):
        self.player = player(10, self.WIDTH // 2, self.HEIGHT // 2, player_blue)
        #set player relative to the coords of the board
        #TODO collpase this all into one function to make it easier
        #this takes in a tile object from the board
        self.player.updateBoardPos(self.playBoard.board[4][4], self.diceRoll)

    def drawPlayers(self):
        return
    
    def handleCurrentPlayerMoves(self):
        self.player.currentNeighbors.clear()
        neighbors = self.player.currentNeighbors
        #TODO prune non max distance neighbors for a more traditional trivial pursuit experience
        #print(self.player.currCordinate)
        self.player.getNeighbors(self.playBoard, self.player.currCordinate, self.diceRoll + 1, neighbors)
        for i in range(len(neighbors)):
            #if this within our range
            if self.player.checkValidMove(self.playBoard.board[neighbors[i][0]][neighbors[i][1]]):
                #check if the player has moved beyond their starting square
                if self.player.currCordinate != neighbors[i]:
                    #TODO make the call from here to spawn the end turn button
                    return
                    print("has changed")
                break
        #reset player position if its invalid
        else:
            return
            print("bad move")

    def calculateBoundingBox(self):
        self.playBoard.board[0][0].box.size[0]

    #TODO implement this later
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

    #SETTING UP INTERACTIVTY
    def mainLoop(self):
        while self.run:
            #event chain
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.run= False               
                self.player.checkIfHeld(event)              
                self.testButton.isClicked(event)
                abs = self.testMenu.listen_for_buttons(event)
                #BUTTON CALLBACK
                if abs == 2:
                    self.testDice.rollDice(self.screen)
                    self.player.hasRolled = True
                elif abs == 1:
                    if self.boundingDraw == True:
                        self.boundingDraw = False
                    else:
                        self.boundingDraw = True

            if not self.testDice.rolling and self.player.hasRolled:
                self.diceRoll = self.testDice.diceValue
                self.player.updateBoxByDice(self.diceRoll, self.playBoard.board[0][0].box.size[0])
            #get the press hold event for the player
            self.player.clampPlayer(self.WIDTH, self.HEIGHT)
            self.handleCurrentPlayerMoves()

            #draw calls
            self.screen.fill((25, 28, 38))
            self.testParticle.drawParticles(self.screen)
            self.playBoard.drawBoard(self.screen, self.player.currentNeighbors)
            #self.debugButton()
            self.testMenu.drawMenu(self.screen)
            self.testWidget.drawWidget(self.screen)
            self.testDice.drawDice(self.screen)
            self.player.drawPlayer(self.screen)
            #bounding box draw
            if self.boundingDraw:
                pygame.draw.rect(self.screen, debug_red, self.player.clampBox.box, 2)
            pygame.display.update()
            self.clock.tick(60) #60 fps

        pygame.quit()

def main(): 
    #tests db connection by retrieving a question/answer of a certain category
    database = databaseConnection(dbname='trivialCompute', user='postgres', password='postgres')
    # question, answer = database.getQuestionAndAnswerByCategory('Chemistry')
    # print(f"test retrieving question from db: {question}")
    # print(f"test retrieving answer from db: {answer}")
    pygame.init()

    #MAIN MENU
    #TWO BUTTONS

    
    demo = pygameMain()
    #demo.mainMenuLoop()
    demo.initiatePlayers()
    demo.mainLoop()
    #database.close()
    
if __name__=="__main__": 
    main() 