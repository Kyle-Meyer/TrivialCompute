import pygame
import cv2
import numpy
from colors import *

class timerClock(object):

    def __init__(self):
        self.timer_event = pygame.USEREVENT+1
        pygame.time.set_timer(self.timer_event, 1000)
        self.counter = 60
        self.clock = pygame.time.Clock()
        self.startCounting = False
        self.shouldDraw = False
        self.position = (640, 360)
        self.radius = 50
        self.width = 5
        self.font = pygame.font.SysFont(None, 40)
        self.text = self.font.render(str(self.counter), True, base3)

    def drawArcCv2(self, surf, color, center, radius, width, end_angle):
        circle_image = numpy.zeros((radius*2+4, radius*2+4, 4), dtype = numpy.uint8)
        circle_image = cv2.ellipse(circle_image, (radius+2, radius+2),
            (radius-width//2, radius-width//2), 0, 0, end_angle, (*color, 255), width, lineType=cv2.LINE_AA) 
        circle_surface = pygame.image.frombuffer(circle_image.flatten(), (radius*2+4, radius*2+4), 'RGBA')
        if end_angle > 0:
            surf.blit(circle_surface, circle_surface.get_rect(center = center), special_flags=pygame.BLEND_PREMULTIPLIED)

    def changeFontSize(self, inSize):
        self.font = pygame.font.SysFont(None, inSize)

    def countTime(self, event):
        self.clock.tick(60)
        if event.type == self.timer_event:
            self.counter -= 1
            self.text = self.font.render(str(self.counter), True, base3)
            if self.counter == 0:
                pygame.time.set_timer(self.timer_event, 0)

    def drawClock(self, window):
        text_rect = self.text.get_rect(center = self.position)
        self.text = self.font.render(str(self.counter), True, base3)
        #print(self.counter)
        self.drawArcCv2(window, base3, self.position, self.radius, self.width, 580*self.counter/100)
        window.blit(self.text, text_rect)
