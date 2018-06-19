import pygame
from pygame.sprite import LayeredUpdates
from math import cos, sin, pi

pi2 = 2 * pi
images = {"rock": "resources/gem_blue.png", "scissors": "resources/gem_ellow.png", "papper": "resources/gem_green.png",
          "background": "resources/background.png"}

class GameView(LayeredUpdates):

    def __init__(self, resolution=None, radius=None):
        LayeredUpdates.__init__(self)

        self.Screen = pygame.display.set_mode(resolution)
        self.CellRadius = radius

        pygame.display.set_caption('Logan stones game')
        self.edgeAmount = 6


    def setCellRadius(self, radius):
        self.CellRadius = radius
    '''
    def drawStone(self, position):
        lines = [(cos(i / self.edgeAmount * pi2) * self.CellRadius / cos(pi / 6) + position[0],
                  sin(i / self.edgeAmount * pi2) * self.CellRadius / cos(pi / 6) + position[1])
                 for i in range(0, self.edgeAmount)]
        color = (64, 128, 255)
        pygame.draw.lines(self.Screen, color, True, lines)
    '''