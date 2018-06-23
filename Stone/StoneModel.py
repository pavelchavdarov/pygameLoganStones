from .Interface import ITwoSideStone


class StoneFactory:
    class __StoneModel(ITwoSideStone):
        def __init__(self):
            self.sides = []
            self.stone_side = None

        def set_sides(self, sides):
            self.sides = list(sides)
            self.stone_side = self.sides[0]

        def get_side(self):
            return self.stone_side

        def flip(self):
            cur_side = (self.sides.index(self.stone_side) + 1) % 2
            self.stone_side = self.sides[cur_side]

    @staticmethod
    def create_stone(*sides):
        stone_model = StoneFactory.__StoneModel()
        stone_model.set_sides(list(sides))

