from Stone.StoneModel import StoneModel
from Stone.Stone import Stone
from pygame.sprite import RenderUpdates

class Player:
    def __init__(self):
        self.__stole_list = []

    def get_stones(self):
        return tuple(self.__stole_list)

    def add_stone(self, stone_model):
        if isinstance(stone_model, StoneModel):
            self.__stole_list.append(stone_model)

    # TODO: get_stone()

class PlayerBatch:
    def __init__(self):
        self.__stone_group = RenderUpdates()

    def get_batch(self):
        return self.__stone_group


class PlayerDispatcher:
    def __init__(self):
        self.__players = [PlayerBatch(), PlayerBatch()]
        self.__current = 0

    def __getattr__(self, item):
        if item == 'current_player':
            current = self.__players[self.__current]
            self.__current = (self.__current + 1) % 2
            return current
        else:
            return item
