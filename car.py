import pygame

from physics_object import *
from sprite import *


class Car(PhysicsObject):
    """
    Car class
    """

    mass: int
    size: tuple[int, int]
    pos: list[int, int]
    vel: float
    a_pos: float
    a_vel: float
    sprite: Sprite

    def __init__(self, mass: int, size: tuple[int, int], pos: list[int, int], handling: int, poly=None) -> None:
        """
        Initializer

        :param mass: mass of the car
        :param size: size of the car
        :param handling: how well a car steers/turns (the higher the value the faster it turns)
        :param poly: polygon representing the shape of the car, rectangle by default
        """

        self.sprite = Sprite(size[0], size[1], (0, 0), "assets/car1.png")

        # if poly is None, create polygon from rect
        if poly is None:
            corners = [
                (self.sprite.rect.topleft[0] + pos[0], self.sprite.rect.topleft[1] + pos[1]),
                (self.sprite.rect.topright[0] + pos[0], self.sprite.rect.topright[1] + pos[1]),
                (self.sprite.rect.bottomright[0] + pos[0], self.sprite.rect.bottomright[1] + pos[1]),
                (self.sprite.rect.bottomleft[0] + pos[0], self.sprite.rect.bottomleft[1] + pos[1])
            ]
            poly = Polygon(corners)

        super().__init__(mass, handling, pos, poly)

    def update_sprite(self) -> None:
        """
        Update the sprite

        :return: None
        """

        self.sprite.image = pygame.transform.rotate(self.sprite.original_image, ((180 / math.pi) * self.a_pos))
        self.sprite.rect = self.sprite.image.get_rect(center=self.sprite.image.get_rect(center=(self.pos[0], self.pos[1])).center)

