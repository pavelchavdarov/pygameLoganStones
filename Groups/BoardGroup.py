from pygame.sprite import RenderUpdates, LayeredUpdates
from math import cos, sin, pi
from Model import Model

cos_pi_6 = cos(pi / 6)
sin_pi_6 = sin(pi / 6)


class BoardGroup(RenderUpdates):

    def __init__(self, centr_pos, cell_radius):
        super().__init__()
        self.centr = centr_pos
        self.cell_radius = cell_radius
        self.model = Model()

    def _calc_pos(self, mouse_pos):
        # расстояние до точки клика по hex-осям X и Y
        delta_x = (mouse_pos[0] - self.centr[0]) / cos_pi_6
        delta_y = (mouse_pos[1] - self.centr[1]) + delta_x * sin_pi_6
        # расстояние в клетках по X и Y
        hex_x = round(delta_x / (2 * self.cell_radius))
        hex_y = round(delta_y / (2 * self.cell_radius))
        # расстояние до центра клетки, в которую попал клик
        cell_x = hex_x * 2 * self.cell_radius
        cell_y = hex_y * 2 * self.cell_radius
        # запишем в модель

        # координаты для отрисовки в обычных координатах
        return {"draw_pos": (self.centr[0] + cell_x * cos_pi_6, self.centr[1] + cell_y - cell_x * sin_pi_6),
                "cell_pos": (hex_x, hex_y)}

    def click(self, mouse_pos):
        pos = self._calc_pos(mouse_pos)
        return self.model.get_stone(pos["sell_pos"])

    def add(self, *sprites):
        super().add(*sprites)
        for spr in sprites:
            pos = self._calc_pos(spr.Centr)
            self.model.put_stone(pos["cell_pos"], spr)

    def add_internal(self, sprite):
        super().add(sprite)
        pos = self._calc_pos(sprite.Centr)
        self.model.put_stone(pos["cell_pos"], sprite)