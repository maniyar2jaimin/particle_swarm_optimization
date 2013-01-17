#!/usr/bin/env python

import time
from pdb import set_trace

import pygame
from pygame.locals import *

from random import sample, randint, choice

SCREEN = None
SCREEN_SIZE = 500, 500
FRAME_RATE = 24
PLOT = []
X = Y = 250
C = (X, Y)
R = 200

SAMPLE_SIZE = 100
MAX_CIRCLE_WIDTH = 15

def circle():
    f = 1 - R; ddf_x = 1; ddf_y = -2 * R
    x = 0; y = R

    while x < y:
        if f >= 0: 
            y -= 1
            ddf_y += 2
            f += ddf_y
        x += 1
        ddf_x += 2
        f += ddf_x

        yield x, y


def initialize_screen():
    global SCREEN
    pygame.init()
    SCREEN = pygame.display.set_mode(SCREEN_SIZE)

    background = pygame.Surface(SCREEN.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    SCREEN.blit(background, (0, 0))
    pygame.display.flip()


def initialize_plot():
    global PLOT
    octants = [
                'X + y, Y + x', 'X + x, Y + y',
                'X - x, Y + y', 'X - y, Y + x',
                'X - y, Y - x', 'X - x, Y - y',
                'X + x, Y - y', 'X + y, Y - x',
              ]
    for x,y in circle():
        for octant in octants:
            x_boundary, y_boundary = eval(octant)
            if x_boundary >= 250:
                PLOT.extend(map(lambda k:(k, y_boundary), range(250,x_boundary+1)))
            elif x_boundary<250:
                PLOT.extend(map(lambda k:(k, y_boundary), range(x_boundary, 250)))
    PLOT = set(PLOT)
    PLOT = list(PLOT)


def draw_circle(point, radius, color):
    for r in range(radius, 0, -1):
        #pygame.draw.circle(SCREEN, (255, 255, 10), point, radius)
        pygame.draw.circle(SCREEN, color, point, radius)


def main():

    initialize_screen()
    initialize_plot()

    SAMPLE = sample(PLOT, SAMPLE_SIZE)
    MASTER_DICT = {}
    #COLOR_STRING = '(255.0/randint(1,20),255.0/randint(1,20),255.0/randint(1,20))'
    COLOR_STRING = '(255,255,50)'
    for point in SAMPLE:
        # This is the start point of the circle, from which it cycles between 0
        # and MAX_CIRCLE_WIDTH
        # Direction specifies whether to brighten or dim the point
        MASTER_DICT[point] = randint(1, MAX_CIRCLE_WIDTH), 1, eval(COLOR_STRING)

    while 1:
        NEW_DICT = {}
        time.sleep(1.0/FRAME_RATE)
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        SCREEN.fill((0,0,0))
        SCREEN.lock()
        sacred_point = MASTER_DICT.keys()[0]
        for point, (radius, direction, color) in MASTER_DICT.iteritems():
            draw_circle(point, radius, color)
            if radius in (0, MAX_CIRCLE_WIDTH):
                direction = -direction
            if radius == 0:
                point = choice(PLOT)
                color = eval(COLOR_STRING)
            NEW_DICT[point] = radius+direction, direction, color
        #MASTER_DICT[point] = radius + direction, direction
        MASTER_DICT = NEW_DICT

        SCREEN.unlock()

        SCREEN.blit(SCREEN, (0, 0))
        pygame.display.flip()


if __name__ == '__main__': main()
