import array
import math
import sys
import cairo
import pygame
from pygame.locals import *
import rsvg

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