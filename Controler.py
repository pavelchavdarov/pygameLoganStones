import pygame
from math import *
from Model import Model
from View import GameView


class Controler:

    def __init__(self, model=None, view=None):
        self.model = model
        self.view = view
        self.done = False
        self.cell_radius = 30
        self.color = (64, 128, 255)
        self.pos_Descart = None;
        self.centr = (150, 150)
        self.screen = None

    def init(self):
        None

    def set_model(self, model):
        self.model = model

    def set_view(self, view):
        self.view = view

    '''def draw_ngon(self, Surface, color, n, radius, position):
        pi2 = 2 * pi
        return pygame.draw.lines(Surface,
                                 color,
                                 True,
                                 [(cos(i / n * pi2) * radius / cos(pi / 6) + position[0],
                                   sin(i / n * pi2) * radius / cos(pi / 6) + position[1]) for i in range(0, n)]
                                 )
    '''

    def start(self):

        #self.draw_ngon(self.screen, self.color, 6, self.cell_radius - 1, self.centr)
        '''        self.draw_ngon(self.screen,
                       self.color,
                       6,
                       self.cell_radius - 1,
                       (self.centr[0], self.centr[1] + 2 * self.cell_radius)
                       )
        '''
        self.view.drawStone(self.centr)
        self.view.drawStone((self.centr[0], self.centr[1] + 2 * self.cell_radius))
        while not self.done:
            for event in pygame.event.get():

                if event.type == pygame.constants.QUIT:
                    self.done = True
                elif event.type == pygame.MOUSEBUTTONUP:

                    mouse_pos = pygame.mouse.get_pos()
                    deltaX = (mouse_pos[0] - self.centr[0]) / cos(pi / 6)
                    deltaY = (mouse_pos[1] - self.centr[1]) + deltaX * sin(pi / 6)

                    hexX = round(deltaX / (2 * self.cell_radius))
                    hexY = round(deltaY / (2 * self.cell_radius))

                    cellX = hexX * 2 * self.cell_radius
                    cellY = hexY * 2 * self.cell_radius

                    if model.putStone((cellX, cellY), 'stone_%s_%s' % (cellX, cellY)) == 1:
                        None

                    pos = (self.centr[0] + cellX * cos(pi / 6),
                           self.centr[1] + cellY - cellX * sin(pi / 6))
                    #self.draw_ngon(self.screen, self.color, 6, self.cell_radius - 1, pos)
                    self.view.drawStone(pos)

            pygame.display.update()

        pygame.quit()
        sys.exit()


if (__name__ == '__main__'):
    cntrl = Controler()
    model = Model()
    view = GameView((400, 300), cntrl.cell_radius-1)

    cntrl.set_model(model)
    cntrl.set_view(view)

    cntrl.init()
    cntrl.start()
