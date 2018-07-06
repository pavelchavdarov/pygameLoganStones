from Stone.StoneModel import StoneModel
from resources import _STONE_ENTITY_3
from random import shuffle
from random import randint


class PouchModel:
    __pouch = []
    __stones_amount = 18

    def init(self):
        if not PouchModel.__pouch:
            stone_sides = list(_STONE_ENTITY_3)
            for i in range(1, 7):
                PouchModel.__pouch.append(StoneModel(stone_sides[0], stone_sides[1]))
                PouchModel.__pouch.append(StoneModel(stone_sides[1], stone_sides[2]))
                PouchModel.__pouch.append(StoneModel(stone_sides[2], stone_sides[0]))

    def get_stone(self):
        return PouchModel.__pouch.pop()

    def shake(self):
        shuffle(PouchModel.__pouch)
        for stone in PouchModel.__pouch:
            if randint(1, 2) % 2:
                stone.flip()

