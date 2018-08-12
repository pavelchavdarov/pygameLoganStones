import pygame
from math import *
from Model import Model
from Stone.Stone import Stone
from Stone.Stone import StoneAvatar
from resources import _STONE_COLOR
from Pouch.PouchModel import PouchModel
from Player.PlayerModel import PlayerDispatcher

from Groups.BoardGroup import BoardGroup

import sys
pi2 = 2 * pi


class Controller:

    def __init__(self, model=None):
        self.model = model
        self.pouch = None

        self.done = False
        self.cell_radius = 30
        self.centr = (400, 330)
        self.drag = False
        self.drag_pos = None
        self.drag_stone = None
        self.avatar = None

        self.board_group = BoardGroup(self.centr, self.cell_radius)  # pygame.sprite.RenderUpdates()
        self.players = PlayerDispatcher()
        # self.player1_group = pygame.sprite.RenderUpdates()
        # self.player2_group = pygame.sprite.RenderUpdates()

        self.Screen = pygame.display.set_mode((800, 720))

        pygame.display.set_caption('Logan stones game')

    def _calc_pos(self, mouse_pos):
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

    def set_pouch(self, pouch):
        self.pouch = pouch

    # depricated
    def _put_stone(self, pos, stone_model, group):
        # stone_model = self.pouch.get_stone()
        if stone_model:
            # model.put_stone(pos["cell_pos"], Stone(self.cell_radius, pos["draw_pos"], group, stone_model))
            Stone(self.cell_radius, pos["draw_pos"], group, stone_model)

    def _move_stone_to_pos(self, stone, pos):
        self.Screen.fill((0, 0, 0), stone.get_rect())
        stone.move_to(pos["draw_pos"])

    def _onMouseDown(self):
        buttons = pygame.mouse.get_pressed()
        pos = self._calc_pos(pygame.mouse.get_pos())
        if buttons[0]:
            # если камня нет, то поставим
            # if model.get_stone(pos["cell_pos"]) is None:
                # self._put_stone(pos)
                # pass
            if model.get_stone(pos["cell_pos"]):
                # иначе начинаем перетаскиваниекамня
                if not self.drag:
                    self.drag_pos = pos # self._calc_pos(pygame.mouse.get_pos())
                    self.drag = True
                    self.avatar = StoneAvatar(model.get_stone(self.drag_pos["cell_pos"]))
        elif buttons[2]:
            stone = model.get_stone(pos["cell_pos"])
            if stone:
                stone.flip()
        self.board_group.update()
        return self.board_group.draw(self.Screen)

    def _onMouseUp(self):
        pos = self._calc_pos(pygame.mouse.get_pos())
        if self.drag:
            self.drag = False
            # если камня нет, то переместим его
            if self.model.get_stone(pos["cell_pos"]) is None:
                drag_stone = self.model.get_stone(self.drag_pos["cell_pos"])
                self._move_stone_to_pos(drag_stone, pos)
                self.model.move_stone(self.drag_pos["cell_pos"], pos["cell_pos"])
            # удаляем аватар
            self.avatar.remove(self.board_group)
            self.board_group.update()
            return self.board_group.draw(self.Screen)

    def _on_mouse_move(self):
        if self.drag:
            pos = self._calc_pos(pygame.mouse.get_pos())
            if self.model.get_stone(pos["cell_pos"]) is None:
                self._move_stone_to_pos(self.avatar, pos)
                return self.board_group.draw(self.Screen)
            else:
                self._move_stone_to_pos(self.avatar, self.drag_pos)
                return self.board_group.draw(self.Screen)

    def start(self):
        self.pouch.shake()
        # раздача фишек
        x = [40, 760]
        y = 60
        i = 0

        rect_list = []

        for stone in self.pouch.stones:
            self.pouch.shake()
            if self.pouch.get_value() > 1:
                current_player = self.players.current_player
                self._put_stone(self._calc_pos((x[i], y)), stone, current_player.get_batch())
                if i:
                    y += 60
                i = (i+1) % 2
                rect_list.extend(current_player.get_batch().draw(self.Screen))
            else:
                game_board = self.board_group
                self._put_stone(self._calc_pos((self.centr[0], self.centr[1] +
                                                self.pouch.get_value()*2*self.cell_radius)), stone, game_board)
                rect_list.extend(game_board.draw(self.Screen))
        pygame.display.update(rect_list)



        while not self.done:
            for event in pygame.event.get():
                if rect_list:
                    rect_list.clear()
                if event.type == pygame.constants.QUIT:
                    self.done = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    rect_list = self._onMouseUp()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    rect_list = self._onMouseDown()
                elif event.type == pygame.MOUSEMOTION:
                    rect_list = self._on_mouse_move()
                pygame.display.update(rect_list)

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    cntrl = Controller()
    model = Model()

    cntrl.set_model(model)
    cntrl.set_pouch(PouchModel(list(_STONE_COLOR)))

    cntrl.start()
