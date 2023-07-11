from constants import *
import math


class PhysicsObject:
    """
    Any rectangular object with physics
    """

    mass: int
    size: tuple[int, int]
    handling: int
    pos: list[int, int]
    vel: float
    a_pos: float
    a_vel: float

    def __init__(self, mass: int, size: tuple[int, int], handling) -> None:
        """
        Initializer

        :param mass: mass of the car
        :param size: size of the car
        :param handling: how well a car steers/turns (the higher the value the faster it turns)
        """

        self.mass = mass
        self.size = size
        self.handling = 5

        self.pos = [100, 100]       # (x, y)
        self.vel = 0            # tangential velocity

        self.a_pos = math.pi          # angular position in radians; positive is CCW
        self.a_vel = 0          # angular velocity; positive is CCW

    def apply_force_tan(self, magnitude: int, direction: float) -> None:
        """
        Applies a force relative to this PhysicsObject and updates the velocity in the tangential direction

        :param magnitude: magnitude of the force
        :param direction: direction of the force
        :return: None
        """

        # calculate acceleration
        acc = magnitude / self.mass

        # calculate velocity
        #   tangential only - normal velocity is always 0 by definition
        self.vel += acc * (1 / TICKRATE)

        if abs(self.vel) >= MAX_SPEED:
            self.vel = self.vel / abs(self.vel) * MAX_SPEED

    def steer_car(self, magnitude: int, direction: float) -> None:
        """
        Steers the car by changing the angular velocity of the car

        :param magnitude: magnitude of the force
        :param direction: direction of the force
        :return: None
        """

        # calculate the angular velocity
        self.a_vel = self.vel * magnitude / 100000 * (self.handling / 2)

        if self.a_vel >= MAX_A_SPEED:
            self.a_vel = MAX_A_SPEED

        #   determine the direction of normal acceleration
        if direction == 0:
            self.a_vel *= -1

    def update_pos(self) -> None:
        """
        Updates the position of the object

        :return: None
        """
        self.pos[0] += (self.vel * math.sin(self.a_pos)) * (1 / TICKRATE)
        self.pos[1] += (self.vel * math.cos(self.a_pos)) * (1 / TICKRATE)
        self.a_pos += self.a_vel * (1 / TICKRATE)



