import pygame
from math import cos, sin, pi

pi2 = 2 * pi

class GameView:

    def __init__(self, resolution=None, radius=None):
        pygame.init()
        self.Screen = pygame.display.set_mode(resolution)
        self.CellRadius = radius

        pygame.display.set_caption('Logan stones game')
        self.edgeAmount = 6

    def setCellRadius(self, radius):
        self.CellRadius = radius

    def drawStone(self, position):
        lines = [(cos(i / self.edgeAmount * pi2) * self.CellRadius / cos(pi / 6) + position[0],
                  sin(i / self.edgeAmount * pi2) * self.CellRadius / cos(pi / 6) + position[1])
                 for i in range(0, self.edgeAmount)]
        color = (64, 128, 255)
        pygame.draw.lines(self.Screen, color, True, lines)
