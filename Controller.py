import pygame
from pygame.event import Event
from math import *
from Model import Model
from Stone.Stone import StoneBuilder
from Stone.Stone import StoneMoveProvider
from resources import _STONE_COLOR
from Pouch.PouchModel import PouchModel
from Player.PlayerModel import PlayerDispatcher
from Events.event_dict import MOUSE_EVENTS
from Events.event_dict import CHANGE_TURN_EVENT
from Groups.BoardGroup import BoardGroup


import sys
pi2 = 2 * pi


class Controller:

    def __init__(self, model=None):
        self.model = model
        self.pouch = None

        self.done = False
        self.cell_radius = 30
        self.drag = False
        self.drag_pos = None
        self.drag_stone = None
        self.avatar = None

        self.Screen = pygame.display.set_mode((800, 720))
        pygame.display.set_caption('Logan stones game')

        self.board = BoardGroup(pygame.Rect(150, 0, 500, 720), self.cell_radius)  # pygame.sprite.RenderUpdates()
        self.centr = self.board.area.center
        self.players = PlayerDispatcher(pygame.Rect(0, 0, 150, 720), pygame.Rect(650, 0, 150, 720))

        self.stone_builder = StoneBuilder()
        self.stone_builder.set_move_provider(StoneMoveProvider()).set_radius(self.cell_radius)

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

        # координвты для отрисовки в обычных координатах
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
            self.stone_builder.set_position(pos["draw_pos"]).set_group(group).set_stone_model(stone_model).build()
            #Stone(self.cell_radius, pos["draw_pos"], group, stone_model)

    def _move_stone_to_pos(self, stone, pos):
        self.Screen.fill((0, 0, 0), stone.get_rect())
        stone.move_to(pos["draw_pos"])

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
                self._put_stone({"draw_pos":(x[i], y)}, stone, current_player.batch)
                print("x={} y={} stone = {}".format(x[i], y, stone))
                if i:
                    y += 60
                i = (i+1) % 2
                rect_list.extend(current_player.batch.draw(self.Screen))
                self.players.pass_turn()
            else:
                game_board = self.board
                self._put_stone(self._calc_pos((self.centr[0], self.centr[1] +
                                                self.pouch.get_value()*2*self.cell_radius)), stone, game_board)
                rect_list.extend(game_board.draw(self.Screen))
        pygame.display.update(rect_list)



        while not self.done:
            for event in pygame.event.get():
                if rect_list:
                    rect_list.clear()
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type in MOUSE_EVENTS:
                    if self.board.is_clicked(event.pos):
                        self.board.process_event(event)
                    elif self.players.current_player.batch.is_clicked(event.pos):
                        self.players.current_player.batch.process_event(event)
                elif event.type == CHANGE_TURN_EVENT:
                    self.players.pass_turn()
                #elif event.type == pygame.MOUSEBUTTONUP:
                #    rect_list = self._on_mouse_up(event.pos)
                #elif event.type == pygame.MOUSEBUTTONDOWN:
                #    rect_list = self._on_mouse_down(event.pos)
                #elif event.type == pygame.MOUSEMOTION:
                #    rect_list = self._on_mouse_move(event.pos)
                # pygame.display.update(rect_list)

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    cntrl = Controller()
    model = Model()

    cntrl.set_model(model)
    cntrl.set_pouch(PouchModel(list(_STONE_COLOR)))

    cntrl.start()
