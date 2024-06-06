import array
import math

import cairo
import pygame
from pygame.locals import *
import rsvg

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
player = pygame.Rect((300, 250, 50, 50))

run = True
moving = False

while run:
    
    screen.fill((0,0,0))

    pygame.draw.rect(screen, (255, 0, 0), player)
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
    pygame.display.update()

pygame.quit()