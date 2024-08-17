import pygame
from colors import *
from player import player


# Initialize Pygame
# pygame.init()

# Function to display the Game Over screen
def displayGameOver(screen, playerList, categories, winner):
    # Screen settings
    screen_width = 1280
    screen_height = 720
    button_height = 50
    button_width = 150

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Over")

    # Fonts
    cat_font = pygame.font.Font(None, 20)
    font = pygame.font.Font(None, 30)
    play_font = pygame.font.Font(None, 40)
    title_font = pygame.font.Font(None, 60)

    # Button class
    class Button:
        def __init__(self, text, x, y, width, height, color, action=None):
            self.text = text
            self.rect = pygame.Rect(x, y, width, height)
            self.color = color
            self.action = action
            self.highlighted_color = [min(255, c + 30) for c in color]
            self.shadow_color = [max(0, c - 30) for c in color]
            self.disabled = False

        def draw(self, screen):
            shadow_rect = self.rect.copy()
            shadow_rect.topleft = (self.rect.x + 2, self.rect.y + 2)
            pygame.draw.rect(screen, self.shadow_color, shadow_rect)
            pygame.draw.rect(screen, self.highlighted_color, self.rect)
            pygame.draw.rect(screen, self.color, self.rect.inflate(-4, -4))

            text_surf = font.render(self.text, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)

        def check_click(self, event):
            if self.disabled:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    if self.action:
                        self.disabled = True
                        return self.action()
            return None

    # Create a sliding dialogue box
    dialogue_box_height = screen_height
    dialogue_box = pygame.Surface((screen_width, dialogue_box_height))
    dialogue_box.fill((0, 0, 0))
    pygame.draw.rect(dialogue_box, white, dialogue_box.get_rect(), 2)

    # Toggle title color variables
    title_color = white  # Start with white
    toggle_time = 0.5  # Time in seconds to toggle color
    last_toggle = pygame.time.get_ticks()  # Track last toggle time

    # Render title
    title = winner.playerName + " Wins!"

    # Display player results
    for i in range(len(playerList)):
        player_text = f"{playerList[i].playerName}:"
        player_surf = play_font.render(player_text, True, playerList[i].circle_color)
        if i == 0 or i == 2:
            x = 250
        else:
            x = 700
        
        if i == 0 or i == 1:
            y = 150
        else:
            y = 350

        player_rect = player_surf.get_rect(topleft=(x, y))
        dialogue_box.blit(player_surf, player_rect)

        for j in range(len(categories)):
            res = playerList[i].playerReportCard[categories[j]['color']]
            cat_text = f"{categories[j]['name']}: {res[0]} / {res[1]}"
            if res[1] != 0:
                cat_text += " (" + str(float(res[0]) / res[1] * 100) + "%)"
            cat_surf = font.render(cat_text, True, white)
            cat_rect = cat_surf.get_rect(topleft=(x+20, y + 10 + (j + 1) * 30))
            dialogue_box.blit(cat_surf, cat_rect)

    # Render "Exit" button
    exit_button = Button("Exit", (screen_width // 2 - button_width // 2), screen_height - button_height - 50, button_width, button_height, (100, 200, 250))

    # Animate dialogue box sliding up
    y_position = screen_height
    while y_position > screen_height - dialogue_box_height:
        screen.fill((0, 0, 0))
        screen.blit(dialogue_box, (0, y_position))
        pygame.display.flip()
        y_position -= 2

    # Keep the dialogue box up until "Exit" is clicked
    while True:
        screen.fill((0, 0, 0))
        screen.blit(dialogue_box, (0, screen_height - dialogue_box_height))

        # Toggle the title color
        current_time = pygame.time.get_ticks()
        if (current_time - last_toggle) / 1000 >= toggle_time:
            title_color = winner.circle_color if title_color == white else white
            last_toggle = current_time

        # Draw the title with the toggled color
        title_surf = title_font.render(title, True, title_color)
        title_rect = title_surf.get_rect(center=(screen_width // 2, 50))
        screen.blit(title_surf, title_rect)

        exit_button.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if exit_button.rect.collidepoint(event.pos):
                    return "exit"
