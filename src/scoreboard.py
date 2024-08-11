import pygame
from colors import *
from tile import tile
from tile import triviaType
from tile import tileDistinction

class scoreboard(object):

    def createScoreboard(self):
        miniTileSize = int(self.width * 0.7 // 2)
        self.miniTiles.append(tile(triviaType.RED, tileDistinction.HQ, miniTileSize, 0, 0))
        self.miniTiles.append(tile(triviaType.YELLOW, tileDistinction.HQ, miniTileSize, 0, 1))
        self.miniTiles.append(tile(triviaType.GREEN, tileDistinction.HQ, miniTileSize, 0, 2))
        self.miniTiles.append(tile(triviaType.BLUE, tileDistinction.HQ, miniTileSize, 0, 3))
        for i in range(4):
            self.miniTiles[i].boardTile = False

    def drawScoreboard(self, screen, score):

        # Set position of player's scorebox
        scoreBox = (self.x_pos, self.y_pos)

        # Draw the player's scorebox
        pygame.draw.rect(screen, null, pygame.Rect(scoreBox[0],scoreBox[1],self.width,self.height), 0)            
        
        # Draw the player's scorebox outline
        pygame.draw.rect(screen, self.color, pygame.Rect(scoreBox[0],scoreBox[1],self.width,self.height), 4)

        for i in range(4):
            self.miniTiles[i].mColor = lightNull
            self.miniTiles[i].mComplimentColor = lightNull

        if configModule.optionalMatchOriginalColors:
            if score["c1"] == "R":
                self.miniTiles[0].mColor = match_red
                self.miniTiles[0].mComplimentColor = darkRed
            if score["c2"] == "G":  
                self.miniTiles[1].mColor = match_green
                self.miniTiles[1].mComplimentColor = darkGreen
            if score["c3"] == "B":
                self.miniTiles[2].mColor = match_blue
                self.miniTiles[2].mComplimentColor = darkBlue
            if score["c4"] == "Y":
                self.miniTiles[3].mColor = match_yellow
                self.miniTiles[3].mComplimentColor = darkYellow
        else:
            if score["c1"] == "R":
                self.miniTiles[0].mColor = HQ_red
                self.miniTiles[0].mComplimentColor = HQ_dark_red
            if score["c2"] == "G":  
                self.miniTiles[1].mColor = HQ_green
                self.miniTiles[1].mComplimentColor = HQ_dark_green
            if score["c3"] == "B":
                self.miniTiles[2].mColor = HQ_blue
                self.miniTiles[2].mComplimentColor = HQ_dark_blue
            if score["c4"] == "Y":
                self.miniTiles[3].mColor = HQ_yellow
                self.miniTiles[3].mComplimentColor = HQ_dark_yellow

        miniTileLocs = [None]*4
        miniTileLocs[0] = (scoreBox[0]+self.width//2-self.miniTiles[0].size, scoreBox[1]+self.height//2-self.miniTiles[0].size)
        miniTileLocs[1] = (scoreBox[0]+self.width//2-self.miniTiles[1].size, scoreBox[1]+self.height//2)
        miniTileLocs[2] = (scoreBox[0]+self.width//2, scoreBox[1]+self.height//2)
        miniTileLocs[3] = (scoreBox[0]+self.width//2, scoreBox[1]+self.height//2-self.miniTiles[1].size)
        
        # Draw the mini tiles
        for i in range(4):
            self.miniTiles[i].updateTile(miniTileLocs[i], self.miniTiles[i].size, self.miniTiles[i].size, 0, i)
            self.miniTiles[i].drawTile(screen)
        
        # Draw the mini-tile outlines
        if configModule.optionalTileBlackOutline:
            for i in range(4):
                pygame.draw.rect(screen, black, 
                                pygame.Rect(miniTileLocs[i][0],
                                            miniTileLocs[i][1],
                                            self.miniTiles[i].size,
                                            self.miniTiles[i].size),2)

    def updateScoreboxColors(self):
        if configModule.optionalMatchOriginalColors:
            if self.color == player_red:
                self.color = match_red
            elif self.color == player_green:
                self.color = match_green
            elif self.color == player_blue:
                self.color = match_blue
            elif self.color == player_yellow:
                self.color = match_yellow
        else:
            if self.color == match_red:
                self.color = player_red
            elif self.color == match_green:
                self.color = player_green
            elif self.color == match_blue:
                self.color = player_blue
            elif self.color == match_yellow:
                self.color = player_yellow

    def __init__(self, name, color, x_pos, y_pos, width, height):
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.name = name
        self.miniTiles = []
        self.createScoreboard()   
        self.updateScoreboxColors() 