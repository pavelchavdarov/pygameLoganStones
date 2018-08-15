from pygame.sprite import RenderUpdates, LayeredUpdates
from pygame import Rect
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
        # print('PlayerGroup: ' + str(event.type))
        pass


