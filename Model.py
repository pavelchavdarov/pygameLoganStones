
class Model:
    def __init__(self):
        self.__StonesOnBoard = {}
        #self.Pouch = []


    def putStone(self, position, stone):
        if position not in self.__StonesOnBoard:
            self.__StonesOnBoard[position] = stone
            #print(self.__StonesOnBoard.keys())
            return 0
        return 1

    def getBoard(self):
        board = tuple(self.__StonesOnBoard.items())
        return board
