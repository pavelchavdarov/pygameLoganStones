from _collections import defaultdict

from pygame.sprite import RenderUpdates, LayeredUpdates
from pygame import Rect
import pygame
from Settings import CELL_RADIUS
from Events.event_dict import STONE_SELECTED_EVENT
from Events.event_dict import CHANGE_TURN_EVENT
from Events.utils import post_event

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
        self.rect_list = []

        self.event_processor = defaultdict(lambda: lambda event: print("Unsupported event {}".format(event)))
        self.event_processor.update({
            pygame.MOUSEBUTTONUP: lambda event: self._on_mouse_up(event.pos),
            pygame.MOUSEBUTTONDOWN: lambda event: self._on_mouse_down(event.pos),
            pygame.MOUSEMOTION: lambda event: self._on_mouse_move(event.rel)
            CHANGE_TURN_EVENT: lambda event: self.turn_over()

        })
    def collide_pos(self, pos):
        clicked_sprites = list(filter(lambda sprite: sprite.is_over(pos), self.sprites()))
        return clicked_sprites[0] if clicked_sprites else None

    def is_clicked(self, pos):
        return self.area.collidepoint(pos[0], pos[1])

    def process_event(self, event):
        # print('{}: process_event'.format(self.__class__.__name__))
        self.rect_list = []
        self.event_processor[event.type](event)



        # if event.type == pygame.MOUSEBUTTONUP:
        #     self._on_mouse_up(event.pos)
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     self._on_mouse_down(event.pos)
        # elif event.type == pygame.MOUSEMOTION:
        #     self._on_mouse_move(event.rel)

        pygame.display.update(self.rect_list)

    def _move_stone_to_pos(self, stone, pos):
        self.Screen.fill((0, 0, 0), stone.rect)
        stone.move_to(pos)

    def _on_mouse_down(self, mouse_pos):
        buttons = pygame.mouse.get_pressed()
        stone = self.collide_pos(mouse_pos)
        if stone:
            if buttons[0]:
                if self.selected_stone:
                    rect = self.selected_stone.rect
                    self._move_stone_to_pos(self.selected_stone, (rect.centerx - CELL_RADIUS*self.direction,
                                                                  rect.centery))
                if self.selected_stone == stone:
                    self.selected_stone = None
                else:
                    self.selected_stone = stone
                    rect = stone.rect
                    self._move_stone_to_pos(self.selected_stone, (rect.centerx + CELL_RADIUS*self.direction,
                                                                  rect.centery))
                # начинаем перетаскиваниекамня
                # if not self.drag:
                #     self.drag_pos = stone.Center  # self._calc_pos(pygame.mouse.get_pos())
                #     self.drag = True
                #     self.drag_stone = stone
            elif buttons[2]:
                self.Screen.fill((0, 0, 0), stone.rect)
                stone.flip()

        else:
            if self.selected_stone:
                rect = self.selected_stone.rect
                self._move_stone_to_pos(self.selected_stone, (rect.centerx - CELL_RADIUS*self.direction,
                                                              rect.centery))
            self.selected_stone = None

        post_event(STONE_SELECTED_EVENT, {'selected': self.selected_stone is not None})
        # event = pygame.event.Event(STONE_SELECTED_EVENT, {'selected': self.selected_stone is not None})
        # pygame.event.post(event)
        self.update()
        self.rect_list = self.draw(self.Screen)

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

    def turn_over(self):
