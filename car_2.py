import pymunk
import pygame
import math
from typing import Union

from weapon import Weapon
from entities import HealthEntity
from sprite import Sprite
from constants import *


class Car2(HealthEntity):
    """
    A physics based car using a bicycle model (one wheel in front and one wheel in back)
    """

    space: pymunk.Space
    body: pymunk.Body
    shape: pymunk.Shape
    front_wheel = pymunk.Body
    back_wheel = pymunk.Body
    front_wheel_groove: pymunk.GrooveJoint
    back_wheel_groove: pymunk.GrooveJoint
    pos: pymunk.Vec2d
    sprite: Sprite
    wep: Union[Weapon, None]

    def __init__(self, space: pymunk.Space, mass: int, pos: pymunk.Vec2d, max_hp: int, image: pygame.image, poly=None) -> None:
        """
        Initializer

        :param mass: mass of the car
        :param pos: initial position of the car
        :param max_hp: max health of the car
        :param image: the image for the sprite of the car
        :param poly: polygon representing the shape of the car, rectangle by default
        """

        HealthEntity.__init__(self, Sprite(pos, image), max_hp, pos)

        self.wep = None
        self.steering_angle = 0
        self.max_steering = math.pi / 6

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

        self.body = pymunk.Body(mass, moment)
        self.body.position = pos
        self.shape = pymunk.Poly(self.body, vertices)

        self.front_pivot_point = pymunk.Vec2d(0, 30)
        self.back_pivot_point = pymunk.Vec2d(0, -30)

        # create groove joints
        self.front_wheel_groove = pymunk.GrooveJoint(self.space.static_body,
                                                     self.body,
                                                     self.body.position + self.front_pivot_point - pymunk.Vec2d(0, 20).rotated(self.steering_angle),
                                                     self.body.position + self.front_pivot_point + pymunk.Vec2d(0, 20).rotated(self.steering_angle),
                                                     self.front_pivot_point)

        self.back_wheel_groove = pymunk.GrooveJoint(self.space.static_body,
                                                    self.body,
                                                    self.body.position + self.back_pivot_point - pymunk.Vec2d(0, 20).rotated(self.steering_angle),
                                                    self.body.position + self.back_pivot_point + pymunk.Vec2d(0, 20).rotated(self.steering_angle),
                                                    self.back_pivot_point)

        self.space.add(self.body, self.shape)
        self.space.add(self.front_wheel_groove)
        self.space.add(self.back_wheel_groove)

    def set_weapon(self, wep: Weapon) -> None:
        """
        Adds a weapon to this car

        :param wep: weapon to add
        :return: None
        """

        self.wep = wep

    def steer(self, th: float) -> None:
        """
        Steer the car th rads relative to the front of the car

        :param th: how much to turn the front wheel in rads
        :return: None
        """

        if self.steering_angle > self.max_steering:
            self.steering_angle = self.max_steering
        elif self.steering_angle < -self.max_steering:
            self.steering_angle = -self.max_steering

        # move the front wheel angle to the correct position gradually
        if self.steering_angle < th:
            self.steering_angle += 0.03
        else:
            self.steering_angle -= 0.03

    def accelerate(self, mag: float) -> None:
        """
        Accelerate the car with mag magnitude

        :param mag: magnitude at which to accelerate
        :return: None
        """

        # apply a force to the back wheel (RWD)

        body_a = (-self.body.rotation_vector.angle) % (2 * math.pi)
        body_v = (math.pi / 2 - self.body.velocity.angle) % (2 * math.pi)

        if abs(body_a - body_v) < math.pi / 2:
            # going forward
            if mag > 0:
                self.body.apply_force_at_local_point((0, mag), self.back_pivot_point)
            else:
                self.body.apply_force_at_local_point((0, 5 * mag), self.back_pivot_point)

        else:
            # going backwards
            if mag > 0:
                self.body.apply_force_at_local_point((0, 5 * mag), self.back_pivot_point)
            else:
                self.body.apply_force_at_local_point((0, mag), self.back_pivot_point)

    def update_grooves(self) -> None:
        """
        Updates the groove joints that define the car's movement
        :return: None
        """

        # remove the grooves
        self.space.remove(self.front_wheel_groove)
        self.space.remove(self.back_wheel_groove)
        # create groove joints
        self.front_wheel_groove = pymunk.GrooveJoint(self.space.static_body,
                                                     self.body,
                                                     self.body.position + self.front_pivot_point.rotated(self.body.rotation_vector.angle) - pymunk.Vec2d(0, 20).rotated(self.steering_angle + self.body.rotation_vector.angle),
                                                     self.body.position + self.front_pivot_point.rotated(self.body.rotation_vector.angle) + pymunk.Vec2d(0, 20).rotated(self.steering_angle + self.body.rotation_vector.angle),
                                                     self.front_pivot_point)

        self.back_wheel_groove = pymunk.GrooveJoint(self.space.static_body,
                                                    self.body,
                                                    self.body.position + self.back_pivot_point.rotated(self.body.rotation_vector.angle) - pymunk.Vec2d(0, 20).rotated(self.body.rotation_vector.angle),
                                                    self.body.position + self.back_pivot_point.rotated(self.body.rotation_vector.angle) + pymunk.Vec2d(0, 20).rotated(self.body.rotation_vector.angle),
                                                    self.back_pivot_point)

        # replace the grooves
        self.space.add(self.front_wheel_groove)
        self.space.add(self.back_wheel_groove)

    def update_sprite(self) -> None:
        """
        Update the sprite

        :return: None
        """

        center_screen = pymunk.Vec2d(MAP_WIDTH / 2 - 20, MAP_HEIGHT / 2 - 20)
        self.sprite.image = pygame.transform.rotate(self.sprite.original_image,
                                                    -self.body.rotation_vector.angle_degrees)
        self.sprite.rect = self.sprite.image.get_rect(center=self.screen_pos)

    def update(self) -> None:
        """
        Updates the entity every tick
        :return: None
        """

        HealthEntity.update(self)
        self.pos = self.body.position
        self.update_grooves()
        self.update_sprite()
        self.hp_bar.update()
        self.wep.pos = self.pos
        self.wep.car_pos = self.pos
        self.wep.find_relative_pos()
        self.wep.update()
