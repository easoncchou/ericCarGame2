import pygame

from physics_object import *
from sprite import *


class Car(PhysicsObject):
    """
    Car class
    """

    sprite: Sprite

    def __init__(self, mass: int, moi: int,
                 size: tuple[int, int], pivot: tuple[int, int]) -> None:
        """
        Initializer
        """

        super().__init__(mass, moi, size, pivot)
        self.sprite = Sprite(size[0], size[1], (0, 0), (0, 0, 0))
