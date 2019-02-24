from Stone.StoneModel import StoneModel
from random import shuffle
from random import randint


class PouchModel:
    __pouch = []
    __stones_amount = 18

    def __init__(self, stone_sides):
        if not PouchModel.__pouch:
            for i in range(0, 6):
                PouchModel.__pouch.append(StoneModel(stone_sides[0], stone_sides[1]))
                PouchModel.__pouch.append(StoneModel(stone_sides[1], stone_sides[2]))
                PouchModel.__pouch.append(StoneModel(stone_sides[2], stone_sides[0]))

                # PouchModel.__pouch.append(StoneModel(stone_sides[0], stone_sides[2]))
                # PouchModel.__pouch.append(StoneModel(stone_sides[1], stone_sides[0]))
                # PouchModel.__pouch.append(StoneModel(stone_sides[2], stone_sides[1]))
            self.shake()
            self.shake()
            self.shake()

    def __get_stone(self):
        if PouchModel.__pouch:
            return PouchModel.__pouch.pop()

    def shake(self):
        shuffle(PouchModel.__pouch)
        for stone in PouchModel.__pouch:
            if randint(1, 2) % 2:
                stone.flip()

    @staticmethod
    def get_value():
        return len(PouchModel.__pouch)

    def __getattr__(self, item):
        if item == 'stones':
            while len(PouchModel.__pouch):
                yield PouchModel.__pouch.pop()
        else:
            return item
