
class Model:
    def __init__(self):
        self.__StonesOnBoard = dict()
        self.marked_stone = None

    def put_stone(self, position, stone):
        if position not in self.__StonesOnBoard and stone:
            self.__StonesOnBoard[position] = stone
            print("put_stone: ", self.__StonesOnBoard.keys())
            return 0
        return 1

    def move_stone(self, from_pos, to_pos):
        if from_pos in self.__StonesOnBoard:
            self.__StonesOnBoard[to_pos] = self.__StonesOnBoard.pop(from_pos)
            print("move_stone", self.__StonesOnBoard.keys())

    def get_stone(self, position):
        if position in self.__StonesOnBoard:
            return self.__StonesOnBoard[position]
        else:
            return None

    def get_board(self):
        return self.__StonesOnBoard.keys()

