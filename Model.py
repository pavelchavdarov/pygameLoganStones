
class Model:
    def __init__(self):
        self.__StonesOnBoard = dict()
        #self.Pouch = []


    def put_stone(self, position, stone):
        if position not in self.__StonesOnBoard:
            self.__StonesOnBoard[position] = stone
            print(self.__StonesOnBoard.keys())
            return 0
        return 1

    def get_stone(self, position):
        if position in self.__StonesOnBoard:
            return self.__StonesOnBoard[position]
        else:
            return None

    def getBoard(self):
        board = tuple(self.__StonesOnBoard.items())
        return board
