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

    # Show Player 1 name and score on the board
    # Note this is currently hardcoded for player 1
    playBoard.board[2][1].title_text = "Kyle"
    playBoard.board[2][2].title_color = white
    
    #the playground
    boundingDraw = False
    testParticle = particleManager(WIDTH, HEIGHT)
    testDice = dice((350, 450), 150, 100)
    testDice.diceMenu.changeTextSize(25)
    testDice.diceMenu.moveBox((testDice.diceMenu.rect.centerx, testDice.diceMenu.rect.centery -30))
    testDice.diceText.changeTextSize(30)
    testDice.diceText.moveBox((testDice.diceText.rect.centerx, testDice.diceText.rect.centery + 60))
    questionAnswerTextWidget = textWidget((350, 400), 100, 100, "")
    questionAnswerTextWidget.border_thickness = 0
    testButton = button((10, 10))
    testButton2 = button((WIDTH // 2, HEIGHT // 2))
    testButton2.button_text = "locked button"
    testButton2.lockOut = True
    testMenu = menu((250, 350), 400, 600) 
    testMenu.title_text = "Example menu"
    testMenu.addChildComponent(button(testMenu.ScreenCoords,  0, 0, "TestButton1"))
    testMenu.addChildComponent(button(testMenu.ScreenCoords,  0, 0, "Draw Bounding Box"))
    testMenu.addChildComponent(button(testMenu.ScreenCoords,  0, 0, "1. Roll dice"))
    testMenu.addChildComponent(button(testMenu.ScreenCoords,  0, 0, "2. Move Token"))
    testMenu.addChildComponent(button(testMenu.ScreenCoords,  0, 0, "3. Get Q and A"))
    testMenu.addChildComponent(button(testMenu.ScreenCoords,  0, 0, "4. Correct!"))
    testMenu.addChildComponent(testButton2)
    testMenu.addChildComponent(menu((250,250), 20, 20, "sub-menu example"))
    testMenu.addChildComponent(questionAnswerTextWidget)
    #for dice roll in the future
    diceRoll = 0
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
    
    # Convert token position to tile coordinates
    def screenPosToCoord(self): 
        leftEdgeOfTiles = int(self.WIDTH // 4 + 0.4 * self.LENGTH) 
        topEdgeOfTiles = int(self.HEIGHT // 4 - 0.15 * self.LENGTH) 
        playerXCoord = int((self.player.circle_x - leftEdgeOfTiles)//((self.LENGTH - (.1 * self.OFFSET))//9)) 
        playerYCoord = int((self.player.circle_y - topEdgeOfTiles)//((self.LENGTH - (.1 * self.OFFSET))//9)) 
        return(playerXCoord,playerYCoord) 
    
    # Locks in the player's move
    def advanceToken(self, position = (-1,-1)):
        if position != (-1,-1):
            self.testDice.diceValue=0
            self.testDice.diceText.title_text = str(self.testDice.diceValue)
            self.diceRoll=self.testDice.diceValue
            self.player.currentNeighbors.clear()
            self.player.updateBoardPos(self.playBoard.board[position[0]][position[1]], self.diceRoll)
            
    # Update the score for a player
    def updatePlayerScore(self, coord=(-1,-1)):
        if coord not in [(0,4), (4,0), (4,8), (8,4)]: return
        else:
            if coord == (4,0): cat = "c1"
            elif coord == (8,4): cat = "c2"
            elif coord == (4,8): cat = "c3"
            elif coord == (0,4): cat = "c4"
            if self.playBoard.board[coord[0]][coord[1]].mTrivia == triviaType.RED: self.player.playerScore[cat]="R"
            elif self.playBoard.board[coord[0]][coord[1]].mTrivia == triviaType.BLUE: self.player.playerScore[cat]="B"
            elif self.playBoard.board[coord[0]][coord[1]].mTrivia == triviaType.GREEN: self.player.playerScore[cat]="G"
            elif self.playBoard.board[coord[0]][coord[1]].mTrivia == triviaType.YELLOW: self.player.playerScore[cat]="Y"
            # Note this is currently hardcoded for player 1
            self.playBoard.board[2][2].title_text = str(self.player.playerScore["c1"])+ \
                        str(self.player.playerScore["c2"])+     \
                        str(self.player.playerScore["c3"])+     \
                        str(self.player.playerScore["c4"])
        return
    
    # Check for game winner
    def checkIfPlayerJustWon(self):
        if self.player.currCordinate == (4,4):
            if '_' in self.player.playerScore.values():
                return False
            else:
                return True
    
    # Crown the victor
    def crownVictor(self):
        self.playBoard.board[2][1].title_color = winner_green
        self.playBoard.board[2][2].mcolor = winner_green
                
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

    def __init__(self, databaseConnection):
        self.databaseConnection = databaseConnection    

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
                # Bounding Box Button
                if abs == 1:
                    if self.boundingDraw == True:
                        self.boundingDraw = False
                    else:
                        self.boundingDraw = True
                # Roll Dice Button
                elif abs == 2:
                    self.testDice.rollDice(self.screen)
                    self.player.hasRolled = True 
                # Move Token Button
                elif abs == 3:
                    currentTokenPosition = self.screenPosToCoord()
                    if currentTokenPosition in self.player.currentNeighbors and \
                        currentTokenPosition != self.player.currCordinate:
                        self.advanceToken(currentTokenPosition)
                    else:
                        self.player.updateBoardPos(self.playBoard.board[self.player.currCordinate[0]][self.player.currCordinate[1]], self.diceRoll)
                # Get Q&A Button
                elif abs == 4:
                    question, answer = self.databaseConnection.getRandomQuestionAndAnswer()
                    self.questionAnswerTextWidget.updateText(question + ' ' + answer) 
                # Correct Answer Button
                elif abs == 5:
                    if self.player.currCordinate in [(4,0),(8,4),(4,8),(0,4)]: 
                        self.updatePlayerScore(self.player.currCordinate)
                    elif self.player.currCordinate == (4,4):
                        if self.checkIfPlayerJustWon():
                            self.crownVictor

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
            # self.questionAnswerTextWidget.drawWidget(self.screen)
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

    
    demo = pygameMain(database)
    #demo.mainMenuLoop()
    demo.initiatePlayers()
    demo.mainLoop()
    #database.close()
    
if __name__=="__main__": 
    main() 