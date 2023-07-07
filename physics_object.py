from constants import *
import math


class PhysicsObject:
    """
    Any rectangular object with physics
    """

    mass: int
    moi: int
    size: tuple[int, int]
    lever_arm: int
    pos: list[int, int]
    vel: float
    a_pos: float
    a_vel: float

    def __init__(self, mass: int, moi: int,
                 size: tuple[int, int], lever_arm: int) -> None:
        """
        Initializer

        :param mass: mass of the car
        :param moi: moment of inertia of the car
        :param size: size of the car
        :param lever_arm: distance between applied force and centre of mass of the car
        """

        self.mass = mass
        self.moi = moi          # moment of inertia
        self.size = size
        self.lever_arm = lever_arm      # how well a car turns; used for angular calculations

        self.pos = [0, 0]       # (x, y)
        self.vel = 0            # tangential velocity

        self.a_pos = 0          # angular position in degrees; positive is CCW
        self.a_vel = 0          # angular velocity; positive is CCW

    def apply_force(self, magnitude: int, direction: float) -> None:
        """
        Applies a force relative to this PhysicsObject and updates the velocity

        :param magnitude: magnitude of the force
        :param direction: direction of the force
        :return: None
        """

        # calculate acceleration
        acc = magnitude / self.mass

        # calculate velocity
        #   tangential only - normal velocity is always 0 by definition
        self.vel += acc * (1 / TICKRATE)

        # calculate normal acceleration
        #   calculate the magnitude of the angular acceleration
        normal_acc = self.vel * ((magnitude * self.lever_arm) / self.moi)

        #   determine the direction of normal acceleration
        if direction == 0:
            normal_acc *= -1

        # calculate angular velocity
        self.a_vel += normal_acc * (1 / TICKRATE)

    def update_pos(self) -> None:
        """
        Updates the position of the object

        :return: None
        """
        self.pos[0] += (self.vel * math.cos(self.a_pos)) * (1 / TICKRATE)
        self.pos[1] += (self.vel * math.sin(self.a_pos)) * (1 / TICKRATE)
        self.a_pos = self.a_vel * (1 / TICKRATE)



