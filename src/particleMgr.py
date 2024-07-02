import pygame
import sys
import random
import os
import sys
from colors import *

class particleManager(object):
    num_particles = 200
    screen_width = 100
    screen_height = 100
    particles = []
    timingOffset = 0
    def drawParticles(self, screen):
        # Update particle positions
        if self.timingOffset < len(self.particles):
            self.timingOffset += 1
        for i in range(self.timingOffset):
            particle = self.particles[i]
            particle['x'] += particle['speed']  # Move particle rightwards at its own speed
            # Reset particles that move off the screen to simulate continuous flow
            if particle['x'] > self.screen_width:
                particle['x'] = random.randint(-100, 0)
                particle['y'] = random.randint(0, self.screen_height)
            pygame.draw.circle(screen, particle['color'], (int(particle['x']), int(particle['y'])), particle['size'])

    def __init__(self, width, height):
        self.screen_height = height
        self.screen_width = width
        # Each particle is a dictionary with x, y, and speed
        for _ in range(self.num_particles):
            particle = {
                'x': random.randint(-100, 0),  # Start off-screen
                'y': random.randint(0, height),
                'speed': random.uniform(2, 6),  # Slow speeds
                'color': random.choice([particle1, particle2, particle3]),
                'size' : random.randint(1, 3)
            }
            self.particles.append(particle)