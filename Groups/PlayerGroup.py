from pygame.sprite import RenderUpdates, LayeredUpdates
from math import cos, sin, pi


class PlayerGroup(RenderUpdates):

    def click(self, pos):
        clicked_sprites = list(filter(lambda sprite: sprite.click(pos), self.sprites()))
        return clicked_sprites[0] if clicked_sprites else None


