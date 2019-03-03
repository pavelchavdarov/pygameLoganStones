from pygame.sprite import Sprite, RenderUpdates
from pygame import Rect
from pygame import Surface
from pygame import draw


class GameBorder(Sprite):
    def __init__(self, area: Rect):
        super().__init__()
        self.rect = area
        self.__inner_rect = Rect(0, 0, area.width, area.height)
        self.border_image = Surface((area.width, area.height))
        self.border_image.set_colorkey((0, 0, 0))

        self.image = self.border_image

    def update(self, *args):
        self.image = self.border_image

    def show(self):
        draw.rect(self.border_image, (63, 72, 204), self.__inner_rect, 2)

    def hide(self):
        draw.rect(self.border_image, (88, 88, 88), self.__inner_rect, 2)


class GameArea(RenderUpdates):
    def __init__(self, area: Rect):
        super().__init__()
        self.border_image = GameBorder(area)
        self.area = area

    def _show_border(self):
        self.border_image.show()
        pass


    def _hide_border(self):
        self.border_image.hide()
        pass

    @property
    def sprites_list(self):
        return [sprite for sprite in self.sprites() if sprite != self.border_image]
        # return self.sprites()

    def is_hover(self, pos):
        return self.area.collidepoint(pos[0], pos[1])