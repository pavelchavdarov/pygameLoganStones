import pygame
from pygame.sprite import Sprite
from pygame import Rect
from pygame import image
from math import cos
from math import sin
from math import pi

from View import images

pi2 = 2 * pi
class Stone (Sprite):

    def __init__(self, radius, position, group, sides):
        Sprite.__init__(self, group)
        self.Radius = radius
        #self.Position = position
        R = radius / cos(pi/6)
        self.rect = Rect((position[0] - R, position[1] - radius), (R, radius))
        self.sides = sides
        self.stone_side = self.sides[0]
        self.image_sides = {x: image.load(images[x]) for x in self.sides}
        self.image = None

    def update(self, *args):
        self.image = self.image_sides[self.stone_side]

    def flip(self):
        cur_side = (self.sides.index(self.stone_side) + 1) % 2
        self.stone_side = self.sides[cur_side]
        # self.drawStone(position)
'''
    def drawStone(self, position):
        lines = [(cos(i / 6 * pi2) * self.Radius / cos(pi / 6) + position[0],
                  sin(i / 6 * pi2) * self.Radius / cos(pi / 6) + position[1])
                 for i in range(0, 6)]
        color = (64, 128, 255)
        pygame.draw.lines(self.rect, color, True, lines)
'''