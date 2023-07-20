import pymunk
import pygame

from game import Game
from weapon import Weapon
from entities import HealthEntity
from sprite import Sprite


class Car2(HealthEntity):
    """
    A physics based car using a bicycle model (one wheel in front and one wheel in back)
    """

    game: 'Game'
    body: pymunk.Body
    front_wheel = pymunk.Body
    back_wheel = pymunk.Body
    front_wheel_groove: pymunk.GrooveJoint
    back_wheel_groove: pymunk.GrooveJoint
    pos: list[int, int]
    sprite: Sprite
    wep: Weapon

    def __init__(self, game: 'Game', mass: int, pos: list[int], max_hp: int, image: pygame.image, poly=None) -> None:
        """
        Initializer

        :param game: game that the car belongs in
        :param mass: mass of the car
        :param pos: initial position of the car
        :param max_hp: max health of the car
        :param image: the image for the sprite of the car
        :param poly: polygon representing the shape of the car, rectangle by default
        """

        HealthEntity.__init__(self, game, pos, Sprite(pos, image), max_hp, (0, 0))

        pos = pymunk.Vec2d(pos[0], pos[1])

        if poly is None:
            vertices = [self.sprite.rect.topleft,
                        self.sprite.rect.topright,
                        self.sprite.rect.bottomright,
                        self.sprite.rect.bottomleft]
        else:
            vertices = poly.exterior.coords

        moment = pymunk.moment_for_poly(mass, vertices)

        car_body = pymunk.Body(mass, moment)
        car_body.position = pos
        car_body_shape = pymunk.Poly(car_body, vertices)

        # set it to a very high moment so that it simulates front/back movement
        front_wheel = pymunk.Body(1, 166666)
        # set the position of the front wheel
        front_wheel.position = pos + pymunk.Vec2d(0, 30)
        # use a square to simulate the contact between the wheel/ground
        front_wheel_shape = pymunk.Poly.create_box(front_wheel)

        # attach wheel to the body with a pivot joint
        front_pivot = pymunk.PivotJoint(car_body, front_wheel, front_wheel.position)

        # set it to a very high moment so that it simulates front/back movement
        back_wheel = pymunk.Body(1, 166666)
        # set the position of the front wheel
        back_wheel.position = pos + pymunk.Vec2d(0, -30)
        # use a square to simulate the contact between the wheel/ground
        back_wheel_shape = pymunk.Poly.create_box(back_wheel)

        # attach wheel to the body with a pivot joint
        back_pivot = pymunk.PivotJoint(car_body, back_wheel, back_wheel.position)

        # create groove joints
        front_wheel_groove = pymunk.GrooveJoint(self.game.space.static_body,
                                                front_wheel,
                                                front_wheel.position - pymunk.Vec2d(0, 20).rotated(front_wheel.angle),
                                                front_wheel.position + pymunk.Vec2d(0, 20).rotated(front_wheel.angle),
                                                (0, 0))

        back_wheel_groove = pymunk.GrooveJoint(self.game.space.static_body,
                                               back_wheel,
                                               back_wheel.position - pymunk.Vec2d(0, 20).rotated(back_wheel.angle),
                                               back_wheel.position + pymunk.Vec2d(0, 20).rotated(back_wheel.angle),
                                               (0, 0))

        # add everything to the space
        game.space.add(car_body, car_body_shape)
        game.space.add(front_wheel, front_wheel_shape)
        game.space.add(back_wheel, back_wheel_shape)
        game.space.add(front_pivot)
        game.space.add(back_pivot)
        game.space.add(front_wheel_groove)
        game.space.add(back_wheel_groove)

        self.body = car_body
        self.front_wheel = front_wheel
        self.back_wheel = back_wheel
        self.car_body_shape = car_body_shape
        self.front_wheel_groove = front_wheel_groove
        self.back_wheel_groove = back_wheel_groove

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
        if self.front_wheel.angle < self.body.angle + th:
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
        self.game.space.remove(self.front_wheel_groove)
        self.game.space.remove(self.back_wheel_groove)

        # modify the grooves
        self.front_wheel_groove = pymunk.GrooveJoint(self.game.space.static_body,
                                                     self.front_wheel,
                                                     self.front_wheel.position - pymunk.Vec2d(0, 20).rotated(self.front_wheel.angle),
                                                     self.front_wheel.position + pymunk.Vec2d(0, 20).rotated(self.front_wheel.angle),
                                                     (0, 0))

        self.back_wheel_groove = pymunk.GrooveJoint(self.game.space.static_body,
                                                    self.back_wheel,
                                                    self.back_wheel.position - pymunk.Vec2d(0, 20).rotated(self.back_wheel.angle),
                                                    self.back_wheel.position + pymunk.Vec2d(0, 20).rotated(self.back_wheel.angle),
                                                    (0, 0))

        # replace the grooves
        self.game.space.add(self.front_wheel_groove)
        self.game.space.add(self.back_wheel_groove)

    def update_sprite(self) -> None:
        """
        Update the sprite

        :return: None
        """

        self.sprite.image = pygame.transform.rotate(self.sprite.original_image, -self.body.rotation_vector.angle_degrees)
        self.sprite.rect = self.sprite.image.get_rect(center=self.body.position)

    def update(self) -> None:
        """
        Updates the entity every tick
        :return: None
        """

        self.pos = list(self.body.position)
        self.back_wheel.angle = self.body.angle
        self.update_grooves()
        self.update_sprite()
        self.wep.update()
