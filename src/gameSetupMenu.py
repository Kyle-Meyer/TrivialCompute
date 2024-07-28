import pygame
import sys
import numpy as np
from databaseSetup import setup_database_and_execute_scripts
from colors import *
import slideBarWidget
import configMenu as cm
from databaseConnection import databaseConnection


def runSetupMenu(database):

    #Screen Settings
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Trivial Compute")
    # Load background image
    background_image = pygame.image.load("background.jpg")
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    # Fonts
    font = pygame.font.Font(None, 40) 

    # Text Input Box Setup
    input_box = pygame.Rect(screen_width - 350, screen_height / 2 - 30, 140, 30)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    clock = pygame.time.Clock()

    def draw_text(surf, text, font, color, pos):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = pos
        surf.blit(textobj, textrect)
    
    def categorySelection():
        categories = database.getCategories()
        selected_categories = []

        selecting = True
        while selecting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i, (rect, category) in enumerate(category_buttons):
                            if rect.collidepoint(event.pos):
                                if category not in selected_categories:
                                    if len(selected_categories) < 4:
                                        selected_categories.append(category[1])
                                else:
                                    selected_categories.remove(category[1])

                                # # Update button color
                                button_colors[i] = (0, 255, 0) if category in selected_categories else (255, 0, 0)

            # Draw background
            screen.blit(background_image, (0, 0))

            # Draw category buttons
            category_buttons = []
            button_colors = []
            for i, category in enumerate(categories):
                button_rect = pygame.Rect(800, 100 + i * 60, 300, 50)
                button_color = (0, 255, 0) if category[1] in selected_categories else (255, 0, 0)
                pygame.draw.rect(screen, button_color, button_rect)
                text_surf = font.render(category[1], True, black)
                text_rect = text_surf.get_rect(center=button_rect.center)
                screen.blit(text_surf, text_rect)
                category_buttons.append((button_rect, category))
                button_colors.append(button_color)

            pygame.display.flip()
            
            if len(selected_categories) == 4:
                selecting = False

        return selected_categories

    
    # Prompt for number of players
    number_of_players = 0
    while number_of_players not in range(1, 5):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "exit"
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        try:
                            number_of_players = int(text)
                            if number_of_players in range(1, 5):
                                active = False
                                text = ''
                            else:
                                text = ''
                        except ValueError:
                            text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

        screen.blit(background_image, (0, 0))
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)
        draw_text(screen, 'Enter number of players (1-4):', font, pygame.Color('white'), (screen_width - 300, screen_height / 2 - 60))
        pygame.display.flip()
        clock.tick(30)

    class Button:
        def __init__(self, text, x, y, width, height, color, action=None):
            self.text = text
            self.rect = pygame.Rect(x, y, width, height)
            self.color_list = [(255, 0 , 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
            self.color_index = 0
            self.color = color
            self.action = action
            self.highlighted_color = [min(255, c + 30) for c in color]
            self.shadow_color = [max(0, c - 30) for c in color]

        def draw(self, screen):
            # Draw shadow
            shadow_rect = self.rect.copy()
            shadow_rect.topleft = (self.rect.x + 2, self.rect.y + 2)
            pygame.draw.rect(screen, self.shadow_color, shadow_rect)

            # Draw main button
            pygame.draw.rect(screen, self.highlighted_color, self.rect)
            pygame.draw.rect(screen, self.color, self.rect.inflate(-4, -4))

            # Draw text
            text_surf = font.render(self.text, True, black)
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)
        
        def getColor(self):
            return self.color

        def check_click(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    if self.action:
                        self.action()
            return None

        def setup_player(self):
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
            current_name = self.text
            current_color = self.color
            color_buttons = [pygame.Rect(750 + i * 120, 400, 100, 100) for i in range(len(colors))]
            name_input_box = pygame.Rect(775, 275, 400, 50)
            active = False
            new_name = current_name

            setup = True
            while setup:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if name_input_box.collidepoint(event.pos):
                            active = not active
                        else:
                            active = False

                        # Check if a color button is clicked
                        for i, rect in enumerate(color_buttons):
                            if rect.collidepoint(event.pos):
                                current_color = colors[i]

                    elif event.type == pygame.KEYDOWN:
                        if active:
                            if event.key == pygame.K_RETURN:
                                self.text = new_name
                                self.color = current_color
                                setup = False
                            elif event.key == pygame.K_BACKSPACE:
                                new_name = new_name[:-1]
                            else:
                                new_name += event.unicode

                screen.blit(background_image, (0, 0))

                # Draw input box for the player's name
                pygame.draw.rect(screen, pygame.Color('white'), name_input_box, 2)
                name_text_surface = font.render(new_name, True, pygame.Color('white'))
                screen.blit(name_text_surface, (name_input_box.x + 5, name_input_box.y + 5))

                # Draw color selection buttons
                for i, rect in enumerate(color_buttons):
                    pygame.draw.rect(screen, colors[i], rect)
                    if colors[i] == current_color:
                        pygame.draw.rect(screen, pygame.Color('white'), rect, 2)

                draw_text(screen, 'Enter Player Name:', font, pygame.Color('white'), (900, 250))
                draw_text(screen, 'Select Player Color:', font, pygame.Color('white'), (900, 350))
                setupDoneButton = Button('Done', 950, 500, 300, 75, pygame.Color('red'), pygame.display.flip())
                pygame.display.flip()
                clock.tick(30)


    button_positions = [
        (850, 100), (1000, 100),
        (850, 250), (1000, 250)
    ]

    buttons = []
    colors = [(255, 0 , 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

    for i in range(number_of_players):
        button = (Button(f"Player{i+1}", *button_positions[i], 150, 150, colors[i]))
        button.action = button.setup_player
        buttons.append(button)

    # TODO: Need to figure out how to get number of players
    # (255, 0 , 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)
    # player1Button = Button("Player1" , 850, 100, 150, 150, (255, 0, 0))
    # player2Button = Button("Player2", 1000, 100, 150, 150, (0, 255, 0))
    # player3Button = Button("Player3", 850, -50, 150, 150, (0, 0, 255))
    # player4Button = Button("Player4", 1000, -50, 150, 150, (255, 255, 0))
    database = databaseConnection(dbname='trivialCompute', user='postgres', password='postgres')
    categoriesButton = Button("Categories", 850, 475, 300, 75, color=pygame.Color('magenta'), action=categorySelection)
    submitButton = Button("Done", 850, 575, 300, 75, color=pygame.Color('red'), action=pygame.display.flip)

    #playerButtons = [player1Button, player2Button, player3Button, player4Button]
    buttons.append(categoriesButton)
    buttons.append(submitButton) #, categoriesButton, submitButton]

    

    running = True
    while running:
        # Draw background image
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "exit"
            for button in buttons:
                result = button.check_click(event)
                if result is not None:
                    return result

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()

    return "exit"