import array
import math
import sys
import cairo
import pygame
from pygame.locals import *
sys.path.append('/path/to/application/app/folder')
import wrappers.rsvg as rsvg
import random
from tile import *
from colors import *
from board import cBoard

def pygameDemo():
    WIDTH = 1280
    HEIGHT = 720



    #globals are bad, avoid them when we can
    run = True
    moving = False
    color = green

    playBoard = cBoard(WIDTH, HEIGHT)

    #except for these, you could make an argument that this is acceptable since there will only ever be One screen and 4 players
    screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.RESIZABLE)
    player_size = WIDTH * HEIGHT * .00008
    player = pygame.Rect((300, 250, player_size, player_size))

    bounding_box = pygame.Rect(300, 200, 200, 200)
    bounding_box2 = pygame.Rect(100, 200, 200, 200)

    #detect if we are in bounding box
    def is_inside_bounding_box(point_or_rect):
        """ Check if a point or another rectangle is inside the bounding box. """
        if isinstance(point_or_rect, pygame.Rect):
            return bounding_box.colliderect(point_or_rect)
        elif isinstance(point_or_rect, tuple):
            return bounding_box.collidepoint(point_or_rect)
        return False

    def initializeBoard():
        LENGTH = WIDTH
        OFFSET = HEIGHT
        if HEIGHT < WIDTH:
            LENGTH = HEIGHT
            OFFSET = WIDTH
        rect_x, rect_y = WIDTH//4, HEIGHT//4  # Position of the rectangle we always work in quadrants
        rect_width, rect_height = LENGTH - (.1 * OFFSET), LENGTH - (.1 * OFFSET)  # Size of the rectangle
        cols, rows = 9, 9  # Number of columns and rows in the grid
        cell_width = rect_width // cols
        cell_height = rect_height // rows
        center_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        center_rect.center = (WIDTH + 200,HEIGHT//2)
        for col in range(cols):
            for row in range(rows):
                cell_x = rect_x + col * cell_width + (LENGTH * .4)
                cell_y = rect_y + row * cell_height - (LENGTH * .15)
                cell_rect = pygame.Rect(cell_x, cell_y, cell_width, cell_height)
                pygame.draw.rect(screen, base01, cell_rect, 1)
    while run:
        
        screen.fill((25, 28, 38))
        #draw calls
        #pygame.draw.rect(screen, color, bounding_box)
        #pygame.draw.rect(screen, color, bounding_box2, 7)
        #do a draw of the grid
        initializeBoard()
        #Test for resize
        #pygame.draw.rect(screen, (200,0,0), (screen.get_width()/3, screen.get_height()/3, screen.get_width()/3, screen.get_height()/3))
        #pygame.draw.rect(screen, red, playBoard.outerBoard, 1)
        pygame.draw.rect(screen, base1, player)
        for event in pygame.event.get():
            if event.type == QUIT:
                run= False

            if event.type == pygame.VIDEORESIZE:
                # addfunctionality to resize everything
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            # Making player move
            if event.type == MOUSEBUTTONDOWN:
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
            color = blue
        else:
            color = green
        
        #perform a check on the player cube so that it cant go off screen
        #right edge
        if player.x > WIDTH - player_size:
            player.x = WIDTH - player_size
        #left edge
        if player.x < 0:
            player.x = 0
        #lower edge
        if player.y < 0:
            player.y = 0
        #upper edge
        if player.y > HEIGHT - player_size:
            player.y = HEIGHT - player_size
        pygame.display.update()
        

    pygame.quit()

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