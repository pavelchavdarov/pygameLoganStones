import pygame
from pygame.sprite import Sprite
from pygame import Rect
from math import cos
from math import sin
from math import pi
from pygame.math import Vector2
from pygame.sprite import Group

from resources import StoneViewGenerator
from .Interface import MoveProvider
from .StoneModel import StoneModel
from Settings import CELL_RADIUS


# pi2 = 2 * pi

class StoneBuilder:
    def __init__(self):
        self._init()

    def _init(self):
        self.radius = self.position = self.group = self.stone_model = \
            self.move_provider = None
        self.position = (0, 0)

    def set_position(self, position):
        self.position = position
        return self

    def set_group(self, group):
        self.group = group
        return self

    def set_stone_model(self, stone_model):
        self.stone_model = stone_model
        return self

    def set_move_provider(self, move_provider):
        self.move_provider = move_provider
        return self

    def build(self):
        stone = Stone()

        if self.position:
            # stone.Center = Vector2(self.position)
            # stone.rect = Rect((round(stone.Center[0] - stone.Radius), round(stone.Center[1] - stone.radius)),
            #                   (round(stone.Radius * 2), round(stone.radius * 2)))
            stone.rect = Rect(self.position - Vector2(stone.Radius, stone.radius),
                              (stone.Radius * 2, stone.radius * 2))

        if self.group is not None:
            self.group.add(stone)

        if self.stone_model:
            stone_view = StoneViewGenerator.get_simple_generator(stone.radius - 1)
            stone.stone_model = self.stone_model
            stone.image_sides = stone_view.get_views(stone.stone_model)
            stone.image = stone.image_sides[stone.stone_model.side]

        if self.move_provider:
            stone.move_provider = self.move_provider

        # почистим переменные-параметры
        self._init()

        return stone


class Stone(Sprite):
    def __init__(self):
        super().__init__()

        # self.Center = position
        # group.add(self)
        self.position = None
        self.stone_model = None
        self.image_sides = None
        # self.Center = None
        self.image = None
        self.rect = None

        self.radius = CELL_RADIUS
        self.Radius = self.radius / cos(pi / 6)
        self.radius_vector = Vector2(self.Radius, self.radius)
        # self.stone_model = stone_model

        # stone_view = StoneViewGenerator.get_simple_generator(self.radius-1)
        # self.image_sides = stone_view.get_views(self.stone_model)
        # self.image = self.image_sides[self.stone_model.side]
        # self.rect = Rect((round(position[0] - self.Radius), round(position[1] - self.radius)),
        #                  (self.image.get_width(), self.image.get_height()))
        # self.move_provider = move_provider
    @property
    def Center(self):
        return self.rect.center

    def update(self, *args):
        self.image = self.image_sides[self.stone_model.side]

    def flip(self):
        self.stone_model.flip()

    def is_over(self, pos):
        vec_centr = Vector2(self.Center)
        vec_pos = Vector2(pos)
        return round(vec_pos.distance_to(vec_centr)) < self.radius

    def move_to(self, position: Vector2):
        # self.rect = Rect((round(position[0] - self.Radius), round(position[1] - self.radius)),
        #                  (self.image.get_width(), self.image.get_height()))
        self.rect = Rect(position - self.radius_vector,
                         (self.image.get_width(), self.image.get_height()))

        # self.Center = position

    def get_rect(self):
        return self.rect


# class Avatar(Sprite):
class Avatar(Sprite):
    def __init__(self):
        super().__init__()
        self.image = None
        self.Center = None
        self.rect = None
        self.radius = CELL_RADIUS
        self.Radius = self.radius / cos(pi / 6)
        self.radius_vector = Vector2(self.Radius, self.radius)

    def set_image(self, image):
        self.image = image
        return self

    # def set_centr(self, pos):
    #     self.Center = pos
    #     return self

    def set_rect(self, pos):
        self.rect = Rect((pos[0], pos[1]), (self.image.get_width(), self.image.get_height()))
        return self

    def move_to(self, position: Vector2):
        # if self.move_provider:
        #     self.move_provider.move_to(self, position)
        # return self
        # self.rect = Rect((round(position[0] - self.Radius), round(position[1] - self.radius)),
        #                  (self.image.get_width(), self.image.get_height()))
        self.rect = Rect(position - self.radius_vector,
                         (self.image.get_width(), self.image.get_height()))

        self.Center = position
        return self

    def set_group(self, group):
        group.add(self)
        return self
