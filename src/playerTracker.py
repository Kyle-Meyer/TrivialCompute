from menu import menu
from textWidget import textWidget

# Class to track the current player's turn
class playerTracker(object):

    # Draw the player tracker
    def drawPlayerTracker(self, screen):
        self.playerTrackerText.drawWidget(screen)
    
    # Update the player tracker
    def updatePlayerTracker(self, screen, name, color):
        self.playerTrackerText.title_text = name+"'s Turn!"
        self.playerTrackerText.textCol = color
        self.drawPlayerTracker(screen)

    # Constructor        
    def __init__(self, position : tuple[int, ...], width = 300, height = 50):
        self.playerTrackerText = textWidget(position, width, height)
        self.playerTrackerText.changeTextSize(25)