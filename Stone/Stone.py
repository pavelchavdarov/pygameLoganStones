import pygame
from pygame.sprite import Sprite
from pygame import Rect
from math import cos
from math import sin
from math import pi
from pygame.math import Vector2
from pygame.sprite import Group

from resources import StoneViewGenerator
from Stone.Interface import ITwoSideStone


# pi2 = 2 * pi


class Stone (Sprite):

    def __init__(self, radius=None, position=None, group=None, stone_model=None):

        super().__init__()
        if not (radius and position and isinstance(group, Group) and stone_model):
            return

        self.Center = position
        group.add(self)

        self.radius = radius
        self.Radius = self.radius / cos(pi / 6)
        self.stone_model = stone_model

        stone_view = StoneViewGenerator.get_simple_generator(self.radius-1)
        self.image_sides = stone_view.get_views(self.stone_model)
        self.image = self.image_sides[self.stone_model.get_side()]
        self.rect = Rect((round(position[0] - self.Radius), round(position[1] - self.radius)),
                         (self.image.get_width(), self.image.get_height()))
        self.is_marked = False

    def update(self, *args):
        self.image = self.image_sides[self.stone_model.get_side()]

    def flip(self):
        self.stone_model.flip()


    def is_clicked(self, pos):
        vec_centr = Vector2(self.Center)
        vec_pos = Vector2(pos)
        return round(vec_pos.distance_to(vec_centr)) < self.radius

    def mark(self):
        self.is_marked = not self.is_marked

    # def __draw_marker(self):
    #    if self.is_marked:
    #        pos = (self.radius / cos(pi / 6), self.radius)
    #        lines = [(cos(i / 6 * pi2) * self.radius / cos(pi / 6) + pos[0],
    #                  sin(i / 6 * pi2) * self.radius / cos(pi / 6) + pos[1])
    #                for i in range(0, 6)]
    #        color = (255, 255, 50)
    #       pygame.draw.polygon(self.image, color, lines, 2)

    def move_to(self, position):
        self.rect = Rect((round(position[0] - self.Radius), round(position[1] - self.radius)),
                         (self.image.get_width(), self.image.get_height()))
        self.Center = position

    def get_rect(self):
        return self.rect


class StoneAvatar(Stone):

    def __init__(self, stone):
        super().__init__()
        self.Center = stone.Center
        stone.groups()[0].add(self)
        self.radius = stone.radius
        self.Radius = stone.Radius
        self.image = stone.image.copy()
        self.image.set_alpha(150)
        self.rect = stone.rect.copy()
        self.origin_stone = stone

    def update(self, *args):
        pass
