from _collections import defaultdict

from pygame.sprite import RenderUpdates, LayeredUpdates
from pygame import Rect
import pygame
from Settings import CELL_RADIUS
from Events.event_dict import STONE_SELECTED_EVENT
from Events.event_dict import CHANGE_TURN_EVENT
from Events.event_dict import FOCUS_OFF_EVENT
from Events.event_dict import FOCUS_ON_EVENT
from Events.utils import post_event, create_event
from Groups.GameArea import GameArea


class Player(GameArea):

    def __init__(self, area: Rect, index):
        super().__init__(area)
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
            pygame.MOUSEMOTION: lambda event: self._on_mouse_move(event.rel),
            FOCUS_ON_EVENT: lambda event: self._on_focus_on(),
            FOCUS_OFF_EVENT: lambda event: self._on_focus_off()

        })

    def collide_pos(self, pos):
        clicked_sprites = list(filter(lambda sprite: sprite.is_over(pos), self.sprites_list))
        return clicked_sprites[0] if clicked_sprites else None

    # def is_hover(self, pos):
    #     return self.area.collidepoint(pos[0], pos[1])

    def process_event(self, event):
        self.rect_list = []
        self.event_processor[event.type](event)

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

    def _on_turn_over(self):
        self._hide_border()

    def _on_focus_off(self):
        self._hide_border()
        self.update()
        self.rect_list = self.draw(self.Screen)

    def _on_focus_on(self):
        self._show_border()
        self.update()
        self.rect_list = self.draw(self.Screen)


class PlayerDispatcher:
    def __init__(self, *players):
        self.__players = players
        self.__players_amount = len(players)
        if self.__players_amount < 2:
            raise Exception('It must be 2 or more players!')

        self.__cur_player_idx = 0

        self.event_processor = defaultdict(lambda: lambda event: print("Unsupported event {}".format(event)))
        self.event_processor.update({
            # pygame.MOUSEBUTTONUP: lambda event: self._on_mouse_up(event.pos),
            # pygame.MOUSEBUTTONDOWN: lambda event: self._on_mouse_down(event.pos),
            # pygame.MOUSEMOTION: lambda event: self._on_mouse_move(event.rel),
            CHANGE_TURN_EVENT: lambda event: self.pass_turn(),
            # FOCUS_OFF_EVENT: lambda event: self._on_focus_off(),
            # FOCUS_ON_EVENT: lambda event: self._on_focus_on()

        })

    @property
    def current_player(self):
        return self.__players[self.__cur_player_idx]

    def pass_turn(self):
        self.current_player.process_event(create_event(FOCUS_OFF_EVENT))
        self.__cur_player_idx = (self.__cur_player_idx + 1) % self.__players_amount
        self.current_player.process_event(create_event(FOCUS_ON_EVENT))

    def process_event(self, event):
        self.event_processor[event.type](event)

    def _on_change_turn(self):
        self.current_player.process_event(create_event(FOCUS_OFF_EVENT))
        self.pass_turn()
        self.current_player.process_event(create_event(FOCUS_ON_EVENT))
