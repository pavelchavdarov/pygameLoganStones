from pygame.sprite import RenderUpdates, LayeredUpdates
from pygame import Rect
import pygame

from math import cos, sin, pi


class PlayerGroup(RenderUpdates):

    def __init__(self, area: Rect):
        super().__init__()
        self.area = area

    def collide_pos(self, pos):
        clicked_sprites = list(filter(lambda sprite: sprite.is_clicked(pos), self.sprites()))
        return clicked_sprites[0] if clicked_sprites else None

    def is_clicked(self, pos):
        return self.area.collidepoint(pos[0], pos[1])

    def process_event(self, event):
        rect_list = []
        if event.type == pygame.MOUSEBUTTONUP:
            rect_list = self._on_mouse_up(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            rect_list = self._on_mouse_down(event.pos)

        elif event.type == pygame.MOUSEMOTION:
            rect_list = self._on_mouse_move(event.pos)

        pygame.display.update(rect_list)

    def _on_mouse_down(self, mouse_pos):
        buttons = pygame.mouse.get_pressed()
        stone = self.collide_pos(mouse_pos)
        if stone:
            print("x={}, y={}, stone={}".format(stone.Center[0], stone.Center[1], stone))

    def _on_mouse_move(self, mouse_pos):
        pass

    def _on_mouse_up(self, mouse_pos):
        pass