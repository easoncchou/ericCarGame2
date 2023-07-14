import pygame

from physics_object import *
from sprite import *


class Car(PhysicsObject):
    """
    Car class
    """

    mass: int
    size: tuple[int, int]
    pos: list[int, int]
    vel: float
    a_pos: float
    a_vel: float
    sprite: Sprite

    def __init__(self, mass: int, size: tuple[int, int], pos: list[int, int], max_speed: int,
                 acceleration: int, max_a_speed: int, handling: int, image: pygame.image, poly=None) -> None:
        """
        Initializer

        :param mass: mass of the car
        :param size: size of the car
        :param handling: how well a car steers/turns (the higher the value the faster it turns)
        :param poly: polygon representing the shape of the car, rectangle by default
        """

        self.sprite = Sprite(size[0], size[1], image)
        self.max_a_speed = max_a_speed
        self.handling = handling

        # if poly is None, create polygon from rect
        if poly is None:
            corners = [
                (self.sprite.rect.topleft[0] + pos[0], self.sprite.rect.topleft[1] + pos[1]),
                (self.sprite.rect.topright[0] + pos[0], self.sprite.rect.topright[1] + pos[1]),
                (self.sprite.rect.bottomright[0] + pos[0], self.sprite.rect.bottomright[1] + pos[1]),
                (self.sprite.rect.bottomleft[0] + pos[0], self.sprite.rect.bottomleft[1] + pos[1])
            ]
            poly = Polygon(corners)

        super().__init__(mass, max_speed, acceleration, pos, poly)

    def steer_car(self, direction: int) -> None:
        """
        Steers the car by changing the angular velocity of the car

        :param magnitude: magnitude of the force
        :param direction: direction of the force
        :return: None
        """

        # calculate the angular velocity
        if abs(self.vel) <= 0.5:
            a_vel = 0
        elif abs(self.vel) <= 0.75 * self.max_speed:
            a_vel = self.handling * (self.vel / 150)
        else:
            magnitude = self.handling - (abs(self.vel) / 75)
            a_vel = math.copysign(magnitude, self.vel)

        if a_vel >= self.max_a_speed:
            a_vel = self.max_a_speed

        #   determine the direction of normal acceleration
        if direction == RIGHT:
            a_vel *= -1

        # update the angular position
        dth = a_vel * (1 / TICKRATE)
        self.a_pos += dth
        self.poly = rotate(self.poly, - dth * 180 / math.pi)

    def update_sprite(self) -> None:
        """
        Update the sprite

        :return: None
        """

        self.sprite.image = pygame.transform.rotate(self.sprite.original_image, ((180 / math.pi) * self.a_pos))
        self.sprite.rect = self.sprite.image.get_rect(center=self.sprite.image.get_rect(center=(self.pos[0], self.pos[1])).center)

