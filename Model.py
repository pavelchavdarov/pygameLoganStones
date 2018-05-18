
class Model:
    def __init__(self):
        self.__StonesOnBoard = {}
        #self.Pouch = []


    def putStone(self, position, stone):
        if not(self.__StonesOnBoard[position]):
            self.__StonesOnBoard[position] = stone
            return 0
        return 1

    def getBoard(self):
        board = tuple(self.__StonesOnBoard.items())
        return tuple
