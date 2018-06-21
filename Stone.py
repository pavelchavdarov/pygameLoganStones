import pygame
from pygame.sprite import Sprite
from pygame import Rect
from math import cos
from math import sin
from math import pi

from resources import GeneratorSingleton

pi2 = 2 * pi


class Stone (Sprite):

    def __init__(self, radius, position, group, sides):
        Sprite.__init__(self, group)
        self.Radius = radius-3
        r = self.Radius / cos(pi/6)
        self.sides = sides
        self.stone_side = self.sides[0]
        # TODO: избавиться от этого ужаса
        side_gen = GeneratorSingleton.get_generator(self.Radius)
        self.image_sides = {x: side_gen.get_entity(x).copy() for x in self.sides}
        self.image = self.image_sides[self.stone_side]
        self.rect = Rect((round(position[0] - r), round(position[1] - self.Radius)),
                         (self.image.get_width(), self.image.get_height()))
        self.is_marked = False

    def get_avatar(self):
        avatar = Stone(self.Radius+3, (0, 0), self.groups()[0], self.sides)
        avatar.rect = self.rect.copy()
        avatar.image.set_alpha(150)
        return avatar

    def update(self, *args):
        self.image = self.image_sides[self.stone_side].copy()

    def flip(self):
        cur_side = (self.sides.index(self.stone_side) + 1) % 2
        self.stone_side = self.sides[cur_side]

    def mark(self):
        self.is_marked = not self.is_marked

    def __draw_marker(self):
        if self.is_marked:
            pos = (self.Radius / cos(pi / 6), self.Radius)
            lines = [(cos(i / 6 * pi2) * (self.Radius) / cos(pi / 6) + pos[0],
                      sin(i / 6 * pi2) * (self.Radius) / cos(pi / 6) + pos[1])
                     for i in range(0, 6)]
            color = (255, 255, 50)
            pygame.draw.polygon(self.image, color, lines, 2)

    def move_to(self, position):
        r = self.Radius / cos(pi / 6)
        self.rect = Rect((round(position[0] - r), round(position[1] - self.Radius)), (self.image.get_width(), self.image.get_height()))

    def get_rect(self):
        return self.rect

