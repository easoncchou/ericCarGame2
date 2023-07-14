import pygame


class Sprite(pygame.sprite.Sprite):
    """
    PyGame Sprite class
    """

    def __init__(self, pos: tuple[int, int], image: pygame.image):
        """
        Initializer

        :param pos: position (x, y)
        :param image: image
        """
        # Call superclass constructor
        super().__init__()

        # Image
        self.image = image

        # make the space created from rotation transparent
        self.image = self.image.convert_alpha()

        # set the position of the center of the image to pos[]
        self.rect = self.image.get_rect(center=self.image.get_rect(center=(pos[0], pos[1])).center)

        # keep the original image for updating orientation using pygame.transform.rotate
        self.original_image = self.image
