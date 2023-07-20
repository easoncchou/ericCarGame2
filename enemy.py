import pymunk
import pygame

from constants import *
from entities import HealthEntity
from sprite import Sprite


class Target(HealthEntity):
    """
    A stationary target with hp
    """

    body: pymunk.Body
    shape: pymunk.Shape
    sprite: Sprite
    max_hp: int
    hp: int

    def __init__(self, pos: pymunk.Vec2d, max_hp: int, image: pygame.image, poly=None):
        """

        :param game:
        :param pos:
        :param max_hp:
        :param image:
        :param poly:
        """

        HealthEntity.__init__(self, Sprite(pos, image), max_hp, pos)

        if poly is None:
            vertices = [self.sprite.rect.topleft - self.pos,
                        self.sprite.rect.topright - self.pos,
                        self.sprite.rect.bottomright - self.pos,
                        self.sprite.rect.bottomleft - self.pos]
        else:
            vertices = poly.exterior.coords

        body = pymunk.Body(1000, 100000)
        body.position = pos
        shape = pymunk.Poly(body, vertices)
        shape.collision_type = COLL_ENEM

        self.body = body
        self.shape = shape

    def update_sprite(self) -> None:
        """
        Update the sprite

        :return: None
        """

        self.sprite.image = pygame.transform.rotate(self.sprite.original_image,
                                                    -self.body.rotation_vector.angle_degrees)
        self.sprite.rect = self.sprite.image.get_rect(center=self.body.position)

    def update(self) -> None:
        """
        Updates the entity every tick

        :return: None
        """

        self.pos = self.body.position
        HealthEntity.update(self)
        self.update_sprite()
