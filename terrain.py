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
    def __init__(self, space: pymunk.Space, mass: int, pos: pymunk.Vec2d, width: int, height: int, poly=None) -> None:
        """
        Initializer

        :param mass: mass of the car
        :param pos: initial position of the car
        :param poly: polygon representing the shape of the car, rectangle by default
        """

        image = pygame.Surface((width, height))

        GenericEntity.__init__(self, Sprite(pos, image), pos)
        self.space = space

        if poly is None:
            vertices = [self.sprite.rect.topleft - self.pos,
                        self.sprite.rect.topright - self.pos,
                        self.sprite.rect.bottomright - self.pos,
                        self.sprite.rect.bottomleft - self.pos]
        else:
            vertices = poly.exterior.coords

        self.body = pymunk.Body(mass, 0, body_type=pymunk.Body.STATIC)
        self.body.position = pos
        self.shape = pymunk.Poly(self.body, vertices)
        self.shape.collision_type = COLLTYPE_WALL

    def update(self) -> None:
        """
        Update the piece of terrain

        :return:
        """
        self.update_sprite()

    def update_sprite(self) -> None:
        """
        Update the sprite's location

        :return: None
        """
        self.sprite.rect = self.sprite.image.get_rect(center=self.screen_pos)


class BoundaryWall(Terrain):
    """
    A subclass of terrain used for the boundaries/edges of the map
    """
    def __init__(self, space: pymunk.Space, mass: int, pos: pymunk.Vec2d, width: int, height: int, poly=None) -> None:
        Terrain.__init__(self, space, mass, pos, width, height)
        self.sprite.image.fill(BLUE)


class CoverWall(Terrain):
    """
    A subclass of terrain used for smaller walls inside the map as cover
    """
    def __init__(self, space: pymunk.Space, mass: int, pos: pymunk.Vec2d, width: int, height: int, poly=None) -> None:
        Terrain.__init__(self, space, mass, pos, width, height)
        self.sprite.image.fill(YELLOW)


class ObstacleRock(Terrain):
    """
    A subclass of terrain used for rocks that stop cars but not projectiles
    """


