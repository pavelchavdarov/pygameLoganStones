import pygame
from math import *
from Model import Model
from Stone.Stone import Stone
from Stone.Stone import StoneAvatar
from resources import _STONE_ENTITY_3
from Stone.StoneModel import StoneModel
from Pouch.PouchModel import PouchModel

from random import randint

import sys
pi2 = 2 * pi


class Controller:

    def __init__(self, model=None, view=None):
        self.model = model
        self.view = view
        self.done = False
        self.cell_radius = 30
        self.centr = (400, 330)

        self.board_group = pygame.sprite.LayeredUpdates()

        self.Screen = pygame.display.set_mode((800, 720))

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

    def set_model(self, model):
        self.model = model

    def set_view(self, view):
        self.view = view

    def set_pouch(self, pouch):
        self.pouch = pouch

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
        stone_model = self.pouch.get_stone()
        if stone_model:
            model.put_stone(pos["cell_pos"], Stone(self.cell_radius, pos["draw_pos"], self.board_group, stone_model))

    def start(self):
        self.pouch.shake()

        pos = {"draw_pos": self.centr}
        pos.update({"cell_pos": (0, 0)})
        self._put_stone(pos)

        pos["draw_pos"] = (self.centr[0], self.centr[1] + 2 * self.cell_radius)
        pos["cell_pos"] = (0, 1)
        self._put_stone(pos)

        rect_list = self.board_group.draw(self.Screen)
        pygame.display.update(rect_list)

        drag = False
        drag_pos = None
        while not self.done:
            for event in pygame.event.get():

                if event.type == pygame.constants.QUIT:
                    self.done = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = self._get_screen_pos(pygame.mouse.get_pos())
                    if drag:
                        drag = False
                        self.Screen.fill((0, 0, 0), avatar.get_rect())
                        self.Screen.fill((0, 0, 0), drag_stone.get_rect())

                        # если камня нет, то переместим его
                        if model.get_stone(pos["cell_pos"]) is None:
                            model.move_stone(drag_pos["cell_pos"], pos["cell_pos"])
                            drag_stone.move_to(pos["draw_pos"])
                        avatar.remove(self.board_group)
                        self.board_group.update()
                        rect_list = self.board_group.draw(self.Screen)
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
                                drag_stone = model.get_stone(drag_pos["cell_pos"])
                                avatar = StoneAvatar(drag_stone)#drag_stone.get_avatar()
                    elif buttons[2]:
                        stone = model.get_stone(pos["cell_pos"])
                        if stone:
                            stone.flip()
                    self.board_group.update()
                    rect_list = self.board_group.draw(self.Screen)
                elif event.type == pygame.MOUSEMOTION:
                    if drag:
                        pos = self._get_screen_pos(pygame.mouse.get_pos())
                        if model.get_stone(pos["cell_pos"]) is None:
                            old_rect = avatar.get_rect()

                            avatar.move_to(pos["draw_pos"])
                            self.Screen.fill((0, 0, 0), old_rect)

                            rect_list = self.board_group.draw(self.Screen)

                pygame.display.update(rect_list)

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    cntrl = Controller()
    model = Model()

    cntrl.set_model(model)
    cntrl.set_pouch(PouchModel(list(_STONE_ENTITY_3)))

    cntrl.start()
