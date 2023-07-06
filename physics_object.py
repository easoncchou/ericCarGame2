from constants import *
import math

class PhysicsObject:
    """
    Any rectangular object with physics
    """

    def __init__(self, mass: int, moi: int,
                 size: tuple[int, int], pivot: tuple[int, int]) -> None:
        """
        Initializer
        """

        self.mass = mass
        self.moi = moi          # moment of inertia
        self.size = size
        self.pivot = pivot      # pivot point for the car

        self.pos = (0, 0)       # (x, y)
        self.vel = 0            # tangential velocity

        self.a_pos = 0          # angular position
        self.a_vel = 0          # angular velocity

    def apply_force(self, force_pos: tuple[int, int], magnitude: int, direction: float) -> None:
        """
        Applies a force relative to this PhysicsObject
        :return:
        """

        # calculate acceleration
        acc = magnitude / self.mass

        # calculate velocity (tangential only - normal velocity is always 0 by definition)
        self.vel += acc * (1 / TICKRATE)

        # calculate normal acceleration

        # calculate angular velocity

        # calculate angular position

        # calculate position
        self.pos[0] += (self.vel * math.cos(self.a_pos)) * (1 / TICKRATE)
        self.pos[1] += (self.vel * math.sin(self.a_pos)) * (1 / TICKRATE)


