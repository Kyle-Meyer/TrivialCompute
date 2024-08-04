import pygame
import sys
from menu import *
from slideBarWidget import slideBarWidget

class slidingMenu(menu):
    
    toDraw = False
    startX = 0
    startY = 0
    menuDuration = 0
    newCent = 0
    isOut = False
    stateList = []
    activeDictionary = {}
    exitButton = button((-640, 500),  100, 50, "Exit")
    rightButton = button((-550, 500),  50, 50, ">")
    leftButton = button((-720, 500),  50, 50, "!")
    activeIndex = 0

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
    
    def updateButtonFadeBoxes(self):
        self.exitButton.updateFadeBox()
        self.rightButton.updateFadeBox()
        self.leftButton.updateFadeBox()

    def addDictionary(self):
        newDict = {}
        newDict[childType.BUTTON] = []
        newDict[childType.MENU] = []
        newDict[childType.TEXT] = []
        newDict[childType.SLIDER] = []
        newDict[childType.CHECK] = []
        self.stateList.append(newDict)
    
    def switchActiveDictionary(self, index):
        self.activeDictionary = self.stateList[index]

    def slideFadeBox(self):
        time_elapsed = pygame.time.get_ticks() - self.start_time
        if self.slidingIn:
            if time_elapsed <= self.menuDuration:
                self.fadeBox.x = self.ease_in(time_elapsed, -self.fadeBox.rect_width, self.overlayTarget[0] + self.fadeBox.rect_width, self.menuDuration)
            else:
                self.fadeBox.x = self.overlayTarget[0]  # Stop the rectangle at the target position
            
        elif self.slidingOut:
            if time_elapsed <= self.menuDuration:
                self.fadeBox.x = self.ease_in(time_elapsed, self.overlayTarget[0],  -self.fadeBox.rect_width, self.menuDuration)
            else:
                self.fadeBox.x =  -self.fadeBox.rect_width  # Stop the rectangle at the target position
        #print(self.fadeBox.x, " : ", time_elapsed)
    def slideMenu(self):
        time_elapsed = pygame.time.get_ticks() - self.start_time
        if self.slidingIn:
            initial_x = -self.rect.width - 10
            target_x = self.fadeBox.rect_width // 2
            if time_elapsed <= self.menuDuration:
                self.rect.centerx = self.ease_in(time_elapsed, initial_x, target_x - initial_x, self.menuDuration)
                self.exitButton.button_rect.centerx = self.ease_in(time_elapsed, -640, 1280, self.menuDuration)
                self.rightButton.button_rect.centerx = self.ease_in(time_elapsed, -550, 1280, self.menuDuration)
                self.leftButton.button_rect.centerx = self.ease_in(time_elapsed, -730, 1280, self.menuDuration)
            else:
                self.rect.centerx = target_x
                self.exitButton.button_rect.centerx = 640
                self.rightButton.button_rect.centerx = 1280 - 550
                self.leftButton.button_rect.centerx = 1280 - 730
            self.updateButtonFadeBoxes()

            
        elif self.slidingOut:
            initial_x = self.fadeBox.rect_width // 2
            target_x = -self.rect.width - 10
            if time_elapsed <= self.menuDuration:     
                self.rect.centerx = self.ease_in(time_elapsed, initial_x, target_x - initial_x, self.menuDuration)
                self.exitButton.button_rect.centerx = self.ease_in(time_elapsed,1280-640, -1280, self.menuDuration)
                self.rightButton.button_rect.centerx = self.ease_in(time_elapsed, 1280-550, -1280, self.menuDuration)
                self.leftButton.button_rect.centerx = self.ease_in(time_elapsed, 1280-730, -1280, self.menuDuration)
            else:
                self.rect.centerx = target_x
                self.exitButton.button_rect.centerx = -640
                self.rightButton.button_rect.centerx = -550
                self.leftButton.button_rect.centerx = -730
            self.updateButtonFadeBoxes()

        #print(self.newCent, " : ", time_elapsed)
    def slideButtons(self):
        time_elapsed = pygame.time.get_ticks() - self.start_time
        if self.slidingIn:
            for i in range(len(self.activeDictionary[childType.BUTTON])):
                currWidget = self.activeDictionary[childType.BUTTON][i]
                initial_x = currWidget.originalX
                target_x = currWidget.originalX + 1280
                currButton = self.activeDictionary[childType.BUTTON][i]
                if time_elapsed <= self.menuDuration:
                    currButton.button_rect.centerx = self.ease_in(time_elapsed, initial_x, target_x - initial_x, self.menuDuration)
                else:
                    currButton.button_rect.centerx = target_x
            
        elif self.slidingOut:
             for i in range(len(self.activeDictionary[childType.BUTTON])):
                currWidget = self.activeDictionary[childType.BUTTON][i]
                initial_x = currWidget.originalX + 1280
                target_x = currWidget.originalX
                currButton = self.activeDictionary[childType.BUTTON][i]
                if time_elapsed <= self.menuDuration:     
                    currButton.button_rect.centerx = self.ease_in(time_elapsed, initial_x, target_x - initial_x, self.menuDuration)
                else:
                    currButton.button_rect.centerx = target_x

    def slideSliders(self):
        time_elapsed = pygame.time.get_ticks() - self.start_time
        if self.slidingIn:
            initial_x = -self.rect.width - 10
            target_x = self.fadeBox.rect_width // 2
            for i in range(len(self.activeDictionary[childType.SLIDER])):
                currButton = self.activeDictionary[childType.SLIDER][i]
                thumbTarg = currButton.storedXVal
                if thumbTarg <= 0:
                    thumbTarg = target_x
                if time_elapsed <= self.menuDuration:
                    currButton.rect.centerx = self.ease_in(time_elapsed, initial_x, target_x - initial_x, self.menuDuration)
                    currButton.sliderRect.centerx = self.ease_in(time_elapsed, initial_x, target_x - initial_x, self.menuDuration)
                    currButton.thumbRect.centerx = self.ease_in(time_elapsed, initial_x, thumbTarg - initial_x, self.menuDuration)
                else:
                    currButton.rect.centerx = target_x
                    currButton.sliderRect.centerx = target_x
                    currButton.thumbRect.centerx = thumbTarg
                    self.isOut = True

        elif self.slidingOut:
            self.isOut = False
            initial_x = self.fadeBox.rect_width // 2
            target_x = -self.rect.width - 10
            for i in range(len(self.activeDictionary[childType.SLIDER])):
                currButton = self.activeDictionary[childType.SLIDER][i]
                thumbTarg = currButton.storedXVal
                if time_elapsed <= self.menuDuration:     
                    currButton.rect.centerx = self.ease_in(time_elapsed, initial_x, target_x - initial_x, self.menuDuration)
                    currButton.sliderRect.centerx = self.ease_in(time_elapsed, initial_x, target_x - initial_x, self.menuDuration)
                    currButton.thumbRect.centerx = self.ease_in(time_elapsed, thumbTarg, target_x - thumbTarg, self.menuDuration)
                else:
                    currButton.rect.centerx = target_x
                    currButton.sliderRect.centerx = target_x
                    currButton.thumbRect.centerx = target_x

    #TODO make a store for each widget for their original X position, handle it here instead of in the widget itself
    def slideTextWidgets(self):
        time_elapsed = pygame.time.get_ticks() - self.start_time
        if self.slidingIn:
            for i in range(len(self.activeDictionary[childType.TEXT])):
                currWidget = self.activeDictionary[childType.TEXT][i]
                initial_x = currWidget.originalX
                target_x = currWidget.originalX + 1280
                if time_elapsed <= self.menuDuration:
                    currWidget.rect.centerx = self.ease_in(time_elapsed, initial_x, target_x - initial_x, self.menuDuration)
                else:
                    currWidget.rect.centerx = target_x
            
        elif self.slidingOut:
            for i in range(len(self.activeDictionary[childType.TEXT])):
                currWidget = self.activeDictionary[childType.TEXT][i]
                initial_x = currWidget.originalX + 1280
                target_x = currWidget.originalX
                if time_elapsed <= self.menuDuration:     
                    currWidget.rect.centerx = self.ease_in(time_elapsed, initial_x, target_x - initial_x, self.menuDuration)
                else:
                    currWidget.rect.centerx = target_x
    
    def slideCheckBoxes(self):
        time_elapsed = pygame.time.get_ticks() - self.start_time
        if self.slidingIn:
            for i in range(len(self.activeDictionary[childType.CHECK])):
                currWidget = self.activeDictionary[childType.CHECK][i]
                initial_x = currWidget.originalX
                target_x = currWidget.originalX + 1280
                if time_elapsed <= self.menuDuration:
                    currWidget.outer_rect.centerx = self.ease_in(time_elapsed, initial_x, target_x - initial_x, self.menuDuration)
                    currWidget.checkbox_rect.centerx = self.ease_in(time_elapsed, initial_x, target_x - initial_x, self.menuDuration)
                else:
                    currWidget.outer_rect.centerx = target_x
                    currWidget.checkbox_rect.centerx = target_x
            
        elif self.slidingOut:
            for i in range(len(self.activeDictionary[childType.CHECK])):
                currWidget = self.activeDictionary[childType.CHECK][i]
                initial_x = currWidget.originalX + 1280
                target_x = currWidget.originalX
                if time_elapsed <= self.menuDuration:     
                    currWidget.outer_rect.centerx = self.ease_in(time_elapsed, initial_x, target_x - initial_x, self.menuDuration)
                    currWidget.checkbox_rect.centerx = self.ease_in(time_elapsed, initial_x, target_x - initial_x, self.menuDuration)
                else:
                    currWidget.outer_rect.centerx = target_x
                    currWidget.checkbox_rect.centerx = target_x
                    
    def slideAll(self):
        self.slideFadeBox()
        self.slideMenu()
        self.slideButtons()
        if self.slidingOut == True and self.slidingIn == False:
            self.isOut = False       
        if not self.isOut:
            self.slideSliders()
        self.slideTextWidgets()
        self.slideCheckBoxes()     

    def bindCheckBoxes(self):
        for i in range(len(self.activeDictionary[childType.CHECK])):
            entry = self.activeDictionary[childType.CHECK][i]
            match i:
                case 0:
                    entry.checked = configModule.optionalMatchOriginalColors
                case 1:
                    entry.checked = configModule.optionalStaticBoard
                case 2:
                    entry.checked = configModule.optionalThreeDimensionalTiles
                case 3:
                    entry.checked = configModule.optionalThreeDimensionalTokens
                case 4:
                    entry.checked = configModule.optionalTileBlackOutline
                case 5:
                    entry.checked = configModule.optionalDebugMode
                case 6:
                    entry.checked = configModule.optionalFastDice
                case 7:
                    entry.checked = configModule.optionalPruneNeighbors

    def listen_for_checkBox(self, event):
        super().listen_for_checkBox(event)
        for i in range(len(self.activeDictionary[childType.CHECK])):
            entry = self.activeDictionary[childType.CHECK][i]
            match i:
                case 0:
                    configModule.optionalMatchOriginalColors = entry.checked

                case 1:
                    configModule.optionalStaticBoard = entry.checked 

                case 2:
                    configModule.optionalThreeDimensionalTiles = entry.checked

                case 3:
                    configModule.optionalThreeDimensionalTokens = entry.checked

                case 4:
                    configModule.optionalTileBlackOutline = entry.checked 

                case 5:
                    configModule.optionalDebugMode = entry.checked

                case 6:
                    configModule.optionalFastDice = entry.checked

                case 7:
                    configModule.optionalPruneNeighbors = entry.checked

    def listen_for_buttons(self, event):
        selfSet = -1
        
        #check if right and left should be locked
        if self.activeIndex <= 0:
            self.leftButton.lockOut = True
        else:
            self.leftButton.lockOut = False
        if self.activeIndex == len(self.stateList) - 1:
            self.rightButton.lockOut = True
        else:
            self.rightButton.lockOut = False

        if self.exitButton.isClicked(event):
           return -3
        elif self.rightButton.isClicked(event):
            if self.activeIndex < len(self.stateList):
                self.switchActiveDictionary(self.activeIndex+1)
                self.activeIndex += 1
            else:
                self.rightButton.lockOut = True
        elif self.leftButton.isClicked(event):
            if self.activeIndex > 0:
                self.switchActiveDictionary(self.activeIndex-1)
                self.activeIndex -= 1
            else:
                self.leftButton.lockOut = True
        else:
            for i in range(len(self.activeDictionary[childType.BUTTON])):
                if self.activeDictionary[childType.BUTTON][i].isClicked(event):
                    selfSet = i
            return selfSet


    def drawMenu(self, screen):
        
        self.slideAll()
        self.fadeBox.drawAlpha(screen)
        self.draw_rounded_rect(screen)
        text_surf = self.title.render(self.title_text, True, base3)
        text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.centery - (self.menu_height // 2) + self.title_text_size))
        screen.blit(text_surf, text_rect)
        for i in range(len(self.activeDictionary[childType.BUTTON])):
            self.activeDictionary[childType.BUTTON][i].draw_button(screen)
        for i in range(len(self.activeDictionary[childType.SLIDER])):
            self.activeDictionary[childType.SLIDER][i].draw(screen)
        #for i in range(len(self.activeDictionary[childType.MENU])):
        #    self.activeDictionary[childType.MENU][i].drawMenu(screen)
        for i in range(len(self.activeDictionary[childType.TEXT])):
            self.activeDictionary[childType.TEXT][i].drawWidget(screen)
        for i in range(len(self.activeDictionary[childType.CHECK])):
            #print("drawing: ", i, " at ", self.activeDictionary[childType.CHECK][i].outer_rect.center)
            self.activeDictionary[childType.CHECK][i].drawWidget(screen)
        self.exitButton.draw_button(screen)
        self.rightButton.draw_button(screen)
        self.leftButton.draw_button(screen)

    def __init__(self, position : tuple[int, ...], width = 200, height = 200, titleText = "place holder"):
        super().__init__(position, width, height, titleText)
        self.startX = -width//2 - 10
        self.newCent = self.startX
        self.startY = self.rect.centery
        self.exitButton = button((-640, 500),  100, 50, "Exit")
        self.rightButton = button((-550, 500),  50, 50, ">")
        self.leftButton = button((-550, 500),  50, 50, "<")
        self.activeDictionary = self.child_Dictionary
        self.stateList.append(self.activeDictionary)
        self.activeIndex = 0
        