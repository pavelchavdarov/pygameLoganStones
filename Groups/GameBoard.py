import os
from _collections import defaultdict

import pygame
from pygame import Rect
from pygame.math import Vector2
from pygame import Surface
from math import cos, sin, pi
from Model import Model

from Events.event_dict import CHANGE_TURN_EVENT
from Events.event_dict import STONE_SELECTED_EVENT
from Events.event_dict import FOCUS_OFF_EVENT, FOCUS_ON_EVENT
from Events.event_dict import MOUSE_EVENTS
from Events.utils import post_event

from Stone.Stone import Stone, Avatar
from resources import _STONE_AVATAR
from Settings import *
from Groups.GameArea import GameArea

from pygame import image as image_loader

cos_pi_6 = cos(pi / 6)
sin_pi_6 = sin(pi / 6)


class GameBoard(GameArea):

    def __init__(self, screen: Surface, area: Rect):
        super().__init__(area)
        self.area = area

        # self.frame_center = Vector2(area.center)
        self.frame_center = Vector2(area.width/2, area.height/2)
        self.board_vector = Vector2(area.x, area.y)
        self.cell_radius = CELL_RADIUS
        self.model = Model()
        self.Screen = screen  # pygame.display.get_surface()
        self.drag = False  # признак события перетаскивания (Drag-and-Drop)
        self.drag_pos = None  # позиция начала перетаскивания
        self.drag_stone = None
        self.rect_list = []
        image = image_loader.load(os.path.join('resources', _STONE_AVATAR))
        self.avatar_sprite = Avatar().set_image(image)  # .set_rect(pos=(0, 0))
        self.stone_selected = False

        self.scroll_x = int(WINDOW_WIDTH/2)
        self.scroll_y = int(WINDOW_HIGHT/2)
        self.scroll_vector = Vector2(int(WINDOW_WIDTH/2), int(WINDOW_HIGHT/2))
        self.add(self.border_image)

        self.event_processor = defaultdict(lambda: lambda event: print("Unsupported event {}".format(event)))
        self.event_processor.update({
            pygame.MOUSEBUTTONUP: lambda event: self._on_mouse_up(event.pos),
            pygame.MOUSEBUTTONDOWN: lambda event: self._on_mouse_down(event.pos),
            pygame.MOUSEMOTION: lambda event: self._on_mouse_move(event.pos),
            STONE_SELECTED_EVENT: lambda event: self._on_avatar_change(event.selected),
            FOCUS_OFF_EVENT: lambda event: self._on_focus_off(),
            FOCUS_ON_EVENT: lambda event: self._on_focus_on()
        })

    def draw(self, surface):
        rect_list = super().draw(surface)
        pygame.display.get_surface().blit(self.Screen,
                                          # (2*BORDER_WIDTH + PLAYER_WIDTH, BORDER_WIDTH),
                                          (self.area.left, self.area.top),
                                          Rect(self.scroll_x, self.scroll_y, BOARD_WIDTH, BOARD_HIGHT))
                                          # (0, 0, BOARD_WIDTH, BOARD_HIGHT))
        # rect_list.append(Rect(self.scroll_x, self.scroll_y, BOARD_WIDTH, BOARD_HIGHT))
        rect_list.append(self.area)
        return rect_list

    def _calc_pos(self, mouse_pos):
        # расстояние до точки клика по hex-осям X и Y
        delta_x = (mouse_pos[0] - self.frame_center[0] + self.scroll_x) / cos_pi_6
        delta_y = (mouse_pos[1] - self.frame_center[1] + self.scroll_y) + delta_x * sin_pi_6
        # delta_x = (mouse_pos[0] + self.scroll_x) / cos_pi_6
        # delta_y = (mouse_pos[1] + self.scroll_y) + delta_x * sin_pi_6

        # расстояние в клетках по X и Y
        hex_x = round(delta_x / (2 * self.cell_radius))
        hex_y = round(delta_y / (2 * self.cell_radius))
        # расстояние до центра клетки, в которую попал клик
        cell_x = hex_x * 2 * self.cell_radius
        cell_y = hex_y * 2 * self.cell_radius
        # запишем в модель

        # координаты для отрисовки в обычных координатах
        return {"draw_pos": (self.frame_center[0] + cell_x * cos_pi_6 + self.scroll_x,
                             self.frame_center[1] + cell_y - cell_x * sin_pi_6 + self.scroll_y),
                "cell_pos": (hex_x, hex_y)}

    def _move_stone_to_pos(self, stone, pos):
        self.Screen.fill((0, 0, 0), stone.rect)
        stone.move_to(pos["draw_pos"])

    def _on_mouse_down(self, mouse_pos):
        buttons = pygame.mouse.get_pressed()
        pos = self._calc_pos(mouse_pos)
        stone = self.model.get_stone(pos["cell_pos"])
        if buttons[0]:
            if stone:
                # начинаем перетаскиваниекамня
                if not self.drag:
                    self.drag_pos = pos # self._calc_pos(pygame.mouse.get_pos())
                    self.drag = True
                    self.drag_stone = stone
        elif buttons[2]:
            if stone:
                stone.flip()
        self.update()
        self.rect_list = self.draw(self.Screen)

    def _on_mouse_up(self, mouse_pos):
        pos = self._calc_pos(mouse_pos)
        if self.drag:
            self.drag = False
            # если камня нет, то переместим его
            if self.model.get_stone(pos["cell_pos"]) is None:
                self.model.move_stone(self.drag_pos["cell_pos"], pos["cell_pos"])
            self.update()
            post_event(CHANGE_TURN_EVENT)
            self.rect_list = self.draw(self.Screen)

    def _on_mouse_move(self, mouse_pos):
        pos = self._calc_pos(mouse_pos)
        stone = self.model.get_stone(pos["cell_pos"])
        if self.drag:
            if stone is None or stone == self.drag_stone:
                self._move_stone_to_pos(self.drag_stone, pos)
                self.update()
                self.rect_list = self.draw(self.Screen)
            else:
                pass
                #self._move_stone_to_pos(self.avatar, self.drag_pos)
                #return self.draw(self.Screen)
        elif self.avatar_sprite.groups:
            if stone is None:
                if self.stone_selected:
                    self.avatar_sprite.set_group(self)
                    self._move_stone_to_pos(self.avatar_sprite, pos)
                    self.update()
                    self.rect_list = self.draw(self.Screen)

    def _on_focus_off(self):
        if self.avatar_sprite.groups():
            self.avatar_sprite.remove(self)
        self._hide_border()
        self.update()
        self.rect_list = self.draw(self.Screen)

    def _on_focus_on(self):
        self._show_border()
        self.update()
        self.rect_list = self.draw(self.Screen)

    def _on_avatar_change(self, selected):
        self.stone_selected = selected
        # self.rect_list = self.draw(self.Screen)
        if self.avatar_sprite.groups():
            self.avatar_sprite.remove(self)
        # if selected:
        #     self.avatar_sprite.set_group(self)
        # else:
        #     self.avatar_sprite.remove(self)
        # self.Screen.fill((0, 0, 0), self.avatar_sprite.rect)
        # self.rect_list = self.draw(self.Screen)

    # def is_over(self, pos):
    #     return self.area.collidepoint(pos[0], pos[1])

    def collide_pos(self, mouse_pos):
        pos = self._calc_pos(mouse_pos)
        return self.model.get_stone(pos["sell_pos"])

    def add(self, *sprites):

        super().add(*sprites)
        for spr in sprites:
            if isinstance(spr, Stone):
                spr.rect = spr.rect.move(-self.board_vector).move(self.scroll_x, self.scroll_y)
                pos = self._calc_pos(spr.Center)
                self.model.put_stone(pos["cell_pos"], spr)
            else:
                spr.rect = spr.rect.move(self.scroll_x, self.scroll_y).move(-self.board_vector)

    # def add_internal(self, sprite):
    #     super().add_internal(sprite)
    #     sprite.rect = sprite.rect.move(-self.board_vector)
    #     if isinstance(sprite, Stone):
    #         pos = self._calc_pos(sprite.Center)
    #         sprite_rect = sprite.get_rect()
    #         sprite_rect.top = pos["draw_pos"][1]
    #         sprite_rect.left = pos["draw_pos"][0]
    #         sprite.rect = sprite_rect
    #         self.model.put_stone(pos["cell_pos"], sprite)

    def remove_internal(self, sprite):
        super().remove_internal(sprite)
        if isinstance(sprite, Stone):
            pos = self._calc_pos(sprite.Center)
            self.Screen.fill((0, 0, 0), sprite.rect)
            self.model.remove_stone(pos["cell_pos"])

    def process_event(self, event):
        self.rect_list = []
        if event.type in MOUSE_EVENTS:
            # event.pos = (event.pos[0] - (2*BORDER_WIDTH + PLAYER_WIDTH), event.pos[1] - BORDER_WIDTH)
            event.pos = event.pos - self.board_vector + self.scroll_vector
        self.event_processor[event.type](event)
        pygame.display.update(self.rect_list)

    # TODO:
    #  1) что-то не так с центром фишки
    #  2) при перетаскивании фишка пропадает --- blit и scroll