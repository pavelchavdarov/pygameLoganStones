from pygame import Surface
from pygame import draw
from math import sin
from math import cos
from math import pi

_STONE_SIDES_3 = ("rock", "scissors", "papper")


class StoneSideViewer:
    def get_side_view(self, side_name):
        raise Exception("Not implemented!")


class SideGenerator3(StoneSideViewer):

    def __init__(self, radius, attitude):
        self.radius = radius
        self.attitute = attitude
        self.__sides_dict = dict()

        pi2 = pi * 2
        r1 = self.radius / cos(pi / 6)
        if self.attitute == 0:
            lines = [(round(cos(i / 6 * pi2) * self.radius / cos(pi / 6) + r1+1),
                      round(sin(i / 6 * pi2) * self.radius / cos(pi / 6) + self.radius)+1)
                     for i in range(0, 6)]
            image = Surface((round(2 * r1)+3, round(2 * self.radius)+3))
        else:
            lines = [(sin(i / 6 * pi2) * self.radius / cos(pi / 6) + self.radius,
                      cos(i / 6 * pi2) * self.radius / cos(pi / 6) + r1)
                     for i in range(0, 6)]
            image = Surface((round(2 * self.radius), round(2 * r1)))

        for side in _STONE_SIDES_3:
            if side == "rock":
                color = (194, 159, 117)
            elif side == "scissors":
                color = (176, 196, 222)
            elif side == "papper":
                color = (248, 248, 255)
            self.__sides_dict[side] = image.copy()
            self.__sides_dict[side].set_colorkey((0, 0, 0))
            draw.aalines(self.__sides_dict[side], color, True, lines)

    def get_side_view(self, side_name):
        if side_name in self.__sides_dict:
            return self.__sides_dict[side_name]
        else:
            return None
