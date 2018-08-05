from pygame import Surface
from pygame import draw
from math import sin
from math import cos
from math import pi

_STONE_COLOR = {"rock":      (194, 159, 117),
                   "scissors":  (176, 196, 250),
                   "papper":    (248, 248, 255)
                }
pi2 = pi * 2


class StoneSideViewer:
    def get_entity(self, side_name):
        raise Exception("Not implemented!")

    def get_views(self, side_list):
        pass


class StoneViewGenerator:
    __instance = None

    class Stone3SideViewer(StoneSideViewer):

        def __init__(self, radius, attitude=0):
            self.radius = radius
            self.attitude = attitude
            self.__sides_dict = dict()

            r1 = self.radius / cos(pi / 6)
            if self.attitude == 0:
                lines = [(round(cos(i / 6 * pi2) * self.radius / cos(pi / 6) + r1 + 1),
                          round(sin(i / 6 * pi2) * self.radius / cos(pi / 6) + self.radius) + 1)
                         for i in range(0, 6)]
                image = Surface((round(2 * r1) + 3, round(2 * self.radius) + 3))
            else:
                lines = [(sin(i / 6 * pi2) * self.radius / cos(pi / 6) + self.radius,
                          cos(i / 6 * pi2) * self.radius / cos(pi / 6) + r1)
                         for i in range(0, 6)]
                image = Surface((round(2 * self.radius), round(2 * r1)))

            for side in _STONE_COLOR:
                self.__sides_dict[side] = image.copy()
                self.__sides_dict[side].set_colorkey((0, 0, 0))
                draw.aalines(self.__sides_dict[side], _STONE_COLOR[side], True, lines)

        def get_entity(self, side_name):
            if side_name in self.__sides_dict:
                return self.__sides_dict[side_name]
            else:
                return None

        def get_views(self, side_list):
            return {x: self.get_entity(x) for x in side_list.sides}

    @staticmethod
    def get_simple_generator(radius):
        if not StoneViewGenerator.__instance:
            StoneViewGenerator.__instance = StoneViewGenerator.Stone3SideViewer(radius)
        else:
            StoneViewGenerator.__instance.radius = radius
        return StoneViewGenerator.__instance




