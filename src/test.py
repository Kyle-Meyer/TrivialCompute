import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Semi-Transparent Rectangle with Text")

# Colors
background_color = (255, 255, 255)  # White background
rectangle_color = (0, 0, 255)  # Blue rectangle
text_color = (255, 255, 255)  # White text

# Rectangle settings
rect_width, rect_height = 400, 200
rectangle_surface = pygame.Surface((rect_width, rect_height))
rectangle_surface.set_alpha(10)  # Set transparency to 50% (0-255)
rectangle_surface.fill(rectangle_color)

# Font settings
font = pygame.font.Font(None, 36)
text = "Hello, Pygame!"
text_surface = font.render(text, True, text_color)
text_rect = text_surface.get_rect(center=(rect_width // 2, rect_height // 2))

# Blit the text onto the rectangle surface
rectangle_surface.blit(text_surface, text_rect)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill(background_color)

    # Draw the semi-transparent rectangle with text on the screen
    rect_x = (width - rect_width) // 2  # Center the rectangle
    rect_y = (height - rect_height) // 2
    screen.blit(rectangle_surface, (rect_x, rect_y))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()