import pygame
from pygame.sprite import Sprite
from pygame import Rect
from math import cos
from math import sin
from math import pi

from resources import GeneratorSingleton

pi2 = 2 * pi


class Stone (Sprite):

    def __init__(self, radius=None, position=None, group=None, sides=None):
        Sprite.__init__(self, group)

        if radius and position and group and sides:
            self.radius = radius - 3
            self.radius_ext = self.radius / cos(pi / 6)
            self.sides = sides
            self.stone_side = self.sides[0]
            side_gen = GeneratorSingleton.get_generator(self.radius)
            self.image_sides = {x: side_gen.get_entity(x) for x in self.sides}
            self.image = self.image_sides[self.stone_side]
            self.rect = Rect((round(position[0] - self.radius_ext), round(position[1] - self.radius)),
                             (self.image.get_width(), self.image.get_height()))
            self.is_marked = False

    def get_avatar(self):
        avatar = Stone(self.radius + 3, (0, 0), self.groups()[0], self.sides)
        avatar.rect = self.rect.copy()
        avatar.image.set_alpha(150)
        return avatar

    def update(self, *args):
        self.image = self.image_sides[self.stone_side]

    def flip(self):
        cur_side = (self.sides.index(self.stone_side) + 1) % 2
        self.stone_side = self.sides[cur_side]

    def mark(self):
        self.is_marked = not self.is_marked

    def __draw_marker(self):
        if self.is_marked:
            pos = (self.radius / cos(pi / 6), self.radius)
            lines = [(cos(i / 6 * pi2) * self.radius / cos(pi / 6) + pos[0],
                      sin(i / 6 * pi2) * self.radius / cos(pi / 6) + pos[1])
                     for i in range(0, 6)]
            color = (255, 255, 50)
            pygame.draw.polygon(self.image, color, lines, 2)

    def move_to(self, position):
        self.rect = Rect((round(position[0] - self.radius_ext), round(position[1] - self.radius)),
                         (self.image.get_width(), self.image.get_height()))

    def get_rect(self):
        return self.rect


class StoneAvatar(Stone):

    def __init__(self, stone):
        Stone.__init__(self, group=stone.groups()[0])
        self.radius = stone.radius
        self.radius_ext = stone.radius_ext
        self.image = stone.image.copy()
        self.image.set_alpha(150)
        self.rect = stone.rect.copy()
        self.add(stone.groups()[0])

    def update(self, *args):
        pass
