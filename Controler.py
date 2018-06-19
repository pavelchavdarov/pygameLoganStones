import pygame
from math import *
from Model import Model
from View import images

from Stone import Stone
from resources import _STONE_SIDES_3

from random import randint

pi2 = 2 * pi
class Controler:

    def __init__(self, model=None, view=None):
        self.model = model
        self.view = view
        self.done = False
        self.cell_radius = 30
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

    def _mark_stone(self, pos):
        if self.model.marked_stone:
            # переключили маркер
            if model.marked_stone != pos["cell_pos"]:
                model.get_stone(model.marked_stone).mark()
                model.get_stone(pos["cell_pos"]).mark()
                model.marked_stone = pos["cell_pos"]
            # сняли маркер
            else:
                model.get_stone(model.marked_stone).mark()
                model.marked_stone = None
        # если ничего не выбрано
        else:
            stone = model.get_stone(pos["cell_pos"])
            if stone:
                stone.mark()
                model.marked_stone = pos["cell_pos"]

    def _put_stone(self, pos):
        rand_side = randint(0,2)
        stone = Stone(self.cell_radius, pos["draw_pos"], self.board_group, (_STONE_SIDES_3[rand_side],
                                                                            _STONE_SIDES_3[(rand_side+randint(1, 2)) % 2]))
        model.put_stone(pos["cell_pos"], stone)

    def start(self):
        rand_side = randint(0, 2)
        stone = Stone(self.cell_radius, self.centr, self.board_group, (_STONE_SIDES_3[rand_side],
                                                                       _STONE_SIDES_3[(rand_side+randint(1, 2)) % 2]))
        model.put_stone((0, 0), stone)

        second_pos = (self.centr[0], self.centr[1] + 2 * self.cell_radius)
        rand_side = randint(0, 2)
        stone = Stone(self.cell_radius, second_pos, self.board_group, (_STONE_SIDES_3[rand_side],
                                                                       _STONE_SIDES_3[(rand_side+randint(1, 2)) % 2]))
        model.put_stone((0, 1), stone)
        #self.board_group.update()
        rect_list = self.board_group.draw(self.Screen)

        pygame.display.update(rect_list)

        drag = False
        drag_pos = None
        while not self.done:
            last_pos = None
            for event in pygame.event.get():
                # print("event: {}".format(event))

                if event.type == pygame.constants.QUIT:
                    self.done = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = self._get_screen_pos(pygame.mouse.get_pos())
                    if drag:
                        drag = False
                        # если камня нет, то переместим его
                        if model.get_stone(pos["cell_pos"]) is None:
                            model.move_stone(drag_pos["cell_pos"], pos["cell_pos"])
                        elif last_pos:
                            drag_stone.move_to(drag_pos["draw_pos"])
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    buttons = pygame.mouse.get_pressed()
                    pos = self._get_screen_pos(pygame.mouse.get_pos())
                    if buttons[0]:
                        # если камня нет, то поставим
                        if model.get_stone(pos["cell_pos"]) is None:
                            self._put_stone(pos)
                        else:
                            # иначе начинаем перетаскиваниекамня
                            if not drag:
                                drag_pos = self._get_screen_pos(pygame.mouse.get_pos())
                                drag = True
                    elif buttons[2]:
                        stone = model.get_stone(pos["cell_pos"])
                        if stone:
                            stone.flip()
                    self.board_group.update()
                    rect_list = self.board_group.draw(self.Screen)
                elif event.type == pygame.MOUSEMOTION:
                    if drag:
                        pos = self._get_screen_pos(pygame.mouse.get_pos())
                        last_pos = pos.copy()
                        drag_stone = model.get_stone(drag_pos["cell_pos"])
                        if model.get_stone(pos["cell_pos"]) is None:
                            old_rect = drag_stone.get_rect()
                            drag_stone.move_to(pos["draw_pos"])
                            self.Screen.fill((0, 0, 0), old_rect)
                        # self.board_group.update()

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
