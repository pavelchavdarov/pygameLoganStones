from _collections import defaultdict

import pygame
from pygame import Rect
from pygame import Surface
from math import *
from pygame.math import Vector2
from Model import Model
from Stone.Stone import StoneBuilder
from resources import _STONE_COLOR
from Pouch.PouchModel import PouchModel
from Groups.Players import Player
from Groups.Players import PlayerDispatcher
from Events.event_dict import MOUSE_EVENTS
from Events.event_dict import CHANGE_TURN_EVENT
from Events.event_dict import STONE_SELECTED_EVENT
from Events.event_dict import FOCUS_OFF_EVENT, FOCUS_ON_EVENT
from Events.utils import post_event
from Groups.GameBoard import GameBoard
from Settings import *

import sys
pi2 = 2 * pi


class Controller:

    def __init__(self, model=None):
        self.model = model
        self.pouch = None

        self.done = False
        self.cell_radius = CELL_RADIUS
        self.drag = False
        self.drag_pos = None
        self.drag_stone = None
        self.avatar = None

        self.Screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HIGHT])
        pygame.display.set_caption('Logan stones game')

        board_image = Surface((2*WINDOW_WIDTH, 2*WINDOW_HIGHT))
        self.board = GameBoard(board_image, Rect(2*BORDER_WIDTH + PLAYER_WIDTH, BORDER_WIDTH, BOARD_WIDTH, BOARD_HIGHT))

        self.centr = self.board.area.center
        self.turn_dispatcher = PlayerDispatcher(Player(Rect(BORDER_WIDTH, BORDER_WIDTH,
                                                            PLAYER_WIDTH, PLAYER_HIGHT), 0),
                                                Player(Rect(3*BORDER_WIDTH + PLAYER_WIDTH + BOARD_WIDTH, BORDER_WIDTH,
                                                            PLAYER_WIDTH, PLAYER_HIGHT), 1)
                                                )

        self.stone_builder = StoneBuilder()

    def _calc_pos(self, mouse_pos):
        # расстояние до точки клика по hex-осям X и Y
        delta_x = (mouse_pos[0] - self.centr[0]) / cos(pi / 6)
        delta_y = (mouse_pos[1] - self.centr[1]) + delta_x * sin(pi / 6)
        # расстояние в клетках по X и Y
        hex_x = round(delta_x / (2 * CELL_RADIUS))
        hex_y = round(delta_y / (2 * CELL_RADIUS))
        # расстояние до центра клетки, в которую попал клик
        cell_x = hex_x * 2 * CELL_RADIUS
        cell_y = hex_y * 2 * CELL_RADIUS

        # координвты для отрисовки в обычных координатах
        return {"draw_pos": (self.centr[0] + cell_x * cos(pi / 6), self.centr[1] + cell_y - cell_x * sin(pi / 6)),
                "cell_pos": (hex_x, hex_y)}

    def set_model(self, model):
        self.model = model

    def set_pouch(self, pouch):
        self.pouch = pouch

    # deprecated
    def _put_stone(self, pos, stone_model, group):
        # stone_model = self.pouch.get_stone()
        if stone_model:
            self.stone_builder.set_position(pos["draw_pos"]).set_group(group).set_stone_model(stone_model).build()

    # deprecated
    def _move_stone_to_pos(self, stone, pos):
        self.Screen.fill((0, 0, 0), stone.get_rect())
        stone.move_to(pos["draw_pos"])

    def start(self):
        self.pouch.shake()
        # раздача фишек
        x = [CELL_RADIUS*1.5, WINDOW_WIDTH-CELL_RADIUS*1.5]
        y = 2.5*CELL_RADIUS
        i = 0

        rect_list = []
        init_list = []
        self.pouch.shake()
        for stone in self.pouch.stones:
            self.pouch.shake()
            if self.pouch.get_value() > 1:
                current_player = self.turn_dispatcher.current_player
                self._put_stone({"draw_pos": (x[i], y)}, stone, current_player)
                y += 100 * i
                i = (i+1) % 2
                self.turn_dispatcher.pass_turn()
            else:
                init_list.append(self.stone_builder.set_stone_model(stone).build())
        rect_list.extend(self.turn_dispatcher.current_player.draw(self.Screen))
        self.turn_dispatcher.pass_turn()
        rect_list.extend(self.turn_dispatcher.current_player.draw(self.Screen))
        self.turn_dispatcher.pass_turn()

        self.board.init_board(*init_list)
        rect_list.extend(self.board.draw(self.board.Screen))
        pygame.display.update(rect_list)

        while not self.done:
            for event in pygame.event.get():
                if rect_list:
                    rect_list.clear()
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type in MOUSE_EVENTS:
                    if self.board.is_hover(event.pos):
                        self.board.process_event(event)
                    elif self.turn_dispatcher.current_player.is_hover(event.pos):
                        self.turn_dispatcher.current_player.process_event(event)
                elif event.type == CHANGE_TURN_EVENT:
                    self.turn_dispatcher.process_event(event)
                elif event.type in (STONE_SELECTED_EVENT, pygame.KEYDOWN, pygame.KEYUP):
                    self.board.process_event(event)
                elif event.type in (FOCUS_OFF_EVENT, FOCUS_ON_EVENT):
                    event.recipient.process_event(event)

            self.board.scroll_board()
            pygame.display.update()

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    cntrl = Controller()
    model = Model()

    cntrl.set_model(model)
    cntrl.set_pouch(PouchModel(list(_STONE_COLOR)))

    cntrl.start()
