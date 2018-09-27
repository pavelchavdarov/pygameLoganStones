from pygame.sprite import RenderUpdates, LayeredUpdates
from pygame import Rect
import pygame
from pygame.math import Vector2
from math import cos, sin, pi


class PlayerGroup(RenderUpdates):

    def __init__(self, area: Rect, index):
        super().__init__()
        self.area = area
        self.direction = 1-2*index
        self.center = area.center
        self.Screen = pygame.display.get_surface()
        self.drag = False  # признак события перетаскивания (Drag-and-Drop)
        self.drag_pos = None  # позиция начала перетаскивания
        self.drag_stone = None
        self.selected_stone = None

    def collide_pos(self, pos):
        clicked_sprites = list(filter(lambda sprite: sprite.is_clicked(pos), self.sprites()))
        return clicked_sprites[0] if clicked_sprites else None

    def is_clicked(self, pos):
        return self.area.collidepoint(pos[0], pos[1])

    def process_event(self, event):
        # print('{}: process_event'.format(self.__class__.__name__))
        rect_list = []
        if event.type == pygame.MOUSEBUTTONUP:
            rect_list = self._on_mouse_up(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            rect_list = self._on_mouse_down(event.pos)

        elif event.type == pygame.MOUSEMOTION:
            rect_list = self._on_mouse_move(event.rel)

        pygame.display.update(rect_list)
        return self.selected_stone

    def _move_stone_to_pos(self, stone, pos):
        self.Screen.fill((0, 0, 0), stone.rect)
        stone.move_to(pos)

    def _on_mouse_down(self, mouse_pos):
        buttons = pygame.mouse.get_pressed()
        stone = self.collide_pos(mouse_pos)
        if stone:
            if buttons[0]:
                if self.selected_stone:
                    center = self.selected_stone.rect.center
                    self._move_stone_to_pos(self.selected_stone, (center[0] - self.selected_stone.radius*self.direction,
                                                                  center[1]))
                if self.selected_stone == stone:
                    print("same stone")
                    self.selected_stone = None
                else:
                    self.selected_stone = stone
                    center = stone.rect.center
                    self._move_stone_to_pos(self.selected_stone, (center[0] + self.selected_stone.radius*self.direction,
                                                                  center[1]))
                # начинаем перетаскиваниекамня
                # if not self.drag:
                #     self.drag_pos = stone.Center  # self._calc_pos(pygame.mouse.get_pos())
                #     self.drag = True
                #     self.drag_stone = stone
            elif buttons[2]:
                stone.flip()

            print("stone={}; selected_stone={}".format(stone.rect,self.selected_stone.rect if self.selected_stone else None))
        else:
            if self.selected_stone:
                center = self.selected_stone.rect.center
                self._move_stone_to_pos(self.selected_stone, (center[0] - self.selected_stone.radius*self.direction,
                                                              center[1]))
            self.selected_stone = None
        self.update()
        return self.draw(self.Screen)

    def _on_mouse_move(self, rel_pos):
        pass
        # if self.drag:
        #     pos = Vector2(self.drag_stone.Center) + Vector2(rel_pos)
        #     self._move_stone_to_pos(self.drag_stone, (pos.x,pos.y))
        #     return self.draw(self.Screen)

    def _on_mouse_up(self, mouse_pos):
        pass
        # if self.drag:
        #     self.drag = False