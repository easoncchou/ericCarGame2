import pygame

import game
from physics_object import *


class Car(PhysicsObject):
    """
    Car class
    """

    sprite: pygame.sprite.Sprite

    def __init__(self, mass: int, moi: int,
                 size: tuple[int, int], pivot: tuple[int, int]) -> None:
        """
        Initializer
        """

        super().__init__(mass, moi, size, pivot)
        self.sprite = game.Sprite(size[0], size[1], (0, 0, 0))   # change color later
