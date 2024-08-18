import pygame
import sys
import numpy as np
from databaseSetup import setup_database_and_execute_scripts
from colors import *
import slideBarWidget
import configMenu as cm
from databaseConnection import databaseConnection
from checkBoxWidget import checkBoxWidget
from textWidget import textWidget


multiCheck = checkBoxWidget((850, 380),50, 50)
multiText = textWidget((1030, 515), 300, 300, "Host Online Game")
multiText.textCol = base3
multiText.changeTextSize(40)

def runSetupMenu(database):

    #Default Categories
    defaultCategories = [{'name': 'Astronomy', 'color': (255, 0, 76), 'askedQuestions': []}, {'name': 'Biology', 'color': (255, 236, 38), 'askedQuestions': []}, {'name': 'Chemistry', 'color': (41, 173, 255), 'askedQuestions': []}, {'name': 'Animals', 'color': (0, 228, 53), 'askedQuestions': []}]

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

    # global datatypes
    selected_categories = {}
    game_setup_data = {}
    category_selection_open = False

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
        nonlocal selected_categories
        selected_categories = {}
        categories = database.getCategories()
        colors = [match_red, match_green, match_blue, match_yellow]
        color_index = {category[1]: 0 for category in categories}
        selecting = True
        while selecting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for i, (rect, category) in enumerate(category_buttons):
                            category_name = category[1]
                            checkmark_rect = checkmark_buttons[i]
                            if checkmark_rect.collidepoint(event.pos):
                                # Toggle selection
                                if category_name not in selected_categories:
                                    if len(selected_categories) < 4:
                                        selected_categories[category_name] = colors[color_index[category_name]]
                                else:
                                    selected_categories.pop(category_name)

                        # Handle color change arrows
                        for i, (left_rect, right_rect, category_name) in enumerate(color_arrows):
                            if category_name in selected_categories:
                                if left_rect.collidepoint(event.pos):
                                    color_index[category_name] = (color_index[category_name] - 1) % len(colors)
                                    selected_categories[category_name] = colors[color_index[category_name]]
                                elif right_rect.collidepoint(event.pos):
                                    color_index[category_name] = (color_index[category_name] + 1) % len(colors)
                                    selected_categories[category_name] = colors[color_index[category_name]]

            # Draw background
            screen.blit(background_image, (0, 0))

            # Draw category buttons and checkmarks
            category_buttons = []
            checkmark_buttons = []
            color_arrows = []
            for i, category in enumerate(categories):
                button_rect = pygame.Rect(800, 100 + i * 60, 300, 50)
                category_name = category[1]
                button_color = selected_categories.get(category_name, base2)
                pygame.draw.rect(screen, button_color, button_rect)
                text_surf = font.render(category_name, True, black)
                text_rect = text_surf.get_rect(center=button_rect.center)
                screen.blit(text_surf, text_rect)
                category_buttons.append((button_rect, category))

                # Checkmark button
                checkmark_rect = pygame.Rect(760, 100 + i * 60, 30, 50)
                checkmark_buttons.append(checkmark_rect)
                checkmark_color = std_green if category_name in selected_categories else std_red
                pygame.draw.rect(screen, checkmark_color, checkmark_rect)

                # Arrows for changing colors
                if category_name in selected_categories:
                    left_arrow_rect = pygame.Rect(1110, 100 + i * 60, 30, 50)
                    right_arrow_rect = pygame.Rect(1150, 100 + i * 60, 30, 50)
                    pygame.draw.polygon(screen, white, [(1110, 125 + i * 60), (1130, 110 + i * 60), (1130, 140 + i * 60)])
                    pygame.draw.polygon(screen, white, [(1150, 125 + i * 60), (1130, 110 + i * 60), (1130, 140 + i * 60)])
                    color_arrows.append((left_arrow_rect, right_arrow_rect, category_name))

            # Check if all selected categories have unique colors
            unique_colors = len(set(selected_categories.values())) == len(selected_categories)

            # Draw Done button
            if len(selected_categories) == 4 and unique_colors:
                done_button_rect = pygame.Rect(800, 600, 300, 50)
                pygame.draw.rect(screen, std_green, done_button_rect)
                done_text_surf = font.render("Done", True, black)
                done_text_rect = done_text_surf.get_rect(center=done_button_rect.center)
                screen.blit(done_text_surf, done_text_rect)
                if event.type == pygame.MOUSEBUTTONDOWN and done_button_rect.collidepoint(event.pos):
                    selecting = False

            pygame.display.flip()

        return selected_categories
    
    def openCategorySelection():
        nonlocal category_selection_open
        category_selection_open = True
        categorySelection()
        category_selection_open = False

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
            self.color_list = [match_red, match_green, match_blue, match_yellow]
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
                    print(f"{self.text} button clicked!")
                    if self.action:
                        result = self.action()
                        print(f"Action result: {result}")
                        return result
            return None

        def setup_player(self):
            colors = [match_red, match_green, match_blue, match_yellow]
            current_name = self.text
            current_color = self.color
            color_buttons = [pygame.Rect(750 + i * 120, 400, 100, 100) for i in range(len(colors))]
            name_input_box = pygame.Rect(775, 275, 400, 50)
            active = False
            new_name = current_name

            setup = True
            #why are there two event queues
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
                                self.highlighted_color = [min(255, c + 30) for c in self.color]
                                self.shadow_color = [max(0, c - 30) for c in self.color]
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

                pygame.display.flip()
                clock.tick(60)

    def checkUniqueColors(buttons):
        # Extract the colors from the buttons (excluding the non-player buttons)
        player_colors = [button.color for button in buttons[:number_of_players]]
        # Ensure all colors are unique
        return len(set(player_colors)) == len(player_colors)


    button_positions = [
        (850, 50), (1000, 50),
        (850, 200), (1000, 200)
    ]
    
    buttons = []
    player_buttons = []
    colors = [match_red, match_green, match_blue, match_yellow]

    # Add the player buttons
    for i in range(number_of_players):
        button = (Button(f"Player{i+1}", *button_positions[i], 150, 150, colors[i]))
        button.action = button.setup_player
        player_buttons.append(button)


    def collectSetupData():
        game_setup_data = {
            'number_of_players': number_of_players,
            'players': [
                {
                    'name': button.text,
                    'color': button.color
                }
                for button in player_buttons
            ],
            'categories': [
                {
                    'name': category,
                    'color': color,
                    'askedQuestions': []
                }
                for category, color in selected_categories.items()
            ]
        }

        if len(game_setup_data['categories']) < 4:
            game_setup_data['categories'] = defaultCategories
            
        return game_setup_data

    def exitSetupMenu():
        nonlocal game_setup_data
        game_setup_data = collectSetupData()
        return "setupDone"
    
     # Add the non-player buttons
    database = databaseConnection(dbname='trivialCompute', user='postgres', password='postgres')
    categoriesButton = Button("Categories", 840, 475, 320, 75, std_magenta, action=openCategorySelection)
    submitButton = Button("Begin Game!", 840, 575, 320, 75, std_green, action=exitSetupMenu)

    buttons.extend(player_buttons)
    buttons.append(categoriesButton)
    buttons.append(submitButton)

    running = True
    while running:
        # Draw background image
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            rbs = multiCheck.listen(event)
            if rbs:
                configModule.online = True
                configModule.host = True
            if event.type == pygame.QUIT:
                running = False
                return "exit"
            for button in buttons:
                result = button.check_click(event)
                if result == "setupDone":
                    running = False
                    break
                elif result:
                    return result
        
        for button in buttons:
            button.draw(screen)
        multiCheck.drawWidget(screen)
        multiText.drawWidget(screen)
        uniqueColors = checkUniqueColors(buttons)
        if uniqueColors:
            submitButton.color = std_green #Active state
            submitButton.text = "Begin Game!"
            submitButton.action = exitSetupMenu
        else:
            submitButton.color = std_red #Inactive state
            submitButton.text = "Colors must be unique"
            submitButton.action = None
        submitButton.highlighted_color = [min(255, c + 30) for c in submitButton.color]
        submitButton.shadow_color = [max(0, c - 30) for c in submitButton.color]

        pygame.display.flip()
    return game_setup_data