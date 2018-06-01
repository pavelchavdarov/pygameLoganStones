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
        self.is_marked = False

    def update(self, *args):
        self.image = self.image_sides[self.stone_side].copy()
        self.draw_marker()

    def flip(self):
        cur_side = (self.sides.index(self.stone_side) + 1) % 2
        self.stone_side = self.sides[cur_side]

    def mark(self):
        self.is_marked = not self.is_marked

    def draw_marker(self):
        if self.is_marked:
            pos = (self.Radius / cos(pi / 6), self.Radius)
            lines = [(cos(i / 6 * pi2) * (self.Radius-3) / cos(pi / 6) + pos[0],
                      sin(i / 6 * pi2) * (self.Radius-3) / cos(pi / 6) + pos[1])
                     for i in range(0, 6)]
            color = (255, 255, 50)
            # pygame.draw.lines(self.image, color, True, lines)
            pygame.draw.polygon(self.image, color, lines, 2)

'''
    def drawStone(self, position):
        lines = [(cos(i / 6 * pi2) * self.Radius / cos(pi / 6) + position[0],
                  sin(i / 6 * pi2) * self.Radius / cos(pi / 6) + position[1])
                 for i in range(0, 6)]
        color = (64, 128, 255)
        pygame.draw.lines(self.rect, color, True, lines)
'''


