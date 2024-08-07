import pygame
import random
import time
import numpy as np
from colors import *
import configMenu as cm

# Initialize Pygame
#pygame.init()

# Function to run the start menu
def run_order_menu(setupInfo):
    print(setupInfo)
    # Screen settings
    screen_width = 1280
    screen_height = 720
    button_height = 75
    button_width = 300

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Determine Player Order")

    # Fonts
    font = pygame.font.Font(None, 40)
    result_font = pygame.font.Font(None, 50)
    order_font = pygame.font.Font(None, 50)
    title_font = pygame.font.Font(None, 60)
    button_font = pygame.font.Font(None, 50)

    # Title text and position
    titleText = "Each Player, Click to Roll!"
    position = (screen_width // 2, screen_height // 8)
    height = 100

    # Button class
    class Button:
        def __init__(self, text, x, y, width, height, color, action=None):
            self.text = text
            self.rect = pygame.Rect(x, y, width, height)
            self.color = color
            self.action = action
            self.highlighted_color = [min(255, c + 30) for c in color]
            self.shadow_color = [max(0, c - 30) for c in color]
            self.result = None  # Store the result of the dice roll
            self.disabled = False  # Disable button after roll

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

            # Draw result if available
            if self.result is not None:
                self.draw_result_box(screen)

        def draw_result_box(self, screen):
            # Draw a rounded rectangle for the result
            result_box_rect = pygame.Rect(self.rect.x, self.rect.y + 100, button_width, 50)
            pygame.draw.rect(screen, white, result_box_rect, border_radius=10)
            pygame.draw.rect(screen, black, result_box_rect.inflate(-4, -4), border_radius=10)

            # Draw result text
            result_text = f"Roll: {self.result}"
            result_surf = result_font.render(result_text, True, white)
            result_rect = result_surf.get_rect(center=result_box_rect.center)
            screen.blit(result_surf, result_rect)

        def check_click(self, event):
            if self.disabled:
                return None  # Do nothing if the button is disabled

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    if self.action:
                        self.disabled = True  # Disable button after first click
                        return self.action()
            return None

    # Dice roll animation
    def roll_dice_animation():
        roll_result = random.randint(1, 6)  # Final dice roll result
        for _ in range(30):  # Number of frames for the animation
            # Cycle through random numbers
            current_roll = random.randint(1, 6)
            yield current_roll  # Generator to yield each frame's roll
            time.sleep(0.04)  # Control the speed of the animation

        yield roll_result  # Final result

    # Button actions
    def roll_dice(player_index):
        print(f"Player {player_index + 1} Button Pressed")
        for roll in roll_dice_animation():
            buttons[player_index].result = roll
            screen.fill(null)
            
            # Draw title
            draw_title(screen)

            for button in buttons:
                button.draw(screen)
            pygame.display.flip()
        rolled[player_index] = True
        return f"player{player_index + 1}"

    # Create buttons with actions
    def create_buttons(number_of_players):
        button_positions = []
        actions = []

        if number_of_players == 2:
            button_positions = [((screen_width//4) - (button_width//2), (screen_height//3) - (button_height//2)),
                                (3*(screen_width//4) - (button_width//2), (screen_height//3) - (button_height//2))]
            actions = [lambda: roll_dice(0), lambda: roll_dice(1)]

        elif number_of_players == 3:
            button_positions = [((screen_width//6) - (button_width//2), (screen_height//3) - (button_height//2)),
                                (3*(screen_width//6) - (button_width//2), (screen_height//3) - (button_height//2)),
                                (5*(screen_width//6) - (button_width//2), (screen_height//3) - (button_height//2))]
            actions = [lambda: roll_dice(0), lambda: roll_dice(1), lambda: roll_dice(2)]

        elif number_of_players == 4:
            button_positions = [((screen_width//4) - (button_width//2), (screen_height//8 + screen_height//6) - (button_height//2)),
                                (3*(screen_width//4) - (button_width//2), (screen_height//8 + screen_height//6) - (button_height//2)),
                                ((screen_width//4) - (button_width//2), (screen_height//2 + screen_height//6) - (button_height//2)),
                                (3*(screen_width//4) - (button_width//2), (screen_height//2 + screen_height//6) - (button_height//2))]
            actions = [lambda: roll_dice(0), lambda: roll_dice(1), lambda: roll_dice(2), lambda: roll_dice(3)]

        buttons = []
        for i in range(number_of_players):
            player_name = setupInfo['players'][i]['name']
            player_color = setupInfo['players'][i]['color']
            button = Button(player_name, button_positions[i][0], button_positions[i][1],
                            button_width, button_height, player_color, actions[i])
            buttons.append(button)

        return buttons

    # Create buttons based on the number of players
    buttons = create_buttons(setupInfo['number_of_players'])

    # Initialize rolled list
    rolled = [False] * setupInfo['number_of_players']

    # Function to determine player order
    def determine_player_order():
        # Gather player rolls and sort
        player_rolls = [(i, button.result) for i, button in enumerate(buttons)]
        player_rolls.sort(key=lambda x: (-x[1], random.random()))  # Sort by roll descending, randomize for ties
        return player_rolls

    # Function to display player order
    def display_player_order(order):
        order_lines = [f"{setupInfo['players'][i]['name']} ({roll})" for i, roll in order]

        # Create a sliding dialogue box
        dialogue_box_height = screen_height #500 + len(order_lines) * 60  # Adjust height based on number of lines
        dialogue_box = pygame.Surface((screen_width, dialogue_box_height))
        dialogue_box.fill(black)
        pygame.draw.rect(dialogue_box, white, dialogue_box.get_rect(), 2)

        # Render title
        title_surf = title_font.render("Player Turn Order", True, white)
        title_rect = title_surf.get_rect(center=(screen_width // 2, 100))
        dialogue_box.blit(title_surf, title_rect)

        # Render order text with spacing
        y_offset = 200
        for order_line in order_lines:
            order_surf = order_font.render(order_line, True, white)
            order_rect = order_surf.get_rect(center=(screen_width // 2, y_offset))
            dialogue_box.blit(order_surf, order_rect)
            y_offset += 60  # Increment y offset for next line

        # Render "Let's Get Started!" button
        lets_go_text = "Let's Get Started!"
        lets_go_button = Button(lets_go_text, (screen_width // 2 - button_width // 2), screen_height - button_height - 100, button_width, button_height, (100, 200, 250))

        # Animate dialogue box sliding up
        y_position = screen_height
        while y_position > screen_height - dialogue_box_height:
            screen.fill(null)
            screen.blit(dialogue_box, (0, y_position))
            pygame.display.flip()
            y_position -= 2  # Slide speed

        # Keep the dialogue box up until "Let's Get Started!" is clicked
        while True:
            screen.fill(null)
            screen.blit(dialogue_box, (0, screen_height - dialogue_box_height))
            lets_go_button.draw(screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "exit"
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if lets_go_button.rect.collidepoint(event.pos):
                        return "game_start"  # Continue to the game

    # Draw the title
    def draw_title(screen):
        title_surf = font.render(titleText, True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(position[0], position[1] - (height // 2) + 50))
        screen.blit(title_surf, title_rect)

    # Main loop
    running = True
    while running:
        screen.fill(null)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return {}

            for button in buttons:
                result = button.check_click(event)
                if result is not None:
                    if all(rolled):
                        player_order = determine_player_order()
                        newSetupInfo = {
                            'number_of_players': setupInfo['number_of_players'],
                            'players': [setupInfo['players'][i] for i, _ in player_order],
                            'categories': setupInfo['categories']
                        }
                        #pause for 2 seconds
                        time.sleep(2)
                        display_player_order(player_order)  # Show player order and proceed
                        return newSetupInfo

        # Draw title
        draw_title(screen)

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()

    return newSetupInfo

# Example setupInfo for testing
setupInfo = {
    'number_of_players': 3,
    'players': [
        {'name': 'Mike', 'color': (255, 0, 0)},
        {'name': 'Ziyun', 'color': (0, 0, 255)},
        {'name': 'Noah', 'color': (0, 255, 0)}#,
        #{'name': 'Player 4', 'color': (255, 255, 0)}
    ]
}

# Run the menu
#run_order_menu(setupInfo)
