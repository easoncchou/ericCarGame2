import pymunk
import pygame
import math

from constants import *
from sprite import Sprite
from entities import *


class Terrain(GenericEntity):
    """
    Terrain class containing obstacles and barriers
    """
    def __init__(self, space: pymunk.Space, mass: int, pos: pymunk.Vec2d, image: pygame.image, poly=None) -> None:
        """
        Initializer

        :param mass: mass of the car
        :param pos: initial position of the car
        :param image: the image for the sprite of the car
        :param poly: polygon representing the shape of the car, rectangle by default
        """

        GenericEntity.__init__(self, Sprite(pos, image))
        self.space = space

        if poly is None:
            vertices = [self.sprite.rect.topleft - self.pos,
                        self.sprite.rect.topright - self.pos,
                        self.sprite.rect.bottomright - self.pos,
                        self.sprite.rect.bottomleft - self.pos]
        else:
            vertices = poly.exterior.coords

        # make moment extra large to simulate proper movement
        moment = pymunk.moment_for_poly(mass, vertices) * 20

        self.body = pymunk.Body(mass, moment, 2)
        self.body.position = pos
        self.shape = pymunk.Poly(self.body, vertices)

    def handle_collision(self) -> None:
        """
        Handle collision between a piece of terrain and a car or projectile

        :return:
        """

        raise NotImplementedError


class BoundaryWall(Terrain):
    """
    A subclass of terrain used for the boundaries/edges of the map
    """


class CoverWall(Terrain):
    """
    A subclass of terrain used for smaller walls inside the map as cover
    """


class ObstacleRock(Terrain):
    """
    A subclass of terrain used for rocks that stop cars but not projectiles
    """


class MudPuddle(Terrain):
    """
    A subclass of terrain used for patches that slow down cars passing through
    """

