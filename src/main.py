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
from playerOrderMenu import run_order_menu
from slidingMenu import slidingMenu
from slideBarWidget import slideBarWidget
from triviaMenu import triviaMenu
from timerClock import timerClock
from voteWidget import voteWidget
import json
from network.connector import connector
from network.networkObjs import *
from legend import categoryLegend
from scoreboard import scoreboard
from playerTracker import playerTracker
from gameOverScreen import displayGameOver

import os
import subprocess
import copy
from _thread import *
import signal
import psutil
import ast

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

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
    def __init__(self, setupInfo, databaseConnection, currPlayerIndex):

        ####MEMBER VARIABLES
        self.databaseConnection = databaseConnection
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.LENGTH = min(self.WIDTH, self.HEIGHT)
        self.OFFSET = max(self.WIDTH, self.HEIGHT)
        self.run = True
        self.moving = False
        self.color = green
        self.clientNumber = 0
        self.controllingPlayer = 0
        self.currState = 0
        self.drawDice = False
        self.boundingDraw = False
        self.clientPlayer = 0
        self.testParticle = particleManager(self.WIDTH, self.HEIGHT)
        self.testDice = dice((300, 280), 80, 80)
        self.testDice.diceMenu.changeTextSize(0)
        self.testDice.diceMenu.moveBox((self.testDice.diceMenu.rect.centerx, self.testDice.diceMenu.rect.centery -30))
        self.testDice.diceText.moveBox((self.testDice.diceText.rect.centerx, self.testDice.diceText.rect.centery - 20))
        self.testDice.diceText.changeTextSize(30)
        self.testDice.diceText.moveBox((self.testDice.diceText.rect.centerx, self.testDice.diceText.rect.centery + 60))
        self.playerTracker = playerTracker((200,150),300,50)
        self.questionAnswerTextWidget = textWidget((350, 400), 100, 100, "")
        self.questionAnswerTextWidget.border_thickness = 0
        self.testButton = button((10, 10))
        self.testButton2 = button((self.WIDTH // 2, self.HEIGHT // 2))
        self.testButton2.button_text = "locked button"
        self.testButton2.lockOut = True
        self.testMenu = menu((200, 350), 300, 550) 
        self.testMenu.title_text = "Game Menu"
        self.testMenu.addChildComponent(button((150, 250),  180, 90, "1. Roll dice"))
        self.testMenu.addChildComponent(button((150, 350),  180, 90, "2. Move Token"))
        self.testMenu.addChildComponent(button((150, 450),  180, 90, "3. Save Game"))
        self.testMenu.addChildComponent(button((150, 550),  180, 90, "6. Settings"))
        self.testMenuButtons = {'Roll Dice':1, 'Move Token':2, 'Save Game':3}
        self.settingsMenu = slidingMenu((-1280, self.HEIGHT//2), 600, 400)
        self.trivMenu = triviaMenu((self.WIDTH//2, -720), 700, 600)
        self.gameSetupMenu = slidingMenu((-1280, self.HEIGHT//2), 600, 400)
        self.diceRoll = 0
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        

        pygame.display.set_caption("Trivial Compute")
        inData = None
        if configModule.online:
            self.n = connector("localhost", 5555)
        else:
            self.n = None

        if isinstance(setupInfo, str) and setupInfo == "join":
            inData = self.n.send(joinObject(0))
            self.setupInfo = inData.initDictionary
            print("PASSED IN JOIN INFO ", self.setupInfo)
        else:
            self.setupInfo = setupInfo
        self.bounding_box = pygame.Rect(300, 200, 200, 200)
        self.bounding_box2 = pygame.Rect(100, 200, 200, 200)
        self.clock = pygame.time.Clock()
        self.legend = categoryLegend(font_size=20, screen_width=self.WIDTH, screen_height=self.HEIGHT)
        self.clientNumber = currPlayerIndex
        self.scoreboards = []
        # Initialize playerList using setupInfo
        self.playerList = []
        #TODO, change how player list will work across network
        self.currPlayer = None
        for i in range(self.setupInfo['number_of_players']):
            self.playerList.append(player(11, self.WIDTH // 2, self.HEIGHT // 2,self.setupInfo['players'][i]['color']))
            self.playerList[i].playerName = self.setupInfo['players'][i]['name']
            self.playerList[i].playerColor = self.setupInfo['players'][i]['color']
            if self.setupInfo['players'][i]['color'] == match_yellow:
                self.playerList[i].recolor(match_yellow, darkYellow, white)
            elif self.setupInfo['players'][i]['color'] == match_blue:
                self.playerList[i].recolor(match_blue, darkBlue, white)
            elif self.setupInfo['players'][i]['color'] ==  match_red:
                self.playerList[i].recolor(match_red, darkRed, white)
            elif self.setupInfo['players'][i]['color'] ==  match_green:
                self.playerList[i].recolor(match_green, darkGreen, white)

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

        self.tileColorMapping =  {
            triviaType.RED: match_red,
            triviaType.YELLOW: match_yellow,
            triviaType.BLUE: match_blue,
            triviaType.GREEN: match_green
        }

    def debugButton(self):
        self.testButton.button_text = "this is a test"
        self.testButton.border_thickness = 0
        self.testButton.changeTextSize(20)
        self.testButton.button_text_color = base3
        self.testButton.draw_button(self.screen)

    def createTriviaMenu(self):
        self.trivMenu.menuDuration = 750
        self.trivMenu.fadeBox.alpha = 200
        self.trivMenu.addChildComponent(textWidget((640, 980),  400, 200, "Question PlaceHolder"))
        self.trivMenu.addDictionary()
        self.trivMenu.switchActiveDictionary(1)
        self.trivMenu.addChildComponent(textWidget((640, 980),  400, 200, "Answer PlaceHolder"))
        offset = 0
        tempList = copy.deepcopy(self.playerList)
        if configModule.online:
            '''del tempList[self.clientNumber]
            count = 0'''
            #TODO turn this back on when we have server functionality
            for i in range(1, len(tempList)+1):
                self.trivMenu.addChildComponent(voteWidget((350, 1000 + offset), 30, 30, self.clientNumber))
                self.trivMenu.addChildComponent(textWidget((450, 990 + offset), 50, 50, str(tempList[i-1].playerName)))
                self.trivMenu.activeDictionary[childType.TEXT][i].textCol = base01
                self.trivMenu.activeDictionary[childType.TEXT][i].changeTextSize(30)
                offset += 50
        
        self.trivMenu.addChildComponent(button((500, 1300),  200, 70, "Correct!"))
        self.trivMenu.addChildComponent(button((800, 1300),  200, 70, "Incorrect!"))
        self.trivMenu.activeDictionary[childType.BUTTON][0].updateTextColor(green)
        self.trivMenu.activeDictionary[childType.BUTTON][1].updateTextColor(red)
            
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

    def categorySelectionScreen(self, categories):
        # Screen settings
        screen_width = 1280
        screen_height = 720
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Select a Category")

        # Fonts
        font = pygame.font.Font(None, 50)

        # Button setup
        button_width = 300
        button_height = 75
        button_padding = 20
        button_x = (screen_width - button_width) // 2
        buttons = []

        # Prepare buttons with category names and colors
        for i, category in enumerate(categories):
            category_name = category['name']
            color = category['color']
            button_y = 100 + i * (button_height + button_padding)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            buttons.append((button_rect, category_name, color))

        # Main loop
        selecting = True
        selected_category = None

        while selecting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button_rect, category_name, color in buttons:
                            if button_rect.collidepoint(event.pos):
                                selected_category = category_name
                                selecting = False
                                break

            screen.fill(pygame.Color('black'))

            # Draw buttons
            for button_rect, category_name, color in buttons:
                pygame.draw.rect(screen, color, button_rect)
                text_surf = font.render(category_name, True, pygame.Color('black'))
                text_rect = text_surf.get_rect(center=button_rect.center)
                screen.blit(text_surf, text_rect)

            pygame.display.flip()

        return selected_category


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
        print("should be setting")
        self.currPlayer = self.playerList[self.clientNumber]

    def initializePlayersForRestoreGame(self, convertedPlayerPositionsTuple):
        # localColorList = [player_red, player_blue, player_green, player_yellow]
        count = 0
        offset = 17

        for play in self.playerList:
            # play = player(11, self.WIDTH // 2, self.HEIGHT // 2, localColorList[count])
            
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
        self.currPlayer = self.playerList[self.clientNumber]

    def restorePlayerScores(self, savedPlayerScores):
        for i in range(len(self.playerList)):
            self.playerList[i].playerScore = savedPlayerScores[i]

    def restorePlayerReportCards(self, savedPlayerReportCards):
        for i in range(len(self.playerList)):
            self.playerList[i].playerReportCard = savedPlayerReportCards[i]       

    def initializeScoreboards(self, playerList):
        rect_width, rect_height = self.LENGTH - (.02 * self.OFFSET), self.LENGTH - (.08 * self.OFFSET)
        cell_width = rect_width // self.playBoard.cols
        cell_height = rect_height // self.playBoard.rows
        scoreBoxWidth = 1.5 * cell_width
        scoreBoxHeight = 1.5 * cell_height

        for play in playerList:
            x_pos, y_pos = self.coordToScreenPos([(play.playerScorePosition[0]), (play.playerScorePosition[1]+1)])
            x_pos, y_pos = (x_pos - 0.25 * cell_width, y_pos - 0.25 * cell_height)
            self.scoreboards.append(scoreboard(play.playerName, play.circle_color, x_pos, y_pos, scoreBoxWidth, scoreBoxHeight))
            
    def drawPlayers(self):
        count = 0
        for play in self.playerList:
            play.drawPlayer(self.screen)
            #print(count, ": \n COLOR: ", play.circle_color, " \n INNER COLOR: ", play.circle_shadow_color, " \n HIGHLIGHT: ", play.circle_highlight_color)
            count += 1
            if play == self.currPlayer:
                diff = play.circle_radius - play.circle_inner_radius
                pygame.draw.circle(self.screen, base3, (play.circle_x, play.circle_y), play.circle_radius+diff, diff*2)
    
    def drawScoreboards(self):
        for i in range(len(self.scoreboards)):
            self.scoreboards[i].drawScoreboard(self.screen, self.playerList[i].playerScore)

    def drawPlayerTurn(self):
        self.playerTracker.updatePlayerTracker(self.screen, self.currPlayer.playerName, self.currPlayer.circle_color)       

    # Convert screen position to tile coordinates
    #TODO redo all of this, its bad
    def screenPosToCoord(self): 
        leftEdgeOfTiles = int(self.playBoard.rect_x + 0.4 * self.LENGTH) 
        topEdgeOfTiles = int(self.playBoard.rect_y - 0.15 * self.LENGTH) 
        tileXCoord = int((self.currPlayer.circle_x - leftEdgeOfTiles)//((self.LENGTH - (.02 * self.OFFSET))//self.playBoard.cols)) 
        tileYCoord = int((self.currPlayer.circle_y - topEdgeOfTiles)//((self.LENGTH - (.08 * self.OFFSET))//self.playBoard.rows))
        return(tileXCoord,tileYCoord) 
    
    # Convert tile coordinates to screen position
    def coordToScreenPos(self, coord):
        leftEdgeOfTiles = int(self.playBoard.rect_x + 0.4 * self.LENGTH) 
        topEdgeOfTiles = int(self.playBoard.rect_y - 0.15 * self.LENGTH) 
        x = int(leftEdgeOfTiles + (self.LENGTH - (.02 * self.OFFSET))//self.playBoard.cols * coord[0]) 
        y = int(topEdgeOfTiles + (self.LENGTH - (.08 * self.OFFSET))//self.playBoard.rows * coord[1])
        return(x,y)
    
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
        return

    # Check for game winner
    def checkIfPlayerJustWon(self):
        if self.currPlayer.currCoordinate == (4,4):
            if '_' in self.currPlayer.playerScore.values():
                return False
            else:
                return True
    
    # Crown the victor
    def crownVictor(self):
        self.playBoard.board[self.currPlayer.playerScorePosition[0]][self.currPlayer.playerScorePosition[1]].title_color = winner_green
        displayGameOver(self.screen, self.playerList, self.setupInfo['categories'], self.currPlayer)
                
    def handleCurrentPlayerMoves(self):
        self.currPlayer.currentNeighbors.clear()
        neighbors = self.currPlayer.currentNeighbors
        #TODO prune non max distance neighbors for a more traditional trivial pursuit experience
        ##print(self.currPlayer.currCoordinate)
        oldCoord = self.currPlayer.currCoordinate
        
        #print("POSSIBLE NEIGHBORS: ", self.currPlayer.currentNeighbors)
        if configModule.optionalPruneNeighbors:
            self.currPlayer.pruneNeighbors(self.diceRoll)
        else:
            self.currPlayer.getNeighbors(self.playBoard, self.currPlayer.currCoordinate, self.diceRoll + 1, neighbors)
        neighbors = self.currPlayer.currentNeighbors
            #print("POSSIBLE NEIGHBORS after prune : ", self.currPlayer.currentNeighbors)
        for i in range(len(neighbors)):
            #if this within our range
            if self.currPlayer.checkValidMove(self.playBoard.board[neighbors[i][0]][neighbors[i][1]]):
                #check if the player has moved beyond their starting square
                if self.currPlayer.currCoordinate != neighbors[i]:
                    #TODO make the call from here to spawn the end turn button
                    if configModule.online:
                        if self.clientNumber == self.controllingPlayer:
                            self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Move Token']-1].lockOut = False
                    else:
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


    def mainLoopOnline(self):
        questionId = None
        question, answer = '', ''
        hasPulled = False
        base64_string = None
        #client 0 is always the dictator at this point
        '''if self.clientNumber == 0:
            self.n.send(initObject(len(self.playerList)))'''
        if configModule.host:
            self.n.send(initObject(self.setupInfo))
        #self.n.send(startGame(True)) turn this back on when its time to handle proper connection closing and refusal
        currSelf = self.n.getObj()
       
        self.clientNumber = currSelf.id
        self.clientPlayer = self.playerList[self.clientNumber]
        #print("I AM: ", self.clientNumber, "AND PLAYER: ", self.clientPlayer.playerName)
        incData = []
        sendObj = None
        myVote = -1
        totalVotes = 0
        passTurn = False
        while self.run:

            #SERVER BULLSHIT
            ##print("SENDING: \n\t STATE: ", self.currState, "\n\t CLIENT: ", self.clientNumber, "\n\t COORDS: ", self.playerList[self.clientNumber].circle_x, ", ", self.playerList[self.clientNumber].circle_y)
            #only send things if we are the controlling player
            if self.clientNumber == self.controllingPlayer:
                sendObj = playerObj(self.currState, 
                                    self.clientNumber, 
                                    (self.playerList[self.clientNumber].circle_x, self.playerList[self.clientNumber].circle_y), 
                                    self.diceRoll,
                                    questionId,
                                    myVote, 
                                    passTurn,
                                    self.trivMenu.isOut) #send our info to the server
                
                '''print("SENDING: \n\t STATE: ", self.currState, 
                      "\n\t CLIENT: ", self.clientNumber, 
                      "\n\t COORDS: ", self.playerList[self.clientNumber].circle_x, ", ", self.playerList[self.clientNumber].circle_y,
                      "currRoll: ", self.diceRoll,
                      "Question Id: ", questionId,
                      "Answer: ", answer)'''
            else:
                sendObj = observeObject(self.clientNumber, myVote)

            incData = self.n.send(sendObj)
            print("trivMenu status according to master: ", incData.trivMenuOut)
            self.currState = incData.state
            #print("I am in state: ", self.currState, " controlling player is: ", self.controllingPlayer)
            if not incData:
                #print("FATAL: cannot connect to game")
                sys.exit()
            temp = []
            voteTemp = []
            if isinstance(incData, serverObj):
                temp.append(incData.player1Pos)
                temp.append(incData.player2Pos)
                temp.append(incData.player3Pos)
                temp.append(incData.player4Pos)
                voteTemp.append(incData.player1Vote)
                voteTemp.append(incData.player2Vote)
                voteTemp.append(incData.player3Vote)
                voteTemp.append(incData.player4Vote)
                #print("I have: ", temp, "at state: ", incData.state)
                for i in range(len(self.playerList)):
                    self.playerList[i].circle_x = temp[i][0]
                    self.playerList[i].circle_y = temp[i][1]
            for event in pygame.event.get():
                #for now only send data on event
                
                if event.type == QUIT:
                    self.run= False 
                #listeners
                rbs = self.settingsMenu.listen_for_checkBox(event)
                dbs = self.settingsMenu.listen_for_buttons(event)
                shouldRedraw = configModule.optionalMatchOriginalColors
                if self.clientNumber == self.controllingPlayer:
                    self.currPlayer.checkIfHeld(event)
                    self.currPlayer.clampPlayer(self.WIDTH, self.HEIGHT)     
                self.testButton.isClicked(event)
                abs = self.testMenu.listen_for_buttons(event)
                mbs = self.trivMenu.listen_for_buttons(event)
                if abs == 3 or dbs == -3:
                    self.settingsMenu.slideIn((self.WIDTH//2, self.HEIGHT//2))
                    self.testMenu.lockOut = not self.testMenu.lockOut
                #start the clock
                if self.trivMenu.triviaClock.startCounting == True:
                    self.trivMenu.triviaClock.countTime(event)
                if self.trivMenu.triviaClock.counter <= 0:
                    self.trivMenu.triviaClock.startCounting = False
                    self.trivMenu.triviaClock.shouldDraw = False
                    self.trivMenu.slideIn((self.WIDTH//2, self.HEIGHT//2))
                    self.trivMenu.resetTimer()
                    self.currState = 0
                
                if self.clientNumber == self.controllingPlayer:
                    # Roll Dice Button
                    if abs == self.testMenuButtons['Roll Dice']-1 and self.currPlayer.hasRolled == False:
                        self.currState = 1 #TODO change this to send to server
                    # Move Token Button
                    elif abs == self.testMenuButtons['Move Token']-1:
                        self.currState = 2
                    elif abs == self.testMenuButtons['Save Game']-1:
                        #print('Save Game')
                        self.databaseConnection.saveCurrentGameState(self.playerList, self.setupInfo, self.clientNumber)
                    elif abs == 1:
                        self.currState == 3
                        #self.trivMenu.triviaClock.startCounting = True
                        
                    if shouldRedraw != configModule.optionalMatchOriginalColors:
                        #self.playBoard.create_board()
                        self.playBoard.updateTileColors()
                        self.legend.updateLegendColors()
                        for play in self.playerList:
                            play.updateColor()
                        for scoreboard in self.scoreboards:
                            scoreboard.updateScoreboxColors()
                    if mbs == -3:
                        #change the trivia button to accurately reflect what stage you are in
                        if self.currState < 3:
                            self.currState = 3
                        else:
                            self.currState = 4

                if not self.clientNumber == self.controllingPlayer:
                    if mbs >= 0 and self.currState == 4:
                        if mbs == 0:
                            myVote = 0
                        else:
                            myVote = 1
            
            if self.currState == 0:
                #print(self.trivMenu.isOut, " : ", self.trivMenu.preventSliding)
                #self.trivMenu.preventSliding = True
                if self.trivMenu.isOut:
                    pass
                    #self.trivMenu.slideIn((self.WIDTH//2, self.HEIGHT//2))
                    #self.trivMenu.isOut = False
                self.controllingPlayer = incData.controller
                if passTurn == True:
                    print("passing control")
                    self.currPlayer = self.playerList[self.controllingPlayer]
                    passTurn = False
                totalVotes = 0
                myVote = -1
                if self.clientNumber == self.controllingPlayer:
                    self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Roll Dice']-1].lockOut=False
                    self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Move Token']-1].lockOut=True
                else:
                    self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Roll Dice']-1].lockOut=True
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
                if self.clientNumber != self.controllingPlayer:
                    self.testDice.diceValue = incData.dice
                    self.diceRoll = incData.dice
                if not self.currPlayer.hasRolled:
                    self.testDice.rollDice(self.screen)
                self.trivMenu.preventSliding = False
                self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Roll Dice']-1].lockOut = True
                self.currPlayer.hasRolled = True 
                self.drawDice = True
                if self.clientNumber != self.controllingPlayer: 
                    self.trivMenu.startButton.lockOut = True
                else:
                    self.trivMenu.startButton.lockout = False

            elif self.currState == 2:
                currentTokenPosition = self.screenPosToCoord()
                passTurn = False
                #################
                tile = self.playBoard.board[currentTokenPosition[0]][currentTokenPosition[1]]
                if tile.mDistinct == tileDistinction.CENTER:
                    self.trivMenu.startButton.button_text = "Select Category"
                else:
                    self.trivMenu.startButton.button_text = "Get Question"
                if currentTokenPosition in self.currPlayer.currentNeighbors and \
                    currentTokenPosition != self.currPlayer.currCoordinate:
                    self.advanceToken(currentTokenPosition)
                    self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Move Token']-1].lockOut = True
                    self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Roll Dice']-1].lockOut = True
                    self.currPlayer.currCoordinate = currentTokenPosition
                    tile_coords = self.screenPosToCoord()
                    tile = self.playBoard.board[tile_coords[0]][tile_coords[1]]
                    if tile.mDistinct == tileDistinction.ROLL:
                        print("Player landed on Roll Again tile. Roll the dice again.")
                        self.currPlayer.hasRolled = False
                        self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Roll Dice']-1].lockOut = False  # Unlock the roll dice button
                        self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Move Token']-1].lockOut = True # Unlock the move token button
                        if self.clientNumber == self.controllingPlayer: 
                            self.currState = 0  # Reset to roll dice state
                    else:
                        self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Roll Dice']-1].lockOut = True
                        self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Move Token']-1].lockOut = True
                        print("SLIDING IN ON STATE 2")
                        self.trivMenu.slideIn((self.WIDTH//2, self.HEIGHT//2))
                        self.drawDice = False

                if self.controllingPlayer == self.clientNumber:
                    self.trivMenu.startButton.lockOut = False
                    self.trivMenu.haltButtons = False
                else:
                    self.trivMenu.startButton.lockOut = True
                    self.trivMenu.haltButtons = True

            elif self.currState == 3:
                #self.trivMenu.currState += 1
                self.trivMenu.triviaClock.shouldDraw = True
                self.trivMenu.triviaClock.startCounting = True

                if not hasPulled:
                    #print("HAS NOT PULLED")
                    categories = self.setupInfo['categories']
                    category_names = []

                    if len(categories) < 4 or categories == {}:
                        categories = [{'name': 'Astronomy', 'color': match_red, 'askedQuestions': []}, {'name': 'Biology', 'color': match_yellow, 'askedQuestions': []}, {'name': 'Chemistry', 'color': match_blue, 'askedQuestions': []}, {'name': 'Geology', 'color': match_green, 'askedQuestions': []}]

                    for catRec in categories:
                        category_names.append(catRec['name'])

                    tile_coords = self.screenPosToCoord()
                    tile = self.playBoard.board[tile_coords[0]][tile_coords[1]]
                    # Handle the normal trivia tile logic
                    tile_trivia = self.tileColorMapping[tile.mTrivia]
                    selectedCategory = None
                    for category in categories:
                        if category['color'] == tile_trivia:
                            selectedCategory = category
                            break

                    if self.clientNumber == self.controllingPlayer:
                        if selectedCategory:
                            questionAndAnswerInCategoryThatWasntAlreadyAsked = self.databaseConnection.getQuestionAndAnswerByCategoryThatWasntAlreadyAsked(selectedCategory['name'], selectedCategory['askedQuestions'])
                            if questionAndAnswerInCategoryThatWasntAlreadyAsked == None:
                                questionId, question, answer, base64_string = self.databaseConnection.getQuestionAndAnswerByCategory(selectedCategory['name'])
                                for category in self.setupInfo['categories']:
                                    if category['name'] == selectedCategory['name']:
                                        category['askedQuestions'] = [questionId]
                                        break
                            else:
                                questionId, question, answer, base64_string = questionAndAnswerInCategoryThatWasntAlreadyAsked
                                for category in self.setupInfo['categories']:
                                    if category['name'] == selectedCategory['name']:
                                        category['askedQuestions'].append(questionId)
                                        break    
                        else:
                            print("No category found")
                    else:
                        question, answer, base64_string = self.databaseConnection.getQuestionAndAnswerById(incData.questionId)

                    self.trivMenu.activeDictionary[childType.TEXT][0].updateText(question)
                    
                    if base64_string is not None:
                        self.trivMenu.drawImage = True
                        self.trivMenu.base64_string = base64_string
                        
                    hasPulled = True

                # self.trivMenu.haltWidgetDraw = True
                self.trivMenu.startButton.button_text = "Reveal Answer"
            elif self.currState == 4:
                if self.controllingPlayer == self.clientNumber:
                    self.trivMenu.startButton.lockOut = True
                    self.trivMenu.haltButtons = True
                else:
                    self.trivMenu.startButton.lockOut = True
                    self.trivMenu.haltButtons = False
                self.trivMenu.haltWidgetDraw = False
                if self.trivMenu.away == False and self.trivMenu.activeIndex == 0:
                    self.trivMenu.switchActiveDictionary(1)
                self.trivMenu.activeDictionary[childType.TEXT][0].updateText(answer)
                count = 0
                #the vote system
                totalVotes = 0
                for ent in self.trivMenu.activeDictionary[childType.VOTE]:
                    if voteTemp[count] > -1:
                        ent.voteSubmitted = True
                        totalVotes += 1
                        if voteTemp[count] == 0:
                            ent.correct = True
                        else:
                            ent.correct = False
                    count += 1
                if totalVotes >= len(self.playerList) - 1:
                    #print("EVALUATING")
                    voteScore = 0
                    for i in voteTemp:
                        if i == 0:
                            voteScore += 1
                        elif i == 1:
                            voteScore -= 1

                    # Update Player's Report Card
                    if voteScore > 0:
                        wrongAnswer = False
                    else:
                        wrongAnswer = True
                    self.currPlayer.updateReportCard(self.tileColorMapping[tile.mTrivia], wrongAnswer) 

                    # Update Player's Score
                    if voteScore > 0:
                        if self.currPlayer.currCoordinate in [(4,0),(8,4),(4,8),(0,4)]: 
                                self.updatePlayerScore(self.currPlayer.currCoordinate)
                        elif self.currPlayer.currCoordinate == (4,4):
                            if self.checkIfPlayerJustWon():
                                self.crownVictor()
                                self.databaseConnection.savePlayerGrades(self.playerList, self.setupInfo)
                                return
                    else:
                        passTurn = True
                    #advance stuff
                    #if self.clientNumber == self.controllingPlayer:
                    self.currState = 5
                    #self.trivMenu.slideIn((self.WIDTH//2, self.HEIGHT//2))
                    #if self.clientNumber == self.controllingPlayer:
                
            elif self.currState == 5:
                self.trivMenu.resetTimer()
                print("should call slide state 5")
                self.trivMenu.slideIn((self.WIDTH//2, self.HEIGHT//2))
                self.trivMenu.startButton.lockOut = True
                questionId = None
                question = ''
                answer = ''
                base64_string = None
                self.trivMenu.drawImage = False
                self.trivMenu.base64_string = None
                if self.clientNumber == self.controllingPlayer:
                        self.currState = 6
            elif self.currState == 6:
                self.currState = 0

            if not self.testDice.rolling and self.currPlayer.hasRolled:
                self.diceRoll = self.testDice.diceValue
                self.currPlayer.updateBoxByDice(self.diceRoll, self.playBoard.board[0][0].box.size[0])
            
            #You must be the right player to do these
            if not self.clientNumber == self.controllingPlayer:
                self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Roll Dice']-1].lockOut=True
                self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Move Token']-1].lockOut=True
                self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Save Game']-1].lockOut=True
            #get the press hold event for the player
            
            self.handleCurrentPlayerMoves()
            
            #game state logic
            #draw calls
            self.screen.fill((25, 28, 38))
            self.testParticle.drawParticles(self.screen)
            self.playBoard.drawBoard(self.screen, self.currPlayer.currentNeighbors)
            #self.debugButton()

        
            # self.questionAnswerTextWidget.drawWidget(self.screen)
            #self.testDice.drawDice(self.screen, self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Roll Dice']-1].lockOut)

            self.drawPlayers()
            self.drawScoreboards()
            self.testMenu.drawMenu(self.screen, base3)
            self.drawPlayerTurn()            
            self.legend.draw(self.screen)
            if self.clientNumber == self.controllingPlayer:
                self.testDice.drawDice(self.screen, self.drawDice)
            else:
                self.testDice.drawDice(self.screen, self.drawDice, incData.dice)
            self.settingsMenu.drawMenu(self.screen)
            self.trivMenu.drawMenu(self.screen)
            #self.slider.draw(self.screen)
            #bounding box draw
            if self.boundingDraw:
                pygame.draw.rect(self.screen, debug_red, self.currPlayer.clampBox.box, 2)
            
            pygame.display.update()
            self.clock.tick(60) #60 fps

        pygame.quit()

    #offline variant, too lazy to surgically align things
    def mainLoopOffline(self):
        questionId = None
        question, answer = '', ''
        hasPulled = False
        base64_string = None
        while self.run:
            for event in pygame.event.get():
                #for now only send data on event
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
                    #print("RESET!")
                    self.trivMenu.resetTimer()
                    self.clientNumber +=1
                    if self.clientNumber >= self.setupInfo['number_of_players']:
                        self.clientNumber = 0
                    self.currPlayer = self.playerList[self.clientNumber]
                    questionId = None
                    question = ''
                    answer = ''
                    base64_string = None
                    self.trivMenu.drawImage = False
                    self.trivMenu.base64_string = None
                    hasPulled = False
                    self.currState = 0
                #BUTTON CALLBACK
                # Roll Dice Button
                if abs == self.testMenuButtons['Roll Dice']-1 and self.currPlayer.hasRolled == False:
                    self.testDice.rollDice(self.screen)
                    self.currState = 1 #TODO change this to send to server
                # Move Token Button
                elif abs == self.testMenuButtons['Move Token']-1:

                    self.currState = 2
                elif abs == self.testMenuButtons['Save Game']-1:
                    #print('Save Game')
                    self.databaseConnection.saveCurrentGameState(self.playerList, self.setupInfo, self.clientNumber)
                if abs == 3 or dbs == -3:
                    self.settingsMenu.slideIn((self.WIDTH//2, self.HEIGHT//2))
                    self.testMenu.lockOut = not self.testMenu.lockOut
                elif abs == 1:
                    self.currState == 3
                    #self.trivMenu.triviaClock.startCounting = True
                    
                if shouldRedraw != configModule.optionalMatchOriginalColors:
                    #self.playBoard.create_board()
                    self.playBoard.updateTileColors()
                    self.legend.updateLegendColors()
                    for play in self.playerList:
                        play.updateColor()
                    for scoreboard in self.scoreboards:
                        scoreboard.updateScoreboxColors()
                if mbs == -3:
                    #change the trivia button to accurately reflect what stage you are in
                    if self.currState < 3:
                        self.currState = 3
                    else:
                        self.currState = 4
                elif mbs >= 0:
                    self.currState = 5

                    #Update Player's Report Card
                    self.currPlayer.updateReportCard(self.tileColorMapping[tile.mTrivia], mbs)

                    #check if correct
                    if mbs == 0:
                        #print("correct clicked")
                        if self.currPlayer.currCoordinate in [(4,0),(8,4),(4,8),(0,4)]: 
                            self.updatePlayerScore(self.currPlayer.currCoordinate)
                        elif self.currPlayer.currCoordinate == (4,4):
                            if self.checkIfPlayerJustWon():
                                self.crownVictor()
                                self.databaseConnection.savePlayerGrades(self.playerList, self.setupInfo)
                                return
                    else:
                        self.clientNumber +=1
                        if self.clientNumber >= len(self.playerList):
                            self.clientNumber = 0
                        self.currPlayer = self.playerList[self.clientNumber]
            #print("currplayer ", self.currPlayer.playerName)
            #game state logic
            if self.currState == 0:
                questionId = None
                question = ''
                answer = ''
                base64_string = None
                self.trivMenu.drawImage = False
                self.trivMenu.base64_string = None
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
                question = ''
                answer = ''
                if self.trivMenu.activeIndex == 1:
                    self.trivMenu.switchActiveDictionary(0)
                self.trivMenu.activeDictionary[childType.TEXT][0].updateText(question)
                self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Roll Dice']-1].lockOut = True
                self.currPlayer.hasRolled = True 
                self.drawDice = True

            elif self.currState == 2:
                currentTokenPosition = self.screenPosToCoord()
                tile = self.playBoard.board[currentTokenPosition[0]][currentTokenPosition[1]]
                
                if currentTokenPosition in self.currPlayer.currentNeighbors and \
                    currentTokenPosition != self.currPlayer.currCoordinate:
                    self.advanceToken(currentTokenPosition)
                    self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Move Token']-1].lockOut = True
                    self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Roll Dice']-1].lockOut = True
                    self.currPlayer.currCoordinate = currentTokenPosition
                    if tile.mDistinct == tileDistinction.CENTER:
                        print("Player coords:", self.currPlayer.currCoordinate)
                        print("Tile Coords:", tile.row, tile.col)
                        print(self.currPlayer.playerScore.values())
                        if self.checkIfPlayerJustWon():
                            self.trivMenu.activeDictionary[childType.TEXT][0].updateText("Opponents Choose Category")
                        else:
                            self.trivMenu.activeDictionary[childType.TEXT][0].updateText("You choose the category")
                        self.trivMenu.startButton.button_text = "Categories"
                else:
                    self.trivMenu.startButton.button_text = "Get Question"
                    # self.trivMenu.slideIn((self.WIDTH//2, self.HEIGHT//2))
                    tile_coords = self.screenPosToCoord()
                    tile = self.playBoard.board[tile_coords[0]][tile_coords[1]]
                    if tile.mDistinct == tileDistinction.ROLL:
                        print("Player landed on Roll Again tile. Roll the dice again.")
                        self.currPlayer.hasRolled = False
                        self.currState = 0  # Reset to roll dice state
                    else:
                        self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Roll Dice']-1].lockOut = True  # Unlock the roll dice button
                        self.testMenu.child_Dictionary[childType.BUTTON][self.testMenuButtons['Move Token']-1].lockOut = True # Unlock the move token button
                        #self.trivMenu.slideIn((self.WIDTH//2, self.HEIGHT//2))
                        if not self.trivMenu.isOut:
                            self.trivMenu.initiateSlide()
                    self.drawDice = False
                
            elif self.currState == 3:
                #self.trivMenu.currState += 1
                self.trivMenu.triviaClock.shouldDraw = True
                self.trivMenu.triviaClock.startCounting = True

                if not hasPulled:
                    #print("HAS NOT PULLED")
                    categories = self.setupInfo['categories']
                    category_names = []
                    
                    if len(categories) < 4 or categories == {}:
                        categories = [{'name': 'Astronomy', 'color': colors.match_red, 'askedQuestions': []}, {'name': 'Biology', 'color': (255, 236, 38), 'askedQuestions': []}, {'name': 'Chemistry', 'color': (41, 173, 255), 'askedQuestions': []}, {'name': 'Geology', 'color': (0, 228, 53), 'askedQuestions': []}]
                    for catRec in categories:
                        category_names.append(catRec['name'])
                        
                    print(categories)
                    print(category_names)
                    tile_coords = self.screenPosToCoord()
                    tile = self.playBoard.board[tile_coords[0]][tile_coords[1]]          
                    # Handle tile color update and redraw
                    if shouldRedraw != configModule.optionalMatchOriginalColors:
                        self.playBoard.updateTileColors()
                        self.currPlayer.updateColor()
                    if tile.mDistinct == tileDistinction.CENTER:
                        # Handle the center tile logic
                        print("Player landed on Center tile. Get a question from any category.")
                        selectedCategory = self.categorySelectionScreen(categories)
                        questionId, question, answer, base64_string = self.databaseConnection.getQuestionAndAnswerByCategory(selectedCategory)
                        self.trivMenu.activeDictionary[childType.TEXT][0].updateText(question)
                    else:
                        # Handle the normal trivia tile logic
                        tile_trivia = self.tileColorMapping[tile.mTrivia]
                        selectedCategory = None
                        for category in categories:
                            if category['color'] == tile_trivia:
                                selectedCategory = category
                                break

                        if selectedCategory:
                            questionAndAnswerInCategoryThatWasntAlreadyAsked = self.databaseConnection.getQuestionAndAnswerByCategoryThatWasntAlreadyAsked(selectedCategory['name'], selectedCategory['askedQuestions'])
                            if questionAndAnswerInCategoryThatWasntAlreadyAsked == None:
                                questionId, question, answer, base64_string = self.databaseConnection.getQuestionAndAnswerByCategory(selectedCategory['name'])
                                for category in self.setupInfo['categories']:
                                    if category['name'] == selectedCategory['name']:
                                        category['askedQuestions'] = [questionId]
                                        break
                            else:
                                questionId, question, answer, base64_string = questionAndAnswerInCategoryThatWasntAlreadyAsked
                                for category in self.setupInfo['categories']:
                                    if category['name'] == selectedCategory['name']:
                                        category['askedQuestions'].append(questionId)
                                        break    
                        else:
                            print("No category found")    

                        self.trivMenu.activeDictionary[childType.TEXT][0].updateText(question)
                        
                        if base64_string is not None:
                            self.trivMenu.drawImage = True
                            self.trivMenu.base64_string = base64_string
                        
                    hasPulled = True

                # self.trivMenu.haltWidgetDraw = True
                self.trivMenu.startButton.button_text = "Reveal Answer"
                
            elif self.currState == 4:
                self.trivMenu.triviaClock.shouldDraw = False
                self.trivMenu.triviaClock.startCounting = False
                self.trivMenu.drawImage = False
                self.trivMenu.base64_string = None
                if self.trivMenu.away == False and self.trivMenu.activeIndex == 0:
                    self.trivMenu.switchActiveDictionary(1)
                self.trivMenu.activeDictionary[childType.TEXT][0].updateText(answer)
                self.trivMenu.startButton.lockOut = True
            
            elif self.currState == 5:
                #self.trivMenu.canVote = True TURN THIS BACK ON FOR SERVER STUFF
                if self.trivMenu.isOut:
                    self.trivMenu.initiateSlide()
                self.trivMenu.resetTimer()
                questionId = None
                question = ''
                answer = ''
                base64_string = None
                self.trivMenu.drawImage = False
                self.trivMenu.base64_string = None
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
            self.legend.draw(self.screen)
            self.playBoard.drawBoard(self.screen, self.currPlayer.currentNeighbors)
            self.drawPlayers()
            self.drawScoreboards()
            self.testMenu.drawMenu(self.screen, base3)
            self.drawPlayerTurn()
            self.testDice.drawDice(self.screen, self.drawDice)
            self.settingsMenu.drawMenu(self.screen)
            self.trivMenu.drawMenu(self.screen)
            #bounding box draw
            if self.boundingDraw:
                pygame.draw.rect(self.screen, debug_red, self.currPlayer.clampBox.box, 2)
            
            pygame.display.update()
            self.clock.tick(60) #60 fps

        pygame.quit()
PID = None
def launch_pygame_server():
    # Start main.py and wait for 
    # it to finish
    global PID
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the full path to the server.py file
    server_path = os.path.join(script_dir, "network/server.py")
    PID = subprocess.Popen(["python", server_path])

def main(): 
    pygame.init()
    #print("running")
    selected_menu_action = run_start_menu()
    bypass = {'number_of_players': 2, 'players': [{'name': 'Player4', 'color': match_yellow}, {'name': 'Player3', 'color': match_blue}, {'name': 'Player1', 'color': match_red}, {'name': 'Player2', 'color': match_green}], 'categories': [{'name': 'Astronomy', 'color': match_red, 'askedQuestions': []}, {'name': 'Biology', 'color': match_yellow, 'askedQuestions': []}, {'name': 'Chemistry', 'color': match_blue, 'askedQuestions': []}, {'name': 'Computer Science', 'color': match_green, 'askedQuestions': []}]}
    if selected_menu_action == "start":   
        database = databaseConnection(dbname='trivialCompute', user='postgres', password='postgres')
        #TODO remove this later
        if configModule.bypass:
            setupInfo = bypass
            configModule.online = True
            configModule.host = True
            print("Online:", setupInfo)
        else:
            setupInfo = runSetupMenu(database)
            print(setupInfo)
            if(setupInfo['number_of_players'] in [2, 3, 4]):
                setupInfo = run_order_menu(setupInfo)
            if setupInfo == {}:
                print("No setup info found.")
                return
        if configModule.host:
            print("setting as host")
            configModule.serverName = "localhost"
            configModule.serverPort = 5555
            launch_pygame_server()
        #print(setupInfo)
        demo = pygameMain(setupInfo, database, 0)
        #demo.createGameSetupMenu(database)
        #demo.mainMenuLoop()
        demo.createSettingsMenu()
        demo.createTriviaMenu()
        demo.initializePlayersForNewGame()
        demo.legend.update_legend(categories=setupInfo['categories'])
        demo.initializeScoreboards(demo.playerList)

        # Optionally fill everyone's wedges for testing purposes
        if configModule.optionalFillScores:
            print("Filling scores")
            for play in demo.playerList:
                print("Player: ", play.playerName)
                play.playerScore =  {"c1":"R","c2":"G","c3":"B","c4":"Y"}
                print("Score: ", play.playerScore)

        if configModule.online:
            demo.mainLoopOnline()
        else:
            demo.mainLoopOffline()
    elif selected_menu_action == "restore":
        database = databaseConnection(dbname='trivialCompute', user='postgres', password='postgres')

        gameStateFromDB = database.getGameStateOfLastSavedGame()

        if gameStateFromDB is None:
            print("No saved game state found.")
            setupInfo = runSetupMenu(database)
            if(setupInfo['number_of_players'] in [2, 3, 4]):
                setupInfo = run_order_menu(setupInfo)
            if setupInfo == {}:
                print("No setup info found.")
                return
            demo = pygameMain(setupInfo, database, 0)
            demo.createSettingsMenu()
            demo.createTriviaMenu()
            demo.initializePlayersForNewGame()
            demo.legend.update_legend(categories=setupInfo['categories'])
            demo.initializeScoreboards(demo.playerList)            
            if configModule.online:
                demo.mainLoopOnline()
            else:
                demo.mainLoopOffline()
    
        else:
            #print("Previous game state found.")
            (id, playerPositions, playerScores, playerReportCards, setupInfo, currPlayerIndex, gameDate) = gameStateFromDB
            converted_setupInfo = {
                'number_of_players': setupInfo['number_of_players'],
                'players': [
                    {
                        'name': player['name'],
                        'color': tuple(player['color'])  # Convert color list to tuple
                    }
                    for player in setupInfo['players']
                ],
                'categories': [
                    {
                        'name': category['name'],
                        'color': tuple(category['color']),
                        'askedQuestions': category['askedQuestions']
                    }
                    for category in setupInfo['categories']
                ]
            }

            demo = pygameMain(converted_setupInfo, database, currPlayerIndex)
            #demo.mainMenuLoop()
            demo.createSettingsMenu()
            demo.createTriviaMenu()

            playerScoresList = list(playerScores.values())
            demo.restorePlayerScores(playerScoresList)


            newReportCardDict = {}
            for player, reportCardDict in playerReportCards.items():
                newReportCardDict[player] = {}
                for key_str, value_list in reportCardDict.items():
                    # Convert the string key to a tuple
                    key_tuple = ast.literal_eval(key_str)
                    # Convert the list value to a tuple
                    value_tuple = tuple(value_list)
                    # Assign to the new dictionary
                    newReportCardDict[player][key_tuple] = value_tuple

            playerReportCardsList = list(newReportCardDict.values())
            demo.restorePlayerReportCards(playerReportCardsList)

            convertedPlayerPositionsTuple = tuple((key, tuple(value)) for key, value in playerPositions.items())
            demo.initializePlayersForRestoreGame(convertedPlayerPositionsTuple)

            demo.legend.update_legend(categories=converted_setupInfo['categories'])
            demo.initializeScoreboards(demo.playerList)

        if configModule.online:
            demo.mainLoopOnline()
        else:
            demo.mainLoopOffline()
        pygame.quit()
    elif selected_menu_action == "join":
        database = databaseConnection(dbname='trivialCompute', user='postgres', password='postgres')
        configModule.online = True
        demo = pygameMain("join", database, 0)
        demo.createSettingsMenu()
        demo.createTriviaMenu()
        demo.initializePlayersForNewGame()
        demo.legend.update_legend(categories=demo.setupInfo['categories'])
        demo.initializeScoreboards(demo.playerList)  
        if configModule.online:
            demo.mainLoopOnline()
        else:
            demo.mainLoopOffline()
    else:
        pygame.quit()
    print("attempting kill")
    if configModule.host:
        PID.kill()
if __name__=="__main__": 
    main() 