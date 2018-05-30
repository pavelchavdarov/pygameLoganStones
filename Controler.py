import pygame
from math import *
from Model import Model
from View import GameView

from Stone import Stone

pi2 = 2 * pi
class Controler:

    def __init__(self, model=None, view=None):
        self.model = model
        self.view = view
        self.done = False
        self.cell_radius = 20
        self.centr = (150, 150)

        pygame.init()

        self.board_group = pygame.sprite.LayeredUpdates()

        self.Screen = pygame.display.set_mode((400, 300))

        pygame.display.set_caption('Logan stones game')

    def _get_screen_pos(self, mouse_pos):
        # расстояние до точки клика по hex-осям X и Y
        delta_x = (mouse_pos[0] - self.centr[0]) / cos(pi / 6)
        delta_y = (mouse_pos[1] - self.centr[1]) + delta_x * sin(pi / 6)
        # расстояние в клетках по X и Y
        hex_x = round(delta_x / (2 * self.cell_radius))
        hex_y = round(delta_y / (2 * self.cell_radius))
        # расстояние до центра клетки, в которую попал клик
        cell_x = hex_x * 2 * self.cell_radius
        cell_y = hex_y * 2 * self.cell_radius
        # запишем в модель

        # координвты для отрисовки в ообычных координатах
        return {"draw_pos": (self.centr[0] + cell_x * cos(pi / 6), self.centr[1] + cell_y - cell_x * sin(pi / 6)),
                "cell_pos": (hex_x, hex_y)}


    def init(self):
        None

    def set_model(self, model):
        self.model = model

    def set_view(self, view):
        self.view = view

    '''def draw_ngon(self, Surface, color, n, radius, position):
        pi2 = 2 * pi
        return pygame.draw.lines(Surface,
                                 color,
                                 True,
                                 [(cos(i / n * pi2) * radius / cos(pi / 6) + position[0],
                                   sin(i / n * pi2) * radius / cos(pi / 6) + position[1]) for i in range(0, n)]
                                 )
    '''

    def drawStone(self, position):
        lines = [(cos(i / 6 * pi2) * self.cell_radius / cos(pi / 6) + position[0],
                  sin(i / 6 * pi2) * self.cell_radius / cos(pi / 6) + position[1])
                 for i in range(0, 6)]
        color = (64, 128, 255)
        pygame.draw.lines(self.Screen, color, True, lines)

    def start(self):

        #self.draw_ngon(self.screen, self.color, 6, self.cell_radius - 1, self.centr)
        '''        self.draw_ngon(self.screen,
                       self.color,
                       6,
                       self.cell_radius - 1,
                       (self.centr[0], self.centr[1] + 2 * self.cell_radius)
                       )
        '''
        #self.view.drawStone(self.centr)
        #self.view.drawStone((self.centr[0], self.centr[1] + 2 * self.cell_radius))

        stone = Stone(self.cell_radius, self.centr, self.board_group, ("rock", "papper"))
        model.put_stone((0, 0), stone)

        second_pos = (self.centr[0], self.centr[1] + 2 * self.cell_radius)
        stone = Stone(self.cell_radius, second_pos, self.board_group, ("rock", "papper"))
        model.put_stone((0, 1), stone)
        self.board_group.update()
        rect_list = self.board_group.draw(self.Screen)

        pygame.display.update(rect_list)

        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.constants.QUIT:
                    self.done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    buttons = pygame.mouse.get_pressed()
                    pos = self._get_screen_pos(pygame.mouse.get_pos())
                    if buttons[0]:
                        # if pos["cell_pos"] not in model.getBoard():
                        if model.get_stone(pos["cell_pos"]) is None:
                            stone = Stone(self.cell_radius, pos["draw_pos"], self.board_group, ("rock", "papper"))
                            model.put_stone(pos["cell_pos"], stone)
                    elif buttons[2]:
                        stone = model.get_stone(pos["cell_pos"])
                        if stone:
                            stone.flip()

                    self.board_group.update()
                    rect_list = self.board_group.draw(self.Screen)

            pygame.display.update(rect_list)

        pygame.quit()
        sys.exit()


if (__name__ == '__main__'):
    cntrl = Controler()
    model = Model()
    #view = GameView((400, 300), cntrl.cell_radius-1)

    cntrl.set_model(model)
#    cntrl.set_view(view)

    cntrl.init()
    cntrl.start()
