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

    def set_radius(self, radius):
        self.radius = radius
        return self

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
        return Stone(self.radius, self.position, self.group, self.stone_model, self.move_provider)


class Stone(Sprite):

    def __init__(self, radius: int =None, position: tuple =None, group: pygame.sprite.Group =None,
                 stone_model: StoneModel =None, move_provider: MoveProvider =None):

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
        self.move_provider = move_provider



    def update(self, *args):
        self.image = self.image_sides[self.stone_model.get_side()]

    def flip(self):
        self.stone_model.flip()

    def is_clicked(self, pos):
        vec_centr = Vector2(self.Center)
        vec_pos = Vector2(pos)
        return round(vec_pos.distance_to(vec_centr)) < self.radius

    #def mark(self):
    #    self.is_marked = not self.is_marked

    # def __draw_marker(self):
    #    if self.is_marked:
    #        pos = (self.radius / cos(pi / 6), self.radius)
    #        lines = [(cos(i / 6 * pi2) * self.radius / cos(pi / 6) + pos[0],
    #                  sin(i / 6 * pi2) * self.radius / cos(pi / 6) + pos[1])
    #                for i in range(0, 6)]
    #        color = (255, 255, 50)
    #       pygame.draw.polygon(self.image, color, lines, 2)

    def move_to(self, position):
        if self.move_provider:
            self.move_provider.move_to(self, position)

        #self.rect = Rect((round(position[0] - self.Radius), round(position[1] - self.radius)),
        #                 (self.image.get_width(), self.image.get_height()))
        #self.Center = position

    def get_rect(self):
        return self.rect

    #def create_avatar(self):
    #    avatar = deepcopy(self)
    #    avatar.image.set_alpha(150)
    #    avatar.origin_stone = self


class StoneAvatar(Sprite):

    def __init__(self, stone, move_provider):
        super().__init__()
        self.Center = stone.Center
        stone.groups()[0].add(self)
        self.radius = stone.radius
        self.Radius = stone.Radius
        self.image = stone.image.copy()
        self.image.set_alpha(150)
        self.rect = stone.rect.copy()
        self.origin_stone = stone
        self.move_provider = move_provider

    def move_to(self, position):
        if self.move_provider:
            self.move_provider.move_to(self, position)
