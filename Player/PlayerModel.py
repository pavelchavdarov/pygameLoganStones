from pygame import Rect
from Groups.PlayerGroup import PlayerGroup


class Player:
    def __init__(self, area: Rect, index: int):
        self.__stone_group = PlayerGroup(area, index)
    @property
    def batch(self):
        return self.__stone_group


class PlayerDispatcher:
    def __init__(self, player1_area, player2_area):
        self.__players = [Player(player1_area,0), Player(player2_area,1)]
        self.__current = 0

    @property
    def current_player(self):
        return self.__players[self.__current]

    def pass_turn(self):
        self.__current = (self.__current + 1) % 2