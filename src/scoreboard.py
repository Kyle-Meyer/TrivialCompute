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

    def drawScoreboard(self, screen, score):

        # Set position of player's scorebox
        scoreBox = (self.x_pos, self.y_pos)

        # Draw the player's scorebox
        pygame.draw.rect(screen, null, pygame.Rect(scoreBox[0],scoreBox[1],self.width,self.height), 0)            
        
        # Draw the player's scorebox outline
        pygame.draw.rect(screen, self.color, pygame.Rect(scoreBox[0],scoreBox[1],self.width,self.height), 4)

        miniTileColors=[lightNull,lightNull,lightNull,lightNull]

        if score["c1"] == "R":
            miniTileColors[0] = self.miniTiles[0].mColor
        if score["c2"] == "G":  
            miniTileColors[1] = self.miniTiles[1].mColor
        if score["c3"] == "B":
            miniTileColors[2] = self.miniTiles[2].mColor
        if score["c4"] == "Y":
            miniTileColors[3] = self.miniTiles[3].mColor

        miniTileLocs = [None]*4
        miniTileLocs[0] = (scoreBox[0]+self.width//2-self.miniTiles[0].size, scoreBox[1]+self.height//2-self.miniTiles[0].size)
        miniTileLocs[1] = (scoreBox[0]+self.width//2-self.miniTiles[1].size, scoreBox[1]+self.height//2)
        miniTileLocs[2] = (scoreBox[0]+self.width//2, scoreBox[1]+self.height//2)
        miniTileLocs[3] = (scoreBox[0]+self.width//2, scoreBox[1]+self.height//2-self.miniTiles[1].size)
        
        # Draw the mini tiles
        for i in range(4):
            pygame.draw.rect(screen, miniTileColors[i], 
                             pygame.Rect(miniTileLocs[i][0],
                                         miniTileLocs[i][1],
                                         self.miniTiles[i].size,
                                         self.miniTiles[i].size),0)
        
        # Draw the mini-tile outlines
        if configModule.optionalTileBlackOutline:
            for i in range(4):
                pygame.draw.rect(screen, black, 
                                pygame.Rect(miniTileLocs[i][0],
                                            miniTileLocs[i][1],
                                            self.miniTiles[i].size,
                                            self.miniTiles[i].size),2)
        
    def updateMiniTileColors(self):
        colors = {"_":null}

        if configModule.optionalMatchOriginalColors:
            colors["R"] = match_red
            colors["G"] = match_green
            colors["B"] = match_blue
            colors["Y"] = match_yellow
        else:
            colors["R"] = HQ_red
            colors["G"] = HQ_green
            colors["B"] = HQ_blue
            colors["Y"] = HQ_yellow

        if self.miniTiles[0].mColor != null:
            self.miniTiles[0].mColor = colors["R"]
        if self.miniTiles[0].mColor != null:            
            self.miniTiles[1].mColor = colors["G"]
        if self.miniTiles[0].mColor != null:
            self.miniTiles[2].mColor = colors["B"]
        if self.miniTiles[0].mColor != null:
            self.miniTiles[3].mColor = colors["Y"]

    def updateScoreboxOutlineColors(self):
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
                
    def updateScoreboxColors(self):
        self.updateMiniTileColors()
        self.updateScoreboxOutlineColors()

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