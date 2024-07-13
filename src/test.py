import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants for the screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 300
FPS = 60  # Frames per second

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Checkbox Example")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Checkbox details
checkbox_rect = pygame.Rect(150, 100, 40, 40)  # x, y, width, height
checkbox_checked = False
outer_rect = pygame.Rect(160, 110, 50, 50)
checkbox_rect.center = outer_rect.center
# Clock for controlling the frame rate
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Check if the mouse click is within the checkbox rectangle
                if checkbox_rect.collidepoint(event.pos):
                    checkbox_checked = not checkbox_checked

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the checkbox
    pygame.draw.rect(screen, BLACK, outer_rect, 2)  # Draw the border of the checkbox
    
    if checkbox_checked:
        pygame.draw.rect(screen, BLUE, checkbox_rect)  # Fill the checkbox if checked
        pygame.draw.rect(screen, WHITE, checkbox_rect, 2)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()