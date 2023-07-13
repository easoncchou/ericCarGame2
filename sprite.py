import pygame


class Sprite(pygame.sprite.Sprite):
    """
    PyGame Sprite class
    """

    def __init__(self, w: int, h: int, pos: tuple[int, int],
                 color: tuple[int, int, int]):
        """
        Initializer

        :param w: width
        :param h: height
        :param pos: position (x, y)
        :param color: color (R, G, B)
        """
        # Call superclass constructor
        super().__init__()

        self.image = pygame.Surface([w, h])
        self.image.fill(color)
        self.rect = self.image.get_rect(center=self.image.get_rect(center=(pos[0], pos[1])).center)

        self.original_image = self.image
