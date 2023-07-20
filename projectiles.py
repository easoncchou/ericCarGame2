import pymunk
import pygame

from constants import *
from entities import GenericEntity
from sprite import Sprite


class Projectile(GenericEntity):
    """
    Projectile fired from a weapon
    """

    body: pymunk.Body
    shape: pymunk.Shape
    damage: float
    mass: int
    pos: pymunk.Vec2d

    def __init__(self, damage: float, pos: pymunk.Vec2d, speed: int,
                 a_pos: float, image: pygame.image, poly=None) -> None:
        """
        Initializer

        :param mass: mass of projectile
        :param damage: damage done by the projectile when it collides with a target
        :param mass: mass of the projectile
        :param pos: a list of two integers representing the x and y coordinates of the projectile
        :param speed: the speed at which the projectile will travel at
        :param a_pos: the angular position of the projectile, in radians
        :param image: a pygame image of the projectile's sprite currently loaded in main
        :param poly: polygon representing the shape of the projectile, rectangle by default
        """

        GenericEntity.__init__(self, Sprite(pos, image), pos, a_pos)

        pos = pymunk.Vec2d(pos[0], pos[1])

        if poly is None:
            vertices = [self.sprite.rect.topleft - self.pos,
                        self.sprite.rect.topright - self.pos,
                        self.sprite.rect.bottomright - self.pos,
                        self.sprite.rect.bottomleft - self.pos]
        else:
            vertices = poly.exterior.coords

        body = pymunk.Body(0.1, 1000)
        body.position = pos
        body.velocity = pymunk.Vec2d(0, speed).rotated(-a_pos)
        body.angle = -a_pos
        shape = pymunk.Poly(body, vertices)
        shape.collision_type = COLL_PROJ

        self.body = body
        self.shape = shape
        self.damage = damage

        # rotate the sprite to match the weapon
        self.sprite.image = pygame.transform.rotate(self.sprite.original_image,
                                                    -self.body.rotation_vector.angle_degrees)

    def update_sprite(self) -> None:
        """
        Update the sprite

        :return: None
        """

        self.sprite.rect = self.sprite.image.get_rect(center=self.body.position)

    def collide_bounds(self) -> None:
        """
        Checks if the projectile is out of bounds

        :return: None
        """
        outer_bound = 100

        return self.body.position.x <= -outer_bound or \
            self.body.position.x > MAP_WIDTH + outer_bound or \
            self.body.position.y <= -outer_bound or \
            self.body.position.y > MAP_HEIGHT + outer_bound

    def update(self) -> None:
        """
        Updates the entity every tick
        :return: None
        """

        self.update_sprite()


class Bullet(Projectile):
    """
    Projectile fired by a machine gun
    """


class Laser(Projectile):
    """
    Projectile fired by a laser cannon
    """


class Rocket(Projectile):
    """
    Projectile fired by a rocket launcher
    """
