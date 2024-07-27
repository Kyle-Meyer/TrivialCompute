import pygame
import sys
import numpy as np
from databaseSetup import setup_database_and_execute_scripts
from colors import *
import configMenu as cm

# Function to run the start menu
def run_start_menu():
    # Initialize Pygame
#    pygame.init()

    # Screen settings
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Trivial Compute")

    # Load background image
    background_image = pygame.image.load("background.jpg")
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    # Fonts
    font = pygame.font.Font(None, 40)

    # Button class
    class Button:
        def __init__(self, text, x, y, width, height, color, action=None):
            self.text = text
            self.rect = pygame.Rect(x, y, width, height)
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

        def check_click(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    if self.action:
                        return self.action()
            return None

    # Button actions
    def start_game():
        print("Start New Game button clicked")
        return "start"

    def restore_last_game():
        print("Restore Last Game button clicked")
        return "restore"

    def exit_game():
        print("Exit Game button clicked")
        return "exit"

    def config_game():
        print("Configuraiton button clicked")
        cm.config_menu()


    # Create buttons
    config_button = Button("Configure", 850, 100, 300, 75, (41,173,255), config_game)
    start_button = Button("Start New Game", 850, 200, 300, 75, (0,228,53), start_game)
    restore_button = Button("Restore Last Game", 850, 300, 300, 75, (0,228,53), restore_last_game)
    exit_button = Button("Exit", 850, 400, 300, 75, (255,0,76), exit_game)


    buttons = [config_button, start_button, restore_button, exit_button]

    # Main loop
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
