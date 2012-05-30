#!/usr/bin/env python

from collections import namedtuple
from copy import copy
 
Colour = namedtuple('Colour','r,g,b')
Colour.copy = lambda self: copy(self)
 
black = Colour(0,0,0)
white = Colour(255,255,255) # Colour ranges are not enforced.
 
class Bitmap():
    def __init__(self, width = 40, height = 40, background=white):
        assert width > 0 and height > 0 and type(background) == Colour
        self.width = width
        self.height = height
        self.background = background
        self.map = [[background.copy() for w in range(width)] for h in range(height)]
 
    def fillrect(self, x, y, width, height, colour=black):
        assert x >= 0 and y >= 0 and width > 0 and height > 0 and type(colour) == Colour
        for h in range(height):
            for w in range(width):
                self.map[y+h][x+w] = colour.copy()
 
    def chardisplay(self):
        txt = [''.join(' ' if bit==self.background else '@'
                       for bit in row)
               for row in self.map]
        # Boxing
        txt = ['|'+row+'|' for row in txt]
        txt.insert(0, '+' + '-' * self.width + '+')
        txt.append('+' + '-' * self.width + '+')
        print('\n'.join(reversed(txt)))
 
    def set(self, x, y, colour):
        assert type(colour) == Colour
        self.map[y][x]=colour
 
    def get(self, x, y):
            return self.map[y][x]
 
if __name__ == '__main__': 
    '''
    The origin, 0,0; is the lower left, with x increasing to the right,
    and Y increasing upwards.
     
    The code below produces the following display :
     
    +--------------------+
    |                    |
    |                    |
    |    @@@@@@          |
    |    @@@@@@          |
    |    @@@@@@          |
    |                    |
    |                    |
    |                    |
    |@                   |
    |                    |
    +--------------------+
    '''
    bitmap = Bitmap(20,10)
    bitmap.fillrect(4, 5, 6, 3)
    assert bitmap.get(5, 5) == black
    assert bitmap.get(0, 1) == white
    bitmap.set(0, 1, black)
    assert bitmap.get(0, 1) == black
    bitmap.chardisplay()
 
