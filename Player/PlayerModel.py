from Stone.StoneModel import StoneModel
from Stone.Stone import Stone

class Player:
    def __init__(self):
        self.__stole_list = []

    def get_stones(self):
        return tuple(self.__stole_list)

    def add_stone(self, stone_model):
        if isinstance(stone_model, StoneModel):
            self.__stole_list.append()

    # TODO: get_stone()