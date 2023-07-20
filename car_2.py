import pymunk
import pygame

from weapon import Weapon
from entities import HealthEntity
from sprite import Sprite


class Car2(HealthEntity):
    """
    A physics based car using a bicycle model (one wheel in front and one wheel in back)
    """

    space: pymunk.Space
    car_body: pymunk.Body
    car_body_shape: pymunk.Shape
    front_wheel = pymunk.Body
    back_wheel = pymunk.Body
    front_wheel_groove: pymunk.GrooveJoint
    back_wheel_groove: pymunk.GrooveJoint
    pos: pymunk.Vec2d
    sprite: Sprite
    wep: Weapon

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

        self.space = space

        if poly is None:
            vertices = [self.sprite.rect.topleft - self.pos,
                        self.sprite.rect.topright - self.pos,
                        self.sprite.rect.bottomright - self.pos,
                        self.sprite.rect.bottomleft - self.pos]
        else:
            vertices = poly.exterior.coords

        moment = pymunk.moment_for_poly(mass, vertices)

        car_body = pymunk.Body(mass, moment)
        car_body.position = pos
        car_body_shape = pymunk.Poly(car_body, vertices)

        # set it to a very high moment so that it simulates front/back movement
        front_wheel = pymunk.Body(1, 166666)
        # set the position of the front wheel
        front_wheel.position = pos + pymunk.Vec2d(0, 40)
        # use a square to simulate the contact between the wheel/ground
        front_wheel_shape = pymunk.Circle(front_wheel, 0)

        # set it to a very high moment so that it simulates front/back movement
        back_wheel = pymunk.Body(1, 166666)
        # set the position of the front wheel
        back_wheel.position = pos + pymunk.Vec2d(0, -40)
        # use a square to simulate the contact between the wheel/ground
        back_wheel_shape = pymunk.Circle(back_wheel, 0)

        # attach wheel to the body with a pivot joint
        front_pivot = pymunk.PivotJoint(car_body, front_wheel, front_wheel.position)
        back_pivot = pymunk.PivotJoint(car_body, back_wheel, back_wheel.position)

        # create groove joints
        front_wheel_groove = pymunk.GrooveJoint(self.space.static_body,
                                                front_wheel,
                                                front_wheel.position - pymunk.Vec2d(0, 20).rotated(front_wheel.angle),
                                                front_wheel.position + pymunk.Vec2d(0, 20).rotated(front_wheel.angle),
                                                (0, 0))

        back_wheel_groove = pymunk.GrooveJoint(self.space.static_body,
                                               back_wheel,
                                               back_wheel.position - pymunk.Vec2d(0, 20).rotated(back_wheel.angle),
                                               back_wheel.position + pymunk.Vec2d(0, 20).rotated(back_wheel.angle),
                                               (0, 0))

        self.car_body = car_body
        self.car_body_shape = car_body_shape

        self.front_wheel = front_wheel
        # self.front_wheel_shape = front_wheel_shape
        self.back_wheel = back_wheel
        # self.back_wheel_shape = back_wheel_shape

        # self.front_pivot = front_pivot
        # self.back_pivot = back_pivot
        self.front_wheel_groove = front_wheel_groove
        self.back_wheel_groove = back_wheel_groove

        # add everything to the space
        self.space.add(car_body, car_body_shape)
        self.space.add(front_wheel, front_wheel_shape)
        self.space.add(back_wheel, back_wheel_shape)
        self.space.add(front_pivot)
        self.space.add(back_pivot)
        self.space.add(front_wheel_groove)
        self.space.add(back_wheel_groove)

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

        # move the front wheel angle to the correct position gradually
        if self.front_wheel.angle < self.car_body.angle + th:
            self.front_wheel.angle += 0.03
        else:
            self.front_wheel.angle -= 0.03

    def accelerate(self, mag: float) -> None:
        """
        Accelerate the car with mag magnitude

        :param mag: magnitude at which to accelerate
        :return: None
        """

        # apply a force to the back wheel (RWD)
        self.back_wheel.apply_force_at_local_point((0, mag))

    def update_grooves(self) -> None:
        """
        Updates the groove joints that define the car's movement
        :return: None
        """

        # remove the grooves
        self.space.remove(self.front_wheel_groove)
        self.space.remove(self.back_wheel_groove)

        # modify the grooves
        self.front_wheel_groove = pymunk.GrooveJoint(self.space.static_body,
                                                     self.front_wheel,
                                                     self.front_wheel.position - pymunk.Vec2d(0, 20).rotated(self.front_wheel.angle),
                                                     self.front_wheel.position + pymunk.Vec2d(0, 20).rotated(self.front_wheel.angle),
                                                     (0, 0))

        self.back_wheel_groove = pymunk.GrooveJoint(self.space.static_body,
                                                    self.back_wheel,
                                                    self.back_wheel.position - pymunk.Vec2d(0, 20).rotated(self.back_wheel.angle),
                                                    self.back_wheel.position + pymunk.Vec2d(0, 20).rotated(self.back_wheel.angle),
                                                    (0, 0))

        # replace the grooves
        self.space.add(self.front_wheel_groove)
        self.space.add(self.back_wheel_groove)

    def update_sprite(self) -> None:
        """
        Update the sprite

        :return: None
        """

        self.sprite.image = pygame.transform.rotate(self.sprite.original_image,
                                                    -self.car_body.rotation_vector.angle_degrees)
        self.sprite.rect = self.sprite.image.get_rect(center=self.car_body.position)

    def update(self) -> None:
        """
        Updates the entity every tick
        :return: None
        """

        HealthEntity.update(self)
        self.pos = self.car_body.position
        self.back_wheel.angle = self.car_body.angle
        self.update_grooves()
        self.update_sprite()
        self.wep.update()
        self.hp_bar.update()
        self.wep.pos = self.pos
