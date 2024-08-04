import button
from menu import menu
from textWidget import textWidget
from colors import *
import pygame
import random
from configOptions import *

class dice(object):
    diceText = textWidget((0,0), 200, 200, "0")
    diceMenu = menu((0,0), 1, 1, "dice roll")
    rolling = False
    diceValue = 0
    rollCount = 0
    current_number = 0
    update_interval = 1  # update every 1000 milliseconds (1 second)
    total_duration = 3000  # total duration of the animation (5 seconds)
    timer = 0  # track the time since the last number update
    start_time = pygame.time.get_ticks()  # get the initial time
    snap_time = pygame.time.get_ticks()

    def drawDice(self, screen, movLockout, preDestined = -1):
        # Draw the dice menu box, adjust colors conditionally
        if movLockout:
            self.diceMenu.drawMenu(screen, base3)
            self.diceText.drawWidget(screen)

        if self.rolling:
            current_time = pygame.time.get_ticks()
            if current_time - self.snap_time >= self.update_interval:
                self.diceValue = random.randint(1,6)
                self.diceText.title_text = str(self.diceValue)
                self.snap_time = current_time
                self.update_interval += 5
            if current_time - self.start_time >= self.total_duration:
                self.rolling = False
                # This is just for use in demo mode to demo with a fortuitous sequence of demo rolls
                if configModule.optionalSkeletalDemoMode:
                    self.diceValue = configModule.optionalSkeletalDemoRolls[self.rollCount]
                    self.diceText.title_text = str(self.diceValue)
                    self.rollCount += 1    
        elif self.diceValue==0:            
            self.diceText.title_text = '_'
        if preDestined >= 0:
                    self.diceValue = preDestined
                    self.diceText.title_text = str(self.diceValue)
    #this function is deceptive, it merely sets things up for the dice roll animation, the actual dice roll will take place in the draw call
    #the reason its done this way is to get around the thread lockout that takes place with pygame.display.update(), and I'm not going to bother
    #with concurrency for this
    def rollDice(self, screen):
        self.update_interval = 1  # update every 1000 milliseconds (1 second)
        if(configModule.optionalFastDice):
            self.total_duration = 300
        else:        
            self.total_duration = 3000  # total duration of the animation (5 seconds)
        self.timer = 0  # track the time since the last number update
        self.rolling = True
        # Main game loop
        running = True
        self.start_time = pygame.time.get_ticks()  # get the initial time
        self.snap_time = pygame.time.get_ticks()
       
            
    def __init__(self, position : tuple[int, ...], width = 200, height = 200):
        self.diceMenu = menu(position, width, height, "Dice Roll")
        self.diceText = textWidget(position, 200, 200, "0")
        self.diceText.border_thickness = 0
        #self.diceMenu.addChildComponent(self.diceText)
        self.diceValue = 0
        self.diceText.changeTextSize(20)
        self.diceText.moveBox(self.diceMenu.rect.center)
        #self.diceText.moveBox((self.diceText.rect.centerx, self.diceText.rect.centery))