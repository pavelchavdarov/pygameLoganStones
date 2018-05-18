import pygame
from math import *
from Model import Model


class Controler:

    def __init__(self, model=None):
        self.model = model
        self.done = False
        self.cell_radius = 30
        self.color = (64, 128, 255)
        self.pos_Descart = None;
        self.centr = (150, 150)
        self.screen = None

    def init(self, resolution):
        pygame.init()
        self.screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption('Logan stones game')

    def setModel(self, model):
        self.model = model

    def draw_ngon(self, Surface, color, n, radius, position):
        pi2 = 2 * pi
        return pygame.draw.lines(Surface,
                                 color,
                                 True,
                                 [(cos(i / n * pi2) * radius / cos(pi / 6) + position[0],
                                   sin(i / n * pi2) * radius / cos(pi / 6) + position[1]) for i in range(0, n)]
                                 )

    def start(self):

        self.draw_ngon(self.screen, self.color, 6, self.cell_radius - 1, self.centr)
        self.draw_ngon(self.screen,
                       self.color,
                       6,
                       self.cell_radius - 1,
                       (self.centr[0], self.centr[1] + 2 * self.cell_radius)
                       )

        while not self.done:
            for event in pygame.event.get():

                if event.type == pygame.constants.QUIT:
                    self.done = True
                elif event.type == pygame.MOUSEBUTTONUP:

                    pos = pygame.mouse.get_pos()
                    DELTA_X = (pos[0] - self.centr[0]) / cos(pi / 6)
                    DELTA_Y = (pos[1] - self.centr[1]) + DELTA_X * sin(pi / 6)

                    HEX_X = round(DELTA_X / (2 * self.cell_radius))
                    HEX_Y = round(DELTA_Y / (2 * self.cell_radius))

                    CELL_X = HEX_X * 2 * self.cell_radius
                    CELL_Y = HEX_Y * 2 * self.cell_radius

                    if model.putStone((CELL_X, CELL_Y), 'stone_%s_%s' % (CELL_X, CELL_Y)) == 1:
                        None

                    pos = (self.centr[0] + CELL_X * cos(pi / 6),
                           self.centr[1] + CELL_Y - CELL_X * sin(pi / 6))
                    self.draw_ngon(self.screen, self.color, 6, self.cell_radius - 1, pos)

            pygame.display.update()

        pygame.quit()
        sys.exit()


if (__name__ == '__main__'):
    cntrl = Controler()
    model = Model()
    cntrl.setModel(model)
    cntrl.init((400, 300))
    cntrl.start()
