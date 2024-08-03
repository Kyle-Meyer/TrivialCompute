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
from startMenu import run_start_menu
from gameSetupMenu import runSetupMenu
from slidingMenu import slidingMenu
from slideBarWidget import slideBarWidget
from triviaMenu import triviaMenu
from timerClock import timerClock
from voteWidget import voteWidget
import json

import os
import copy

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
    def __init__(self, databaseConnection, setupInfo):
        self.databaseConnection = databaseConnection
        self.setupInfo = setupInfo

        # Initialize playerList using setupInfo
        self.playerList = []
        print(self.setupInfo)
        print(self.setupInfo['number_of_players'])
        for i in range(self.setupInfo['number_of_players']):
            color_switcher = {
                (255, 0, 0): player_red,
                (0, 0, 255): player_blue,
                (0, 255, 0): player_green,
                (255, 255, 0): player_yellow
            }
            self.playerList.append(player(11, self.WIDTH // 2, self.HEIGHT // 2,color_switcher.get(self.setupInfo['players'][i]['color'])))
            self.playerList[i].playerName = self.setupInfo['players'][i]['name']
            self.playerList[i].playerColor =color_switcher.get(self.setupInfo['players'][i]['color'])

        # Initialize playBoard attributes that depend on setupInfo
        self.playBoard = cBoard(self.WIDTH, self.HEIGHT)
        for i in range(self.setupInfo['number_of_players']):
            position_switcher = {
                0: (2, 1),
                1: (6, 1),
                2: (2, 5),
                3: (6, 5)
            }
            a, b = position_switcher.get(i)
            self.playerList[i].playerScorePosition = (a,b)
            self.playBoard.board[a][b].title_text = self.playerList[i].playerName #Larry
            self.playBoard.board[a][b+1].title_color = self.playerList[i].playerColor #White

    
    WIDTH = 1280
    HEIGHT = 720
    LENGTH = min(WIDTH, HEIGHT)
    OFFSET = max(WIDTH, HEIGHT)
    run = True
    moving = False
    color = green
   
    #TODO, change how player list will work across network
    #currPlayer = playerList[0]
    clientNumber = 0
    currState = 0
    drawDice = False
    
    #the playground
    boundingDraw = False
    testParticle = particleManager(WIDTH, HEIGHT)
    testDice = dice((300, 280), 80, 80)
    testDice.diceMenu.changeTextSize(0)
    testDice.diceMenu.moveBox((testDice.diceMenu.rect.centerx, testDice.diceMenu.rect.centery -30))
    testDice.diceText.moveBox((testDice.diceText.rect.centerx, testDice.diceText.rect.centery - 20))
    testDice.diceText.changeTextSize(30)
    testDice.diceText.moveBox((testDice.diceText.rect.centerx, testDice.diceText.rect.centery + 60))
    questionAnswerTextWidget = textWidget((350, 400), 100, 100, "")
    questionAnswerTextWidget.border_thickness = 0
    testButton = button((10, 10))
    testButton2 = button((WIDTH // 2, HEIGHT // 2))
    testButton2.button_text = "locked button"
    testButton2.lockOut = True
    testMenu = menu((200, 350), 300, 550) 
    testMenu.title_text = "Game Menu"
    
   
    #testMenu.addChildComponent(button(testMenu.ScreenCoords,  0, 0, "TestButton1"))
    #testMenu.addChildComponent(button(testMenu.ScreenCoords,  0, 0, "Draw Bounding Box"))
    testMenu.addChildComponent(button((150, 200),  180, 90, "1. Roll dice"))
    testMenu.addChildComponent(button((150, 300),  180, 90, "2. Move Token"))
    testMenu.addChildComponent(button((150, 400),  180, 90, "3. Save Game"))
    testMenu.addChildComponent(button((150, 500),  180, 90, "6. Settings"))
    testMenuButtons = {'Roll Dice':1, 'Move Token':2, 'Save Game':3}
    #TODO clean this up
    settingsMenu = slidingMenu((-1280, HEIGHT//2), 600, 400)
    trivMenu = triviaMenu((WIDTH//2, -720), 700, 600)
    gameSetupMenu = slidingMenu((-1280, HEIGHT//2), 600, 400)

    #slider = slideBarWidget((300, 200), 300, 100)
    #settingsMenu = slidingMenu((10, 300), 100, 100)
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

    def createTriviaMenu(self):
        self.trivMenu.menuDuration = 750
        self.trivMenu.fadeBox.alpha = 200
        self.trivMenu.addChildComponent(textWidget((640, 1060),  200, 200, "Question PlaceHolder"))
        self.trivMenu.addDictionary()
        self.trivMenu.switchActiveDictionary(1)
        self.trivMenu.addChildComponent(textWidget((640, 1060),  200, 200, "Answer PlaceHolder"))
        self.trivMenu.addChildComponent(button((500, 1300),  200, 70, "Correct!"))
        self.trivMenu.addChildComponent(button((800, 1300),  200, 70, "Incorrect!"))
        self.trivMenu.activeDictionary[childType.BUTTON][0].updateTextColor(green)
        self.trivMenu.activeDictionary[childType.BUTTON][1].updateTextColor(red)
        offset = 0
        tempList = copy.deepcopy(self.playerList)
        del tempList[self.clientNumber]
        #TODO turn this back on when we have server functionality
        '''for i in range(1, len(self.playerList)):
            self.trivMenu.addChildComponent(voteWidget((350, 1000 + offset), 30, 30))
            self.trivMenu.addChildComponent(textWidget((450, 990 + offset), 50, 50, str("Player: " + str(i))))
            self.trivMenu.activeDictionary[childType.TEXT][i].textCol = base01
            self.trivMenu.activeDictionary[childType.TEXT][i].changeTextSize(30)
            offset += 50'''
        self.trivMenu.switchActiveDictionary(0)
        
    def createSettingsMenu(self):
        self.settingsMenu.menuDuration = 750
        self.settingsMenu.fadeBox.alpha = 200
        #self.settingsMenu.addChildComponent(button((-640, 500),  100, 50, "Exit"))
        self.settingsMenu.addChildComponent(textWidget((-810, 260),  50, 50, "Match Colors: "))
        self.settingsMenu.addChildComponent(textWidget((-810, 310),  50, 50, "Static Board: "))
        self.settingsMenu.addChildComponent(textWidget((-810, 360),  50, 50, "3d Tiles: "))
        self.settingsMenu.addChildComponent(textWidget((-810, 410),  50, 50, "3d Players: "))
        self.settingsMenu.addChildComponent(textWidget((-540, 260),  50, 50, "Outline Tiles: "))
        self.settingsMenu.addChildComponent(textWidget((-540, 310),  50, 50, "Debug Mode: "))
        self.settingsMenu.addChildComponent(textWidget((-540, 360),  50, 50, "Fast Dice: "))
        self.settingsMenu.addChildComponent(textWidget((-540, 410),  50, 50, "Prune Neighbors: "))
        self.settingsMenu.addChildComponent(checkBoxWidget((-750, 260), 20, 20))
        self.settingsMenu.addChildComponent(checkBoxWidget((-750, 310), 20, 20))
        self.settingsMenu.addChildComponent(checkBoxWidget((-750, 360), 20, 20))
        self.settingsMenu.addChildComponent(checkBoxWidget((-750, 410), 20, 20))
        self.settingsMenu.addChildComponent(checkBoxWidget((-480, 260), 20, 20))
        self.settingsMenu.addChildComponent(checkBoxWidget((-480, 310), 20, 20))
        self.settingsMenu.addChildComponent(checkBoxWidget((-480, 360), 20, 20))
        self.settingsMenu.addChildComponent(checkBoxWidget((-480, 410), 20, 20))
        #settingsMenu.addChildComponent(slideBarWidget((-1280, HEIGHT//2), 200, 200))
        for entry in self.settingsMenu.child_Dictionary[childType.TEXT]:
            entry.changeTextSize(20)
        self.settingsMenu.title_text = "Settings"
        self.settingsMenu.bindCheckBoxes()
        #add another menu state
        self.settingsMenu.addDictionary()
        self.settingsMenu.switchActiveDictionary(1)
        self.settingsMenu.switchActiveDictionary(0)

   #TODO encapsulate this so that it can draw mutliple players
    def initializePlayersForNewGame(self):
        #localColorList = [player_red, player_blue, player_green, player_yellow]
        count = 0
        offset = 17
        for play in self.playerList:
            #play = player(11, self.WIDTH // 2, self.HEIGHT // 2, localColorList[count])
            play.updateBoardPos(self.playBoard.board[4][4], self.diceRoll)
            self.playerList[count] = play
            match count:
                case 0:
                    self.playerList[count].tileOffset=(-offset, 0)
                    self.playerList[count].circle_x += -offset
                case 1:
                    self.playerList[count].tileOffset=(0, -offset)
                    self.playerList[count].circle_y += -offset
                case 2:
                    self.playerList[count].tileOffset=(offset, 0)
                    self.playerList[count].circle_x += offset
                case 3:
                    self.playerList[count].tileOffset=(0, offset)
                    self.playerList[count].circle_y += offset
            count += 1
        #TODO change this so that it sets respective player to what the server dictates the client should be
        self.currPlayer = self.playerList[0]
        #set player relative to the coords of the board
        #this takes in a tile object from the board
        #self.currPlayer.updateBoardPos(self.playBoard.board[4][4], self.diceRoll)

    def initializePlayersForRestoreGame(self, convertedPlayerPositionsTuple):
        localColorList = [player_red, player_blue, player_green, player_yellow]
        count = 0
        offset = 17

        for play in self.playerList:
            play = player(11, self.WIDTH // 2, self.HEIGHT // 2, localColorList[count])
            
            (playerName, (x, y)) = convertedPlayerPositionsTuple[count]
            play.updateBoardPos(self.playBoard.board[x][y], self.diceRoll)
            
            self.playerList[count] = play
            match count:
                case 0:
                    self.playerList[count].tileOffset=(-offset, 0)
                    self.playerList[count].circle_x += -offset
                case 1:
                    self.playerList[count].tileOffset=(0, -offset)
                    self.playerList[count].circle_y += -offset
                case 2:
                    self.playerList[count].tileOffset=(offset, 0)
                    self.playerList[count].circle_x += offset
                case 3:
                    self.playerList[count].tileOffset=(0, offset)
                    self.playerList[count].circle_y += offset
            count += 1
        #TODO change this so that it sets respective player to what the server dictates the client should be
        self.currPlayer = self.playerList[0]

    def drawPlayers(self):
        for play in self.playerList:
            play.drawPlayer(self.screen)
            if play == self.currPlayer:
                diff = play.circle_radius - play.circle_inner_radius
                pygame.draw.circle(self.screen, base3, (play.circle_x, play.circle_y), play.circle_radius+diff, diff*2)
    
    # Convert token position to tile coordinates
    #TODO redo all of this, its bad
    def screenPosToCoord(self): 
        leftEdgeOfTiles = int(140 + 0.4 * self.LENGTH) 
        topEdgeOfTiles = int(130 - 0.15 * self.LENGTH) 
        playerXCoord = int((self.currPlayer.circle_x - leftEdgeOfTiles)//((self.LENGTH - (.02 * self.OFFSET))//9)) 
        playerYCoord = int((self.currPlayer.circle_y - topEdgeOfTiles)//((self.LENGTH - (.08 * self.OFFSET))//9))
        return(playerXCoord,playerYCoord) 
    
    # Locks in the player's move
    def advanceToken(self, position = (-1,-1)):
        if position != (-1,-1):
            self.testDice.diceValue=0
            self.testDice.diceText.title_text = str(self.testDice.diceValue)
            self.diceRoll=self.testDice.diceValue
            self.currPlayer.currentNeighbors.clear()
            self.currPlayer.updateBoardPos(self.playBoard.board[position[0]][position[1]], self.diceRoll)
            self.currPlayer.circle_x += self.currPlayer.tileOffset[0]
            self.currPlayer.circle_y += self.currPlayer.tileOffset[1]
            
    # Update the score for a player
    def updatePlayerScore(self, coord=(-1,-1)):
        if coord not in [(0,4), (4,0), (4,8), (8,4)]: return
        else:
            if coord == (4,0): cat = "c1"
            elif coord == (8,4): cat = "c2"
            elif coord == (4,8): cat = "c3"
            elif coord == (0,4): cat = "c4"
            if self.playBoard.board[coord[0]][coord[1]].mTrivia == triviaType.RED: self.currPlayer.playerScore[cat]="R"
            elif self.playBoard.board[coord[0]][coord[1]].mTrivia == triviaType.BLUE: self.currPlayer.playerScore[cat]="B"
            elif self.playBoard.board[coord[0]][coord[1]].mTrivia == triviaType.GREEN: self.currPlayer.playerScore[cat]="G"
            elif self.playBoard.board[coord[0]][coord[1]].mTrivia == triviaType.YELLOW: self.currPlayer.playerScore[cat]="Y"
            self.playBoard.board[self.currPlayer.playerScorePosition[0]][self.currPlayer.playerScorePosition[1]+1].title_text = str(self.currPlayer.playerScore["c1"])+ \
                        str(self.currPlayer.playerScore["c2"])+     \
                        str(self.currPlayer.playerScore["c3"])+     \
                        str(self.currPlayer.playerScore["c4"])
        return
    
    # Check for game winner
    def checkIfPlayerJustWon(self):
        if self.currPlayer.currCoordinate == (4,4):
            if '_' in self.currPlayer.playerScore.values():
                return False
            else:
                return True
    
    #def spawnServer(self):


    # Crown the victor
    def crownVictor(self):

        self.playBoard.board[self.currPlayer.playerScorePosition[0]][self.currPlayer.playerScorePosition[1]].title_color = winner_green
        self.playBoard.board[self.currPlayer.playerScorePosition[0]][self.currPlayer.playerScorePosition[1]+1].mColor = winner_green
                
    def handleCurrentPlayerMoves(self):
        self.currPlayer.currentNeighbors.clear()
        neighbors = self.currPlayer.currentNeighbors
        #TODO prune non max distance neighbors for a more traditional trivial pursuit experience
        #print(self.currPlayer.currCoordinate)
        oldCoord = self.currPlayer.currCoordinate
        self.currPlayer.getNeighbors(self.playBoard, self.currPlayer.currCoordinate, self.diceRoll + 1, neighbors)
        if configModule.optionalPruneNeighbors:
            self.currPlayer.pruneNeighbors(self.diceRoll)
        for i in range(len(neighbors)):
            #if this within our range
            if self.currPlayer.checkValidMove(self.playBoard.board[neighbors[i][0]][neighbors[i][1]]):
                #check if the player has moved beyond their starting square
                if self.currPlayer.currCoordinate != neighbors[i]:
                    #TODO make the call from here to spawn the end turn button
                    self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Move Token']-1].lockOut = False
                    #self.currPlayer.currCoordinate = neighbors[i]
                break
        #reset player position if its invalid
        else:
            self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Move Token']-1].lockOut = True
            #self.currPlayer.currCoordinate = oldCoord

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
        question, answer = '', ''
        hasPulled = False
        while self.run:
            #event chain
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.run= False 
                #listen for board redraw
                shouldRedraw = configModule.optionalMatchOriginalColors              
                self.currPlayer.checkIfHeld(event)              
                self.testButton.isClicked(event)
                abs = self.testMenu.listen_for_buttons(event)
                rbs = self.settingsMenu.listen_for_checkBox(event)
                dbs = self.settingsMenu.listen_for_buttons(event)
                mbs = self.trivMenu.listen_for_buttons(event)
                #start the clock
                if self.trivMenu.triviaClock.startCounting == True:
                    self.trivMenu.triviaClock.countTime(event)
                if self.trivMenu.triviaClock.counter <= 0:
                    self.trivMenu.triviaClock.startCounting = False
                    self.trivMenu.triviaClock.shouldDraw = False
                    self.trivMenu.slideIn((self.WIDTH//2, self.HEIGHT//2))
                    print("RESET!")
                    self.trivMenu.resetTimer()
                    self.clientNumber +=1
                    if self.clientNumber >= 4:
                        self.clientNumber = 0
                    self.currPlayer = self.playerList[self.clientNumber]
                    # question = ''
                    # answer = ''
                    # hasPulled = False
                    self.currState = 0
                    
                #self.slider.listen(event)
                #BUTTON CALLBACK
                # Roll Dice Button
                if abs == self.testMenuButtons['Roll Dice']-1 and self.currPlayer.hasRolled == False:
                    self.testDice.rollDice(self.screen)
                    self.currState = 1 #TODO change this to send to server
                # Move Token Button
                elif abs == self.testMenuButtons['Move Token']-1:
                    print("WHAT THE FUCK")
                    self.currState = 2
                elif abs == self.testMenuButtons['Save Game']-1:
                    print('Save Game')
                    self.databaseConnection.saveCurrentGameState(self.playerList, self.currPlayer, [])
                if abs == 3 or dbs == -3:
                    self.settingsMenu.slideIn((self.WIDTH//2, self.HEIGHT//2))
                    self.testMenu.lockOut = not self.testMenu.lockOut
                elif abs == 1:
                    self.currState == 3
                    #self.trivMenu.triviaClock.startCounting = True
                    
                if shouldRedraw != configModule.optionalMatchOriginalColors:
                    #self.playBoard.create_board()
                    self.playBoard.updateTileColors()
                    self.currPlayer.updateColor()
                if mbs == -3:
                    #change the trivia button to accurately reflect what stage you are in
                    if self.currState < 3:
                        self.currState = 3
                    else:
                        self.currState = 4
                elif mbs >= 0:
                    self.currState = 5
                    #check if correct
                    if mbs == 0:
                        print("correct clicked")
                        if self.currPlayer.currCoordinate in [(4,0),(8,4),(4,8),(0,4)]: 
                            self.updatePlayerScore(self.currPlayer.currCoordinate)
                        elif self.currPlayer.currCoordinate == (4,4):
                            if self.checkIfPlayerJustWon():
                                self.crownVictor()
                    else:
                        self.clientNumber +=1
                        if self.clientNumber >= 4:
                            self.clientNumber = 0
                        self.currPlayer = self.playerList[self.clientNumber]
            #game state logic
            if self.currState == 0:
                self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Roll Dice']-1].lockOut=False
                self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Move Token']-1].lockOut=True
                hasPulled = False
                if self.trivMenu.away == True and self.trivMenu.activeIndex == 1:
                    for ent in self.trivMenu.activeDictionary[childType.VOTE]:
                        ent.voteSubmitted = False
                    self.trivMenu.switchActiveDictionary(0)
                self.trivMenu.triviaClock.startCounting = False
                self.trivMenu.triviaClock.shouldDraw = False
                
                
            if self.currState == 1:
                self.questionAnswerTextWidget.updateText('')
                self.trivMenu.activeDictionary[childType.TEXT][0].updateText(question)
                self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Roll Dice']-1].lockOut = True
                self.currPlayer.hasRolled = True 
                self.drawDice = True

            elif self.currState == 2:
                currentTokenPosition = self.screenPosToCoord()
                self.trivMenu.startButton.button_text = "Get Question"
                if currentTokenPosition in self.currPlayer.currentNeighbors and \
                    currentTokenPosition != self.currPlayer.currCoordinate:
                    self.advanceToken(currentTokenPosition)
                    self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Move Token']-1].lockOut = True
                    self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Roll Dice']-1].lockOut = True
                    
                    self.trivMenu.slideIn((self.WIDTH//2, self.HEIGHT//2))
                    self.drawDice = False

            elif self.currState == 3:
                #self.trivMenu.currState += 1
                self.trivMenu.triviaClock.shouldDraw = True
                self.trivMenu.triviaClock.startCounting = True

                if not hasPulled:
                    print("HAS NOT PULLED")
                    categories = self.setupInfo['categories']
                    category_names = []
                    if len(categories) < 4 or categories == {}:
                        category_names = ['Astronomy', 'Biology', 'Chemistry', 'Geology'] # Default categories
                    else:
                        for catRec in categories:
                            category_names.append(catRec['name'])
                    question, answer = self.databaseConnection.getQuestionAndAnswerByCategories(category_names)
                    self.trivMenu.activeDictionary[childType.TEXT][0].updateText(question)
                    hasPulled = True

                # self.trivMenu.haltWidgetDraw = True
                self.trivMenu.startButton.button_text = "Reveal Answer"
            elif self.currState == 4:
                self.trivMenu.triviaClock.shouldDraw = False
                self.trivMenu.triviaClock.startCounting = False
                if self.trivMenu.away == False and self.trivMenu.activeIndex == 0:
                    self.trivMenu.switchActiveDictionary(1)
                self.trivMenu.activeDictionary[childType.TEXT][0].updateText(answer)
                self.trivMenu.startButton.lockOut = True
            elif self.currState == 5:
                #self.trivMenu.canVote = True TURN THIS BACK ON FOR SERVER STUFF
                for ent in self.trivMenu.activeDictionary[childType.VOTE]:
                    ent.voteSubmitted = True
                self.trivMenu.slideIn((self.WIDTH//2, self.HEIGHT//2))
                self.trivMenu.resetTimer()
                question = ''
                answer = ''
                self.currState = 0

            if not self.testDice.rolling and self.currPlayer.hasRolled:
                self.diceRoll = self.testDice.diceValue
                self.currPlayer.updateBoxByDice(self.diceRoll, self.playBoard.board[0][0].box.size[0])
            
            
            #get the press hold event for the player
            self.currPlayer.clampPlayer(self.WIDTH, self.HEIGHT)
            self.handleCurrentPlayerMoves()

            #draw calls
            self.screen.fill((25, 28, 38))
            self.testParticle.drawParticles(self.screen)
            self.playBoard.drawBoard(self.screen, self.currPlayer.currentNeighbors)
            #self.debugButton()

        
            # self.questionAnswerTextWidget.drawWidget(self.screen)
            #self.testDice.drawDice(self.screen, self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Roll Dice']-1].lockOut)

            self.drawPlayers()
            self.testMenu.drawMenu(self.screen, base3)
            
            self.testDice.drawDice(self.screen, self.drawDice)
            self.settingsMenu.drawMenu(self.screen)
            self.trivMenu.drawMenu(self.screen)
            #self.slider.draw(self.screen)
            #bounding box draw
            if self.boundingDraw:
                pygame.draw.rect(self.screen, debug_red, self.currPlayer.clampBox.box, 2)
            pygame.display.update()
            self.clock.tick(60) #60 fps

        pygame.quit()

def main(): 
    pygame.init()
    selected_menu_action = run_start_menu()

    if selected_menu_action == "start":
        database = databaseConnection(dbname='trivialCompute', user='postgres', password='postgres')
        setupInfo = runSetupMenu(database)
        #print(setupInfo)
        demo = pygameMain(database, setupInfo)
        #demo.createGameSetupMenu(database)
        #demo.mainMenuLoop()
        demo.createSettingsMenu()
        demo.createTriviaMenu()
        demo.initializePlayersForNewGame()
        demo.mainLoop()
        #database.close()
    elif selected_menu_action == "restore":
        database = databaseConnection(dbname='trivialCompute', user='postgres', password='postgres')
        demo = pygameMain(database)
        #demo.mainMenuLoop()
        demo.createSettingsMenu()
        demo.createTriviaMenu()

        playerPostionsOfLastSavedGameFromDB = database.getPlayerPositionsOfLastSavedGame()

        if playerPostionsOfLastSavedGameFromDB is None:
            print("No saved game state found.")
            demo.initializePlayersForNewGame()
        else:
            print("Previous game state found.")
            playerPositionsDictionary = playerPostionsOfLastSavedGameFromDB[0]
            convertedPlayerPositionsTuple = tuple((key, tuple(value)) for key, value in playerPositionsDictionary.items())
            demo.initializePlayersForRestoreGame(convertedPlayerPositionsTuple)

        demo.mainLoop()
        #database.close()
    else:
        pygame.quit()

if __name__=="__main__": 
    main() 