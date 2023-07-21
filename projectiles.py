import pymunk
import pygame
import math

from constants import *
from entities import GenericEntity, HealthEntity
from sprite import Sprite


class Projectile(GenericEntity):
    """
    Projectile fired from a weapon
    """

    body: pymunk.Body
    shape: pymunk.Shape
    damage: float
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

        self.damage = damage

        if poly is None:
            vertices = [self.sprite.rect.topleft - self.pos,
                        self.sprite.rect.topright - self.pos,
                        self.sprite.rect.bottomright - self.pos,
                        self.sprite.rect.bottomleft - self.pos]
        else:
            vertices = poly.exterior.coords

        self.body = pymunk.Body(0.1, 1000)
        self.body.position = pos
        self.body.velocity = pymunk.Vec2d(0, speed).rotated(-a_pos)
        self.body.angle = -a_pos

        self.shape = pymunk.Poly(self.body, vertices)
        self.shape.collision_type = COLL_PROJ

        self.shape.ent = self

    def update_sprite(self) -> None:
        """
        Update the sprite

        :return: None
        """

        self.sprite.image = pygame.transform.rotate(self.sprite.original_image,
                                                    -self.body.rotation_vector.angle_degrees)
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

    target: HealthEntity
    tracking: float       # how well a rocket can adjust its trajectory in order to hit the target

    def __init__(self, damage: float, pos: pymunk.Vec2d, speed: int, a_pos: float,
                 image: pygame.image, target: HealthEntity, tracking: float, poly=None):
        """
        Initializer

        :param damage:
        :param mass:
        :param pos:
        :param speed:
        :param a_pos:
        :param image:
        :param target:
        :param tracking:
        :param poly:
        """
        Projectile.__init__(self, damage, pos, speed, a_pos, image, poly)

        self.target = target
        self.tracking = tracking

    def track(self) -> None:
        """
        Adjust the trajectory of the rocket based on the target's current position

        :return: None
        """

        rocket_angle = - (self.body.angle + math.pi / 2)
        displacement_vec = (self.target.pos - self.pos)
        displacement_angle = (math.pi - displacement_vec.angle)
        difference_angle = (displacement_angle - rocket_angle) % (2 * math.pi)

        if difference_angle > math.pi:
            self.body.angle -= self.tracking / 2
            self.body.velocity = self.body.velocity.rotated(- (self.tracking / 2))
        elif difference_angle == math.pi:
            pass
        else:
            self.body.angle += self.tracking / 2
            self.body.velocity = self.body.velocity.rotated(self.tracking / 2)

    def update(self) -> None:
        """
        Updates the rocket every tick and adjusts its body angle based on the track function
        :return: None
        """

        self.pos = self.body.position
        Projectile.update(self)
        if self.target is not None:
            self.track()




