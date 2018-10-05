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


class StoneMoveProvider(MoveProvider):
    def move_to(self, stone, position):
        stone.rect = Rect((round(position[0] - stone.Radius), round(position[1] - stone.radius)),
                          (stone.image.get_width(), stone.image.get_height()))
        stone.Center = position


class StoneBuilder:
    def __init__(self):
        self.radius = self.position = self.group = self.stone_model = \
        self.move_provider = None


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
        return Stone(self.position, self.group, self.stone_model, self.move_provider)


class Stone(Sprite):
    def __init__(self, position: tuple, group: pygame.sprite.Group ,
                 stone_model: StoneModel, move_provider: MoveProvider):

        super().__init__()

        self.Center = position
        group.add(self)

        self.radius = CELL_RADIUS
        self.Radius = self.radius / cos(pi / 6)
        self.stone_model = stone_model

        stone_view = StoneViewGenerator.get_simple_generator(self.radius-1)
        self.image_sides = stone_view.get_views(self.stone_model)
        self.image = self.image_sides[self.stone_model.side]
        self.rect = Rect((round(position[0] - self.Radius), round(position[1] - self.radius)),
                         (self.image.get_width(), self.image.get_height()))
        self.move_provider = move_provider

    def update(self, *args):
        self.image = self.image_sides[self.stone_model.side]

    def flip(self):
        self.stone_model.flip()

    def is_over(self, pos):
        vec_centr = Vector2(self.Center)
        vec_pos = Vector2(pos)
        return round(vec_pos.distance_to(vec_centr)) < self.radius

    def move_to(self, position):
        if self.move_provider:
            self.move_provider.move_to(self, position)

    def get_rect(self):
        return self.rect



class Avatar(Sprite):
    def __init__(self):
        super().__init__()
        self.image = None
        self.Center = None
        self.rect = None
        self.move_provider = None

        self.radius = CELL_RADIUS
        self.Radius = self.radius / cos(pi / 6)



    def set_image(self, image):
        self.image = image
        return self

    def set_centr(self, pos):
        self.Center = pos
        return self

    def set_rect(self, pos):
        self.rect = Rect((pos[0],pos[1]), (self.image.get_width(), self.image.get_height()))
        return self

    def set_move_provider(self, move_provider):
        self.move_provider = move_provider
        return self

    def move_to(self, position):
        if self.move_provider:
            self.move_provider.move_to(self, position)
        return self

    def set_group(self, group):
        group.add(self)
        return self