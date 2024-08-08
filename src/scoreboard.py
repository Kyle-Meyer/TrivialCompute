import pygame
from colors import *

class scoreboard:
    def __init__(self, name, color, x_pos, y_pos, width, height):
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height
        self.name = name
        
    def drawScoreboard(self, screen, score):
        miniTileWidth = self.width * 0.7 // 2
        miniTileHeight = self.height * 0.7 // 2

        # Set position of player's scorebox
        scoreBox = (self.x_pos, self.y_pos)

        # Draw the player's scorebox
        pygame.draw.rect(screen, null, pygame.Rect(scoreBox[0],scoreBox[1],self.width,self.height), 0)            
        
        # Draw the player's scorebox outline
        pygame.draw.rect(screen, self.color, pygame.Rect(scoreBox[0],scoreBox[1],self.width,self.height), 4)

        # Set the mini-tile colors
        miniTileColors = [lightNull, lightNull, lightNull, lightNull]

        match_colors = [match_red, match_green, match_blue, match_yellow]
        HQ_colors = [HQ_red, HQ_green, HQ_blue, HQ_yellow]
        colors={}

        if optionalMatchOriginalColors:
            colors["R"] = match_red
            colors["G"] = match_green
            colors["B"] = match_blue
            colors["Y"] = match_yellow
        else:
            colors["R"] = HQ_red
            colors["G"] = HQ_green
            colors["B"] = HQ_blue
            colors["Y"] = HQ_yellow

        if score["c1"] == "R":
            miniTileColors[0] = colors['R']
        if score["c2"] == "G":  
            miniTileColors[1] = colors['G']
        if score["c3"] == "B":
            miniTileColors[2] = colors['B']
        if score["c4"] == "Y":
            miniTileColors[3] = colors['Y']

        # Draw the mini-tiles
        pygame.draw.rect(screen, miniTileColors[0], pygame.Rect(scoreBox[0]+self.width//2-miniTileWidth,scoreBox[1]+self.height//2-miniTileHeight,miniTileWidth,miniTileHeight), 0)   
        pygame.draw.rect(screen, miniTileColors[2], pygame.Rect(scoreBox[0]+self.width//2,scoreBox[1]+self.height//2,miniTileWidth,miniTileHeight), 0)
        pygame.draw.rect(screen, miniTileColors[1], pygame.Rect(scoreBox[0]+self.width//2-miniTileWidth,scoreBox[1]+self.height//2,miniTileWidth,miniTileHeight), 0)
        pygame.draw.rect(screen, miniTileColors[3], pygame.Rect(scoreBox[0]+self.width//2,scoreBox[1]+self.height//2-miniTileHeight,miniTileWidth,miniTileHeight), 0)
        
        # Draw the mini-tile outlines
        pygame.draw.rect(screen, black, pygame.Rect(scoreBox[0]+self.width//2-miniTileWidth,scoreBox[1]+self.height//2-miniTileHeight,miniTileWidth,miniTileHeight), 1)   
        pygame.draw.rect(screen, black, pygame.Rect(scoreBox[0]+self.width//2,scoreBox[1]+self.height//2,miniTileWidth,miniTileHeight), 1)
        pygame.draw.rect(screen, black, pygame.Rect(scoreBox[0]+self.width//2-miniTileWidth,scoreBox[1]+self.height//2,miniTileWidth,miniTileHeight), 1)
        pygame.draw.rect(screen, black, pygame.Rect(scoreBox[0]+self.width//2,scoreBox[1]+self.height//2-miniTileHeight,miniTileWidth,miniTileHeight), 1)




