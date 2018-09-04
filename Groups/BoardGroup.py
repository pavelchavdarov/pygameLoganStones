import pygame
from pygame.sprite import RenderUpdates
from pygame import Rect
from math import cos, sin, pi
from Model import Model

from Events.event_dict import CHANGE_TURN_EVENT

cos_pi_6 = cos(pi / 6)
sin_pi_6 = sin(pi / 6)


class BoardGroup(RenderUpdates):

    def __init__(self, area: Rect, cell_radius):
        super().__init__()
        self.area = area
        self.center = area.center
        self.cell_radius = cell_radius
        self.model = Model()
        self.Screen = pygame.display.get_surface()
        self.drag = False  # признак события перетаскивания (Drag-and-Drop)
        self.drag_pos = None  # позиция начала перетаскивания
        self.drag_stone = None

    def _calc_pos(self, mouse_pos):
        # расстояние до точки клика по hex-осям X и Y
        delta_x = (mouse_pos[0] - self.center[0]) / cos_pi_6
        delta_y = (mouse_pos[1] - self.center[1]) + delta_x * sin_pi_6
        # расстояние в клетках по X и Y
        hex_x = round(delta_x / (2 * self.cell_radius))
        hex_y = round(delta_y / (2 * self.cell_radius))
        # расстояние до центра клетки, в которую попал клик
        cell_x = hex_x * 2 * self.cell_radius
        cell_y = hex_y * 2 * self.cell_radius
        # запишем в модель

        # координаты для отрисовки в обычных координатах
        return {"draw_pos": (self.center[0] + cell_x * cos_pi_6, self.center[1] + cell_y - cell_x * sin_pi_6),
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
        return self.draw(self.Screen)

    def _on_mouse_up(self, mouse_pos):
        pos = self._calc_pos(mouse_pos)
        if self.drag:
            self.drag = False
            # если камня нет, то переместим его
            if self.model.get_stone(pos["cell_pos"]) is None:
                self.model.move_stone(self.drag_pos["cell_pos"], pos["cell_pos"])
            self.update()
            event = pygame.event.Event(CHANGE_TURN_EVENT)
            pygame.event.post(event)
            return self.draw(self.Screen)

    def _on_mouse_move(self, mouse_pos):
        if self.drag:
            pos = self._calc_pos(mouse_pos)
            stone = self.model.get_stone(pos["cell_pos"])
            if stone is None or stone == self.drag_stone:
                self._move_stone_to_pos(self.drag_stone, pos)
                return self.draw(self.Screen)
            else:
                pass
                #self._move_stone_to_pos(self.avatar, self.drag_pos)
                #return self.draw(self.Screen)

    def is_clicked(self, pos):
        return self.area.collidepoint(pos[0], pos[1])

    def collide_pos(self, mouse_pos):
        pos = self._calc_pos(mouse_pos)
        return self.model.get_stone(pos["sell_pos"])

    def add(self, *sprites):
        super().add(*sprites)
        for spr in sprites:
            pos = self._calc_pos(spr.Center)
            self.model.put_stone(pos["cell_pos"], spr)

    def add_internal(self, sprite):
        super().add_internal(sprite)
        pos = self._calc_pos(sprite.Center)
        self.model.put_stone(pos["cell_pos"], sprite)

    def remove_internal(self, sprite):
        super().remove_internal(sprite)
        pos = self._calc_pos(sprite.Center)
        self.model.remove_stone(pos["cell_pos"])

    def process_event(self, event):
        # print('BoardGroup: ' + str(event.type))
        rect_list = []
        if event.type == pygame.MOUSEBUTTONUP:
            rect_list = self._on_mouse_up(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            rect_list = self._on_mouse_down(event.pos)

        elif event.type == pygame.MOUSEMOTION:
            rect_list = self._on_mouse_move(event.pos)

        pygame.display.update(rect_list)
