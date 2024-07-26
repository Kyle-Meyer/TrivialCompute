import pygame
import sys
from menu import *
from slideBarWidget import slideBarWidget
from timerClock import timerClock
from voteWidget import voteWidget
class triviaMenu(menu):
    toDraw = False
    startX = 0
    startY = 0
    menuDuration = 0
    newCent = 0
    isOut = False
    stateList = []
    activeDictionary = {}
    canVote = False
    startButton = button((0, 500),  100, 50, "Exit")

    def addChildComponent(self, inComponent):
        if isinstance(inComponent, button):
            self.activeDictionary[childType.BUTTON].append(inComponent)
        elif isinstance(inComponent, menu):
            self.activeDictionary[childType.MENU].append(inComponent)
        elif isinstance(inComponent, textWidget):
            self.activeDictionary[childType.TEXT].append(inComponent)
        elif isinstance(inComponent, slideBarWidget):
            self.activeDictionary[childType.SLIDER].append(inComponent)
        elif isinstance(inComponent, checkBoxWidget):
            self.activeDictionary[childType.CHECK].append(inComponent)
        elif isinstance(inComponent, voteWidget):
            self.activeDictionary[childType.VOTE].append(inComponent)

    
    def addDictionary(self):
        newDict = {}
        newDict[childType.BUTTON] = []
        newDict[childType.MENU] = []
        newDict[childType.TEXT] = []
        newDict[childType.SLIDER] = []
        newDict[childType.CHECK] = []
        newDict[childType.VOTE] = []
        self.stateList.append(newDict)

    def switchActiveDictionary(self, index):
        self.activeDictionary = self.stateList[index]
        self.activeIndex = index

    def slideFadeBox(self):
        time_elapsed = pygame.time.get_ticks() - self.start_time
        if self.slidingIn:
            initial_y = 720
            target_y = 0
            if time_elapsed <= self.menuDuration:
                self.fadeBox.y = self.ease_in(time_elapsed, initial_y, target_y - initial_y, self.menuDuration)
            else:
                self.fadeBox.y = target_y  # Stop the rectangle at the target position
            
        elif self.slidingOut:
            initial_y = 0
            target_y = 720
            if time_elapsed <= self.menuDuration:
                self.fadeBox.y = self.ease_in(time_elapsed, initial_y, target_y - initial_y, self.menuDuration)
            else:
                self.fadeBox.y = target_y  # Stop the rectangle at the target position
        

    def slideMenu(self):
        time_elapsed = pygame.time.get_ticks() - self.start_time
        if self.slidingIn:
            initial_y = 1060
            target_y = 360
            if time_elapsed <= self.menuDuration:
                self.rect.centery = self.ease_in(time_elapsed, initial_y, target_y - initial_y, self.menuDuration)
                self.startButton.button_rect.centery = self.ease_in(time_elapsed, 1300, -700, self.menuDuration)
            else:
                self.away = False
                self.rect.centery = target_y
                self.startButton.button_rect.centery = 600

            
        elif self.slidingOut:
            initial_y = 360
            target_y = 1060
            if time_elapsed <= self.menuDuration:     
                self.rect.centery = self.ease_in(time_elapsed, initial_y, target_y - initial_y, self.menuDuration)
                self.startButton.button_rect.centery = self.ease_in(time_elapsed, 600, 700, self.menuDuration)
            else:
                self.away = True
                self.rect.centery = target_y
                self.startButton.button_rect.centery = 1300

        #print(self.newCent, " : ", time_elapsed)
    def slideButtons(self):
        time_elapsed = pygame.time.get_ticks() - self.start_time
        if self.slidingIn:
            for i in range(len(self.activeDictionary[childType.BUTTON])):
                currWidget = self.activeDictionary[childType.BUTTON][i]
                initial_y = currWidget.originalY
                target_y = currWidget.originalY - 720
                if time_elapsed <= self.menuDuration:
                    currWidget.button_rect.centery = self.ease_in(time_elapsed, initial_y, target_y - initial_y, self.menuDuration)
                else:
                    
                    currWidget.button_rect.centery = target_y
            
        elif self.slidingOut:
            for i in range(len(self.activeDictionary[childType.BUTTON])):
                currWidget = self.activeDictionary[childType.BUTTON][i]
                initial_y = currWidget.originalY - 720
                target_y = currWidget.originalY
                if time_elapsed <= self.menuDuration:     
                    currWidget.button_rect.centery = self.ease_in(time_elapsed, initial_y, target_y - initial_y, self.menuDuration)
                else:
                    currWidget.button_rect.centery = target_y

    #TODO make a store for each widget for their original X position, handle it here instead of in the widget itself
    def slideTextWidgets(self):
        time_elapsed = pygame.time.get_ticks() - self.start_time
        if self.slidingIn:
            for i in range(len(self.activeDictionary[childType.TEXT])):
                currWidget = self.activeDictionary[childType.TEXT][i]
                initial_y = currWidget.originalY
                target_y = currWidget.originalY - 720
                if time_elapsed <= self.menuDuration:
                    currWidget.rect.centery = self.ease_in(time_elapsed, initial_y, target_y - initial_y, self.menuDuration)
                else:
                    
                    currWidget.rect.centery = target_y
            
        elif self.slidingOut:
            for i in range(len(self.activeDictionary[childType.TEXT])):
                currWidget = self.activeDictionary[childType.TEXT][i]
                initial_y = currWidget.originalY - 720
                target_y = currWidget.originalY
                if time_elapsed <= self.menuDuration:     
                    currWidget.rect.centery = self.ease_in(time_elapsed, initial_y, target_y - initial_y, self.menuDuration)
                else:
                    currWidget.rect.centery = target_y
    
    def slideVote(self):
        time_elapsed = pygame.time.get_ticks() - self.start_time
        if self.slidingIn:
            for i in range(len(self.activeDictionary[childType.VOTE])):
                currWidget = self.activeDictionary[childType.VOTE][i]
                initial_y = currWidget.originalY
                target_y = currWidget.originalY - 720
                if time_elapsed <= self.menuDuration:
                    currWidget.outer_rect.centery = self.ease_in(time_elapsed, initial_y, target_y - initial_y, self.menuDuration)
                else:
                    
                    currWidget.outer_rect.centery = target_y
            
        elif self.slidingOut:
            for i in range(len(self.activeDictionary[childType.VOTE])):
                currWidget = self.activeDictionary[childType.VOTE][i]
                initial_y = currWidget.originalY - 720
                target_y = currWidget.originalY
                if time_elapsed <= self.menuDuration:     
                    currWidget.outer_rect.centery = self.ease_in(time_elapsed, initial_y, target_y - initial_y, self.menuDuration)
                else:
                    currWidget.outer_rect.centery = target_y

    def slideClock(self):
        time_elapsed = pygame.time.get_ticks() - self.start_time
        if self.slidingIn:
            initial_y = 1060
            target_y = 360
            if time_elapsed <= self.menuDuration:
                self.triviaClock.position = (self.triviaClock.position[0],
                                             self.ease_in(time_elapsed, initial_y, target_y - initial_y, self.menuDuration))
            else:
                self.triviaClock.position = (self.triviaClock.position[0],
                                             target_y)
        elif self.slidingOut:
            initial_y = 360
            target_y = 1060
            if time_elapsed <= self.menuDuration:
                self.triviaClock.position = (self.triviaClock.position[0],
                                             self.ease_in(time_elapsed, initial_y, target_y - initial_y, self.menuDuration))
            else:
                self.triviaClock.position = (self.triviaClock.position[0],
                                             target_y)
    def resetTimer(self):
        self.triviaClock = timerClock()
        self.triviaClock.position = (900, 1060)
        self.triviaClock.shouldDraw = False
        self.canVote = False
        self.startButton.lockOut = False
    def slideAll(self):
        self.slideFadeBox()
        self.slideMenu()
        self.slideButtons()
        #if self.slidingOut == True and self.slidingIn == False:
        #    self.isOut = False       
        #if not self.isOut:
        #    self.slideSliders()
        self.slideTextWidgets()
        self.slideVote()
        self.slideClock()

    def listen_for_buttons(self, event):
        selfSet = -1
        
        if self.startButton.isClicked(event):
           return -2
        else:
            for i in range(len(self.activeDictionary[childType.BUTTON])):
                if self.activeDictionary[childType.BUTTON][i].isClicked(event):
                    selfSet = i
            return selfSet
        
    def drawMenu(self, screen):
        self.slideAll()
        self.fadeBox.drawAlpha(screen)
        self.draw_rounded_rect(screen)
        if self.triviaClock.shouldDraw:
            self.triviaClock.drawClock(screen)
        text_surf = self.title.render(self.title_text, True, base3)
        text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.centery - (self.menu_height // 2) + self.title_text_size))
        screen.blit(text_surf, text_rect)
        if not self.canVote and self.activeIndex == 0:
            self.startButton.draw_button(screen)
        if not self.haltWidgetDraw:
            for i in range(len(self.activeDictionary[childType.BUTTON])):
                self.activeDictionary[childType.BUTTON][i].draw_button(screen)
            for i in range(len(self.activeDictionary[childType.VOTE])):
                self.activeDictionary[childType.VOTE][i].drawWidget(screen)
            for i in range(len(self.activeDictionary[childType.SLIDER])):
                self.activeDictionary[childType.SLIDER][i].draw(screen)
            #for i in range(len(self.activeDictionary[childType.MENU])):
            #    self.activeDictionary[childType.MENU][i].drawMenu(screen)
            for i in range(len(self.activeDictionary[childType.TEXT])):
                self.activeDictionary[childType.TEXT][i].drawWidget(screen)
            for i in range(len(self.activeDictionary[childType.CHECK])):
                #print("drawing: ", i, " at ", self.activeDictionary[childType.CHECK][i].outer_rect.center)
                self.activeDictionary[childType.CHECK][i].drawWidget(screen)
        
        #self.rightButton.draw_button(screen)
        #self.leftButton.draw_button(screen)

    def __init__(self, position : tuple[int, ...], width = 400, height = 500, titleText = "Trivia Menu"):
        super().__init__(position, width, height, titleText)
        self.startX = -width//2 - 10
        self.newCent = self.startX
        self.startY = self.rect.centery
        self.activeDictionary = self.child_Dictionary
        self.fadeBox.x = 0
        self.fadeBox.y = 720 + 360
        self.startButton = button((640, 800),  200, 70, "Ready?")
        self.startButton.button_text_color = base3
        self.startButton.oldTextColor = base2
        self.stateList.append(self.activeDictionary)
        self.currState = 0
        self.activeIndex = 0
        self.triviaClock = timerClock()
        self.canVote = False #THIS IS NEEDED LATER FOR SERVER stuff
        self.triviaClock.position = (900, 1060)
        self.away = True
        self.haltWidgetDraw = False
        