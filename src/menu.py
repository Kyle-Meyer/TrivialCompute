import pygame 
from enum import Enum
from button import button
from colors import *
from textWidget import textWidget

class childType(Enum):
    BUTTON = 0,
    MENU = 1,
    TEXT = 2
class menu(object):

    #member vars
    border_color = base3
    title = pygame.font.init()
    title_text = "place holder"
    title_text_size = 40
    child_Dictionary = {}
    ScreenCoords = (0,0)
    menu_width = 200    
    menu_height = 200
    border_thickness = 3
    rect = pygame.Rect(ScreenCoords[0], ScreenCoords[1], menu_width, menu_height)

    #copy pasted from button class, I should probably separate this out into its own object, but for now its fine
    def draw_rounded_rect(self, surface):
        """ Draw a rectangle with rounded corners.
        If border_thickness is set, it will draw both the border and the fill color.
        """
        if self.border_thickness > 0:
            inner_rect = self.rect.inflate(-4 * self.border_thickness, -4 * self.border_thickness)
            #inner color will always be null
            pygame.draw.rect(surface, null, inner_rect, 0, 20) #hard setting the border radius as menus should be fixed "roundness"
            outer_rect = self.rect.inflate(self.border_thickness, self.border_thickness)
            pygame.draw.rect(surface, self.border_color, outer_rect, self.border_thickness, 20)
        else:
            raise ValueError("border must be >= 0")
    
    def drawMenu(self, screen):
        self.draw_rounded_rect(screen)
        text_surf = self.title.render(self.title_text, True, base3)
        text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.centery - (self.menu_height // 2) + self.title_text_size))
        #text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.centery))
        #print("in ", self, " 's draw call: ")
        #print("\t BUTTON SIZE: ", len(self.child_Dictionary[childType.BUTTON]))
        #print("\t MENU SIZE: ", len(self.child_Dictionary[childType.MENU]))
        #print("\t TEXT SIZE: ", len(self.child_Dictionary[childType.TEXT]))
        for i in range(len(self.child_Dictionary[childType.BUTTON])):
            self.child_Dictionary[childType.BUTTON][i].draw_button(screen)
        for i in range(len(self.child_Dictionary[childType.MENU])):
            self.child_Dictionary[childType.MENU][i].drawMenu(screen)
        for i in range(len(self.child_Dictionary[childType.TEXT])):
            self.child_Dictionary[childType.TEXT][i].drawWidget(screen)
        screen.blit(text_surf, text_rect)

    def changeTextSize(self, inSize):
        self.title = pygame.font.Font(None, inSize)
        self.title_text_size = inSize

    def resizeBox(self, width, height):
        self.rect = pygame.Rect(self.ScreenCoords[0], self.ScreenCoords[1], width, height)
        self.menu_height = height
        self.menu_width = width

    def moveBox(self, inPosition):
        self.rect.centerx = inPosition[0]
        self.rect.centery = inPosition[1]

    def reOrientButtons(self, inPosition, width, height):
        y_offset = 0
        print(width)
        for i in range(len(self.child_Dictionary[childType.BUTTON])):
            print(self.child_Dictionary[childType.BUTTON][i].button_text_size // 2)
            self.child_Dictionary[childType.BUTTON][i].changeTextSize(self.child_Dictionary[childType.BUTTON][i].button_text_size - (self.child_Dictionary[childType.BUTTON][i].button_text_size // 4))
            self.child_Dictionary[childType.BUTTON][i].resizeBox(width - width // 4, height)
            self.child_Dictionary[childType.BUTTON][i].moveBox((inPosition[0], inPosition[1] + y_offset))
            y_offset += height + 10
    #add fading effect
    

    #TODO change this functionality to add child components rather than just buttons
    #TODO alter functionality to space components based on landscape vs portrait
    def addChildComponent(self, inComponent):
        x_offset = self.ScreenCoords[0]
        width = self.menu_width //2
        height = width // 2
        y_offset = self.ScreenCoords[1] - self.menu_height // 2 + height + 50
        #TODO Might depricate this, this function is doing too much
        if len(self.child_Dictionary[childType.BUTTON]) > 0 and (isinstance(inComponent, menu) or isinstance(inComponent, textWidget)):
            self.reOrientButtons((x_offset - width // 2, y_offset), width, height)
            #adjust the offset to be the new half on the right side of the screen
            x_offset = x_offset + self.menu_width // 4
            
        if isinstance(inComponent, button):
            if len(self.child_Dictionary[childType.BUTTON]) <= 0:
                inComponent.resizeBox(width, height)
                inComponent.moveBox((x_offset, y_offset))
            else:
                for i in range(len(self.child_Dictionary[childType.BUTTON])):
                    y_offset += 15 + height
                inComponent.resizeBox(width, height)
                inComponent.moveBox((x_offset, y_offset))
            self.child_Dictionary[childType.BUTTON].append(inComponent)
        elif isinstance(inComponent, menu):
            for i in range(len(self.child_Dictionary[childType.MENU])):
                y_offset += 15 + height
            #TODO make changing of text size happen in the respective class
            inComponent.changeTextSize(height // 4)
            inComponent.resizeBox(width - 25, height)
            inComponent.moveBox((x_offset, y_offset))
            self.child_Dictionary[childType.MENU].append(inComponent)
        elif isinstance(inComponent, textWidget):
            for i in range(len(self.child_Dictionary[childType.MENU])):
                y_offset += 15 + height
            inComponent.changeTextSize(height // 4)
            inComponent.resizeBox(width - 25, height)
            inComponent.moveBox((x_offset, y_offset))
            self.child_Dictionary[childType.TEXT].append(inComponent)

    def listen_for_buttons(self, event):
        selfSet = False
        for i in range(len(self.child_Dictionary[childType.BUTTON])):
            if self.child_Dictionary[childType.BUTTON][i].isClicked(event):
                selfSet = i
        return selfSet
    def __init__(self, position : tuple[int, ...], width = 200, height = 200, titleText = "place holder"):
        self.ScreenCoords = position
        self.menu_width = width
        self.menu_height = height
        self.rect = pygame.Rect(self.ScreenCoords[0], self.ScreenCoords[1], self.menu_width, self.menu_height)
        self.title_text = titleText
        self.title = pygame.font.Font(None, self.title_text_size)
        self.child_Dictionary = {}
        #initialize our child dictionary to have empty arrays
        self.child_Dictionary[childType.BUTTON] = []
        self.child_Dictionary[childType.MENU] = []
        self.child_Dictionary[childType.TEXT] = []
        if width > 100:
            self.changeTextSize(width // 10)
        else:
            self.changeTextSize(width // 4)
        self.resizeBox(width, height)
        self.moveBox(position)
