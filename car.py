import pygame

from physics_object import *
from sprite import *


class Car(PhysicsObject):
    """
    Car class
    """

    mass: int
    moi: int
    size: tuple[int, int]
    lever_arm: int
    pos: list[int, int]
    vel: float
    a_pos: float
    a_vel: float
    sprite: Sprite

    def __init__(self, mass: int, moi: int,
                 size: tuple[int, int], lever_arm: int) -> None:
        """
        Initializer

        :param mass: mass of the car
        :param moi: moment of inertia of the car
        :param size: size of the car
        :param lever_arm: length of the lever arm of the car
        """

        super().__init__(mass, moi, size, lever_arm)
        self.sprite = Sprite(size[0], size[1], (0, 0), BLACK)

    def update_sprite(self) -> None:
        """
        Update the sprite

        :return: None
        """

        self.sprite.image = pygame.transform.rotate(self.sprite.original_image, ((180 / math.pi) * self.a_pos))

        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.x = self.pos[0]
        self.sprite.rect.y = self.pos[1]
