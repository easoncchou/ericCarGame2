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
        Initializer

        :param pos: initial position
        :param max_hp: max health
        :param image: image
        :param poly: polygon
        """

        HealthEntity.__init__(self, Sprite(pos, image), max_hp, pos)

        if poly is None:
            vertices = [self.sprite.rect.topleft - self.pos,
                        self.sprite.rect.topright - self.pos,
                        self.sprite.rect.bottomright - self.pos,
                        self.sprite.rect.bottomleft - self.pos]
        else:
            vertices = poly.exterior.coords

        self.body = pymunk.Body(1000, 100000)
        self.body.position = pos

        self.shape = pymunk.Poly(self.body, vertices)
        self.shape.collision_type = COLL_ENEM

        self.shape.ent = self

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


class MovingTarget(Target):
    """
    A Target that moves between point A and point B
    """

    def __init__(self, p_a: pymunk.Vec2d, p_b: pymunk.Vec2d, max_hp: int, image: pygame.image, poly=None):
        """
        Initializer

        :param pos: initial position
        :param max_hp: max health
        :param image: image
        :param poly: polygon
        """

        Target.__init__(self, p_a, max_hp, image, poly)

        self.p_a = p_a
        self.p_b = p_b
        self.dest = p_b
        self.speed = 100

        self.body.position = p_a

    def update(self) -> None:
        """
        Updates the entity every tick

        :return:
        """

        self.body.velocity = (self.dest - self.body.position).normalized() * self.speed

        # if the current position gets close enough to the destination
        if abs(self.body.position - self.dest) <= 1:
            # switch the points
            if self.dest == self.p_a:
                self.dest = self.p_b
            else:
                self.dest = self.p_a

        Target.update(self)
