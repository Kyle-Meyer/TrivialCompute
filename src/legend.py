import pygame
from colors import *

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
        self.create_legend_surface()

    def update_legend(self, categories):
        """ Update the legend with new categories and colors. """
        for entry in categories:
            self.categories.append(entry['name'][0:12])
            self.colors.append(entry['color'])
        self.create_legend_surface()

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

        # Draw the legend
        x = 0
        for i, category in enumerate(self.categories):
            # Draw colored rectangle
            pygame.draw.rect(self.legend_surface, self.colors[i], pygame.Rect(x, 0, 30, 30))

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
            screen.blit(self.legend_surface, self.rect)
