import pymunk
import pygame
import math

from constants import *
from entities import GenericEntity, HealthEntity, Explosion
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

        self.shape.ent = self

    def update_sprite(self) -> None:
        """
        Update the sprite

        :return: None
        """

        self.sprite.image = pygame.transform.rotate(self.sprite.original_image,
                                                    -self.body.rotation_vector.angle_degrees)
        self.sprite.rect = self.sprite.image.get_rect(center=self.screen_pos)

    def update(self) -> None:
        """
        Updates the entity every tick
        :return: None
        """

        self.update_sprite()
        self.pos = self.body.position


class Bullet(Projectile):
    """
    Projectile fired by a machine gun
    """

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

        Projectile.__init__(self, damage, pos, speed, a_pos, image, poly)
        self.shape.collision_type = COLLTYPE_BULLETPROJ


class Rocket(Projectile):
    """
    Projectile fired by a rocket launcher
    """

    body: pymunk.Body
    shape: pymunk.Shape
    damage: float
    pos: pymunk.Vec2d
    target: HealthEntity
    tracking: float       # how well a rocket can adjust its trajectory in order to hit the target
    explosion_radius: float
    explosion_force: float

    def __init__(self, damage: float, explosion_radius: float, explosion_force: float, pos: pymunk.Vec2d, speed: int, a_pos: float,
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

        self.shape.collision_type = COLLTYPE_ROCKETPROJ
        self.target = target
        self.tracking = tracking
        self.explosion_radius = explosion_radius
        self.explosion_force = explosion_force

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

    def explode(self) -> Explosion:
        """
        Explode the rocket

        :return:
        """
        return Explosion(self.explosion_radius, self.pos)

    def update(self) -> None:
        """
        Updates the rocket every tick and adjusts its body angle based on the track function
        :return: None
        """

        self.pos = self.body.position
        Projectile.update(self)
        if self.target is not None:
            self.track()


class Laser(Projectile):
    """
    Projectile shot out by a LaserCannon; a beam that stops on contact
    """

    colour: [int, int, int]  # as of now the colour will be hardcoded

    def __init__(self, damage: float, pos: pymunk.Vec2d, a_pos: float, length: float, image: pygame.image, poly=None):
        """
        Initializer

        :param damage: damage done by the laser per tick
        :param pos: origin of the laser upon which rotation will be done
        :param a_pos: angular position of the laser
        :param image: image of single laser block that makes up the laser (not yet implemented this way; just a rect rn)
        :param poly: polygon of the laser used for collision/hit detection
        """

        f_image = pygame.surface.Surface([image.get_width(), length], pygame.SRCALPHA)

        # need to tile the image length // image.get_height() + 1 times
        for i in range(int(length // image.get_height()) + 1):
            f_image.blit(image, (0, i * image.get_height()))

        # create the sprite for the laser beam
        GenericEntity.__init__(self, Sprite(pos, f_image), pos, a_pos)

        self.damage = damage
        self.pos = pos
        self.a_pos = a_pos
        self.length = 0
        self.max_length = length
        self.block_image = image

        if poly is None:
            vertices = [self.sprite.rect.topleft - self.pos,
                        self.sprite.rect.topright - self.pos,
                        self.sprite.rect.bottomright - self.pos,
                        self.sprite.rect.bottomleft - self.pos]
        else:
            vertices = poly.exterior.coords

    def update_sprite(self) -> None:
        """
        Update the sprite

        :return: None
        """

        f_image = pygame.surface.Surface([self.block_image.get_width(), self.length], pygame.SRCALPHA)
        for i in range(int(self.length // self.block_image.get_height()) + 1):
            f_image.blit(self.block_image, (0, i * self.block_image.get_height()))

        self.sprite.original_image = f_image
        rot_off = pymunk.Vec2d(0, self.length / 2)
        offset_rotated = rot_off.rotated(-self.a_pos)

        self.sprite.image = pygame.transform.rotate(self.sprite.original_image, ((180 / math.pi) * self.a_pos))
        self.sprite.rect = self.sprite.image.get_rect(center=self.screen_pos + offset_rotated)

