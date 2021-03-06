from .Interface import ITwoSideStone


class StoneModel(ITwoSideStone):

    def __init__(self, *sides):
        self.__sides = list()
        for side in sides:
            self.__sides.append(side)
        self.stone_side = self.__sides[0]

    def get_side(self):
        return self.stone_side

    def flip(self):
        cur_side = (self.__sides.index(self.stone_side) + 1) % 2
        self.stone_side = self.__sides[cur_side]

    def __getattr__(self, item):
        if item == 'sides':
            return tuple(self.__sides)
        else:
            return item

    def __setattr__(self, key, value):
        if key == 'sides':
            self.__sides = list(value)
        else:
            super().__setattr__(key, value)


