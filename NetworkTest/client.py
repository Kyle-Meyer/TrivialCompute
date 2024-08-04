import pygame
import sys
from connector import connector

# Initialize Pygame
pygame.init()

# Constants for the screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60  # Frames per second

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Draggable Squares")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Squares details
square1 = pygame.Rect(100, 100, 60, 60)
square2 = pygame.Rect(300, 300, 60, 60)
dragging = [False, False]  # Drag states for square1 and square2

# Clock for controlling the frame rate
clock = pygame.time.Clock()

def check_collision(pos, rect):
    if rect.collidepoint(pos):
        return True
    return False
def convert_to_int(strin : str):
    strin = strin.split(",")
    return int(strin[0]), int(strin[1])

def packetize_pos(inTuple):
    return str(inTuple[0]) + "," + str(inTuple[1])

def main():
    running = True
    global dragging
    print("making connector...")
    n = connector()
    #n.send(packetize_pos((square1.x, square1.y)))
    #n.send(packetize_pos((square2.x, square2.y)))
    p1 = n.getObj()
    print("p1 = ", p1)
    while running:
        #send to the server and get something back
        #p2 = n.send(p1)
        #print("huh" , n.getPos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if check_collision(event.pos, p1.rect):
                        print("CLICKED")
                        p1.dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    p1.dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if p1.dragging:
                    p1.rect.x = event.pos[0] - p1.rect.width // 2
                    p1.rect.y = event.pos[1] - p1.rect.height // 2
                    

        # Fill the screen with white
        screen.fill(WHITE)

        # Draw the squares
        pygame.draw.rect(screen, RED, p1.rect)
        #pygame.draw.rect(screen, GREEN, p2.rect)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

# Quit Pygame
main()
pygame.quit()
sys.exit()