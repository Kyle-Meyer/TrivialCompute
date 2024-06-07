import array
import math
import sys
import cairo
import pygame
from pygame.locals import *
import rsvg
import random

def pygameDemo():
    WIDTH = 800
    HEIGHT = 600

    black = (0, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    red = (255, 0, 0)


    #globals are bad, avoid them when we can
    run = True
    moving = False
    color = green

    #except for these, you could make an argument that this is acceptable since there will only ever be One screen and 4 players
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    player = pygame.Rect((300, 250, 50, 50))

    bounding_box = pygame.Rect(300, 200, 200, 200)

    #detect if we are in bounding box
    def is_inside_bounding_box(point_or_rect):
        """ Check if a point or another rectangle is inside the bounding box. """
        if isinstance(point_or_rect, pygame.Rect):
            return bounding_box.colliderect(point_or_rect)
        elif isinstance(point_or_rect, tuple):
            return bounding_box.collidepoint(point_or_rect)
        return False

    while run:
        
        screen.fill((0,0,0))
        #draw calls
        pygame.draw.rect(screen, (255, 0, 0), player)
        pygame.draw.rect(screen, color, bounding_box, 7)

        for event in pygame.event.get():
            if event.type == QUIT:
                run= False
    
            # Making player move
            elif event.type == MOUSEBUTTONDOWN:
                if player.collidepoint(event.pos):
                    moving = True
            elif event.type == MOUSEBUTTONUP:
                moving = False
            #player moves while mouse is held
            elif event.type == MOUSEMOTION and moving:
                player.move_ip(event.rel)
            # Test a moving point (mouse position)
        #update the bounding box
        mouse_pos = pygame.mouse.get_pos()
        if is_inside_bounding_box(player.center):
            color = red
        elif is_inside_bounding_box(mouse_pos):
            color = blue;
        else:
            color = green
        
        pygame.display.update()
        

    pygame.quit()


# Parameters
rows, cols = 10, 10  # Dimensions of the grid
steps = 200  # Number of steps to move
def create_grid(rows, cols):
    """ Create a 2D grid represented as a list of lists """
    return [['.' for _ in range(cols)] for _ in range(rows)]

def print_grid(grid):
    """ Print the grid """
    for row in grid:
        print(' '.join(row))
    print()

def forwardBoardScan(grid, x, y):
    count = 0
    if x-1 >= 0 and grid[x-1][y] == "X":  # Can move left
        count += 1
    if x+1 < rows and grid[x+1][y] == "X":  # Can move right
        count += 1
    if y-1 >= 0 and grid[x][y-1] == "X":  # Can move up
        count += 1
    if y+1 < cols and grid[x][y+1] == "X":  # Can move down
        count += 1
    if count >= 2:
        return False
    return True
def valid_moves(grid, x, y):
    """ Generate valid movements within grid boundaries """
    moves = []
    if x-1 >= 0 and grid[x-1][y] == "." and forwardBoardScan(grid, x-1, y):  # Can move left
        moves.append((x - 1, y))
    if x+1 < rows and grid[x+1][y] == "." and forwardBoardScan(grid, x+1, y):  # Can move right
        moves.append((x + 1, y))
    if y-1 >= 0 and grid[x][y-1] == "." and forwardBoardScan(grid, x, y-1):  # Can move up
        moves.append((x, y-1))
    if y+1 < cols and grid[x][y+1] == "." and forwardBoardScan(grid, x, y+1):  # Can move down
        moves.append((x, y+1))
    return moves

def random_navigation(rows, cols, steps):
    """ Simulate random navigation on a 2D grid """
    grid = create_grid(rows, cols)
    x, y = 0, 0  # Start in the middle of the grid
    grid[x][y] = 'S'  # Starting point

    for _ in range(steps):
        move_options = valid_moves(grid, x, y)

        if not move_options:
            break  # No valid moves possible
        choice = random.choice(move_options)
        x = choice[0]
        y = choice[1]
        grid[x][y] = 'X'  # Mark the path taken

    grid[x][y] = 'E'  # End point
    return grid



# Generate the grid with random navigation


def create_board(rows, cols):
    """ Create a random board game layout with various elements """
    # Define the possible elements in the board game
    elements = ['R', 'G', 'B', '.']  # R = red trivia, B = blue trivia, G = green trivia, '.' = Empty space
    weights = [0.4, 0.2, 0.1, 0.3]  # Probability weights for each element

    # Create the board as a 2D list
    board = [[random.choices(elements, weights)[0] for _ in range(cols)] for _ in range(rows)]

    # Ensure starting and ending points
    board[0][0] = 'S'  # Start at top-left corner
    board[rows-1][cols-1] = 'E'  # End at bottom-right corner

    return board

def print_board(board):
    """ Print the board in a readable format """
    for row in board:
        print(' '.join(row))
    print()

def generate_sierpinski_carpet(n):
    """ Generate a Sierpinski carpet of size 3**n x 3**n. """
    if n == 0:
        elements = ['R', 'G', 'B', '.']  # R = red trivia, B = blue trivia, G = green trivia, '.' = Empty space
        weights = [0.4, 0.2, 0.1, 0.3]  # Probability weights for each element
        return [[random.choices(elements, weights)[0] for _ in range(4)] for _ in range(4)]  # Base case: a 1x1 grid with a filled square

    # Recursive step: Get the (smaller) Sierpinski carpet
    smaller_carpet = generate_sierpinski_carpet(n-1)
    size = len(smaller_carpet)
    new_size = size * 3
    carpet = [[' ' for _ in range(new_size)] for _ in range(new_size)]

    # Populate the larger carpet with 8 smaller carpets and a hole in the center
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:  # Leave the center sub-grid empty
                continue
            # Calculate where to place the smaller carpet in the larger one
            start_x = i * size
            start_y = j * size
            for x in range(size):
                for y in range(size):
                    carpet[start_x + x][start_y + y] = smaller_carpet[x][y]

    return carpet

def print_carpet(carpet):
    """ Print the 2D grid representation of the carpet. """
    for row in carpet:
        print(''.join(row))


def main(): 
    #rows = 10  # Number of rows in the board
    #cols = 10  # Number of columns in the board

    # Generate the board
    #game_board = create_board(rows, cols)

    # Print the generated board
    #print_board(game_board)
    # Example usage
    #n = 2  # Depth of recursion, generates a 3**3 x 3**3 grid
    #sierpinski_carpet = generate_sierpinski_carpet(n)
    #print_carpet(sierpinski_carpet)
    pygameDemo()
    
if __name__=="__main__": 
    main() 