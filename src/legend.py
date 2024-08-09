import pygame
from colors import *
from configOptions import *
from tile import tile
from tile import triviaType
from tile import tileDistinction

class categoryLegend:
    def __init__(self, font_size=20, screen_width=1280, screen_height=720):
        self.categories = []
        self.colors = []
        self.font_size = font_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, font_size)
        self.legend_surface = None
        self.rect = None
        self.legendTiles = []
        self.legendTileSize = 30
        self.outline = True
        self.addLegendTiles()
        self.create_legend_surface()

    def addLegendTiles(self):
        for i in range(4):
            self.legendTiles.append(tile(triviaType.RED, tileDistinction.HQ, self.legendTileSize, 0, i))

    def updateLegendColors(self):
        if configModule.optionalMatchOriginalColors:
            for i in range(4):
                if self.legendTiles[i].mTrivia  == triviaType.RED:
                    self.legendTiles[i].mColor = match_red
                elif self.legendTiles[i].mTrivia == triviaType.GREEN:
                    self.legendTiles[i].mColor = match_green
                elif self.legendTiles[i].mTrivia == triviaType.BLUE:
                    self.legendTiles[i].mColor = match_blue
                elif self.legendTiles[i].mTrivia == triviaType.YELLOW:
                    self.legendTiles[i].mColor = match_yellow
        else:
            for i in range(4):
                if self.legendTiles[i].mTrivia  == triviaType.RED:
                    self.legendTiles[i].mColor = HQ_red
                elif self.legendTiles[i].mTrivia == triviaType.GREEN:
                    self.legendTiles[i].mColor = HQ_green
                elif self.legendTiles[i].mTrivia == triviaType.BLUE:
                    self.legendTiles[i].mColor = HQ_blue
                elif self.legendTiles[i].mTrivia == triviaType.YELLOW:
                    self.legendTiles[i].mColor = HQ_yellow
        self.create_legend_surface()

    def update_legend(self, categories):
        """ Update the legend with new categories and colors. """
        for i in range(4):
            self.categories.append(categories[i]['name'][0:12])
            self.legendTiles[i].mColor = (categories[i]['color'][0],categories[i]['color'][1],categories[i]['color'][2])
            if self.legendTiles[i].mColor == HQ_red or self.legendTiles[i].mColor == match_red:
                self.legendTiles[i].mTrivia = triviaType.RED
            elif self.legendTiles[i].mColor == HQ_green or self.legendTiles[i].mColor == match_green:
                self.legendTiles[i].mTrivia = triviaType.GREEN
            elif self.legendTiles[i].mColor == HQ_blue or self.legendTiles[i].mColor == match_blue:
                self.legendTiles[i].mTrivia = triviaType.BLUE
            elif self.legendTiles[i].mColor == HQ_yellow or self.legendTiles[i].mColor == match_yellow:
                self.legendTiles[i].mTrivia = triviaType.YELLOW            
        self.updateLegendColors()

    def create_legend_surface(self):
        """ Create the surface for the legend. """
        # Define dimensions
        legend_height = self.font_size + 5
        legend_width = 0

        # Width of the board, I know this is ugly
        board_width = self.screen_height - 0.02 * self.screen_width 

        for category in self.categories:
            # Width for each category + padding
            # This is 80% of the board width divided by the number of categories
            legend_width += board_width*0.80//4  

        # Create a surface for the legend
        self.legend_surface = pygame.Surface((legend_width, legend_height))
        self.legend_surface.fill(null)  # Background color

        # Create the legend tiles
        x = 0
        for i, category in enumerate(self.categories):

            # Draw colored rectangle
            pygame.draw.rect(self.legend_surface, self.legendTiles[i].mColor, pygame.Rect(x, 0, self.legendTileSize, self.legendTileSize),0)
            if configModule.optionalTileBlackOutline:
                pygame.draw.rect(self.legend_surface, black, pygame.Rect(x, 0, self.legendTileSize, self.legendTileSize),2)
                self.outline = True
            else:
                self.outline = False

            # Draw category text
            text_surf = self.font.render(category, True, white)

            # Position text slightly below top of rectangle
            text_rect = text_surf.get_rect(topleft=(x + 50, 5))  
            self.legend_surface.blit(text_surf, text_rect)

            # Update x position for next item
            # Move x to the right for the next category
            x += board_width*0.80//4  

        # Position the legend at the bottom of screen
        # This is about as ugly as it gets
        self.rect = self.legend_surface.get_rect(topleft=(self.screen_height*0.4+140 + board_width*0.1, 
                                                          self.screen_height-(130-self.screen_height*0.15)-legend_height))  
        
    def draw(self, screen):
        """ Draw the legend on the provided screen. """
        if self.legend_surface:
            if self.outline == True and configModule.optionalTileBlackOutline == False:
                self.updateLegendColors()
            elif self.outline == False and configModule.optionalTileBlackOutline == True:
                self.updateLegendColors()
            screen.blit(self.legend_surface, self.rect)
