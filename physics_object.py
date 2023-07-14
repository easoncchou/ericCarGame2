from constants import *
import math
from shapely.geometry import Polygon, LineString
from shapely.affinity import translate, rotate


class PhysicsObject:
    """
    Any convex polygon object with physics
    """

    mass: int
    poly: Polygon
    handling: int
    pos: list[int, int]
    vel: float
    a_pos: float

    def __init__(self, mass: int, handling: int, pos: list[int, int], poly: Polygon) -> None:
        """
        Initializer

        :param mass: mass of the obj
        :param poly: size of the obj
        :param pos: position of the obj
        """

        self.poly = poly
        self.mass = mass
        self.handling = handling

        self.pos = pos              # (x, y)
        self.vel = 0                # tangential velocity

        self.a_pos = math.pi        # angular position in radians; positive is CCW

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
            self.vel = math.copysign(MAX_SPEED, self.vel)

    def steer_car(self, magnitude: int, direction: float) -> None:
        """
        Steers the car by changing the angular velocity of the car

        :param magnitude: magnitude of the force
        :param direction: direction of the force
        :return: None
        """

        # calculate the angular velocity
        a_vel = self.vel * magnitude / 100000 * (self.handling / 2)

        if a_vel >= MAX_A_SPEED:
            a_vel = MAX_A_SPEED

        #   determine the direction of normal acceleration
        if direction == 0:
            a_vel *= -1

        # update the angular position
        dth = a_vel * (1 / TICKRATE)
        self.a_pos += dth
        self.poly = rotate(self.poly, - dth * 180 / math.pi)

    def check_wall_collision(self) -> None:
        """
        Check if the object is in contact with the edge of the window/map and stop the object if it is

        NOTE: REMEMBER TO CALL IT BEFORE UPDATE POS, WHICH USES VELOCITY (IN GAME.PY)

        :return: None
        """

        if self.poly.intersects(LineString([(0, 0), (MAP_WIDTH, 0)])):
            # shift the position 1 pixel away from the edge
            self.pos[1] += 1
            # shift the polygon 1 pixel away from the edge
            self.poly = translate(self.poly, yoff=1)
            self.vel = 0
        elif self.poly.intersects(LineString([(MAP_WIDTH, 0), (MAP_WIDTH, MAP_HEIGHT)])):
            self.pos[0] -= 1
            self.poly = translate(self.poly, xoff=-1)
            self.vel = 0
        elif self.poly.intersects(LineString([(MAP_WIDTH, MAP_HEIGHT), (0, MAP_HEIGHT)])):
            self.pos[1] -= 1
            self.poly = translate(self.poly, yoff=-1)
            self.vel = 0
        elif self.poly.intersects(LineString([(0, MAP_HEIGHT), (0, 0)])):
            self.pos[0] += 1
            self.poly = translate(self.poly, xoff=1)
            self.vel = 0

    def update_pos(self) -> None:
        """
        Updates the position of the object

        :return: None
        """
        # friction; the car will passively slow down until it stops moving
        if abs(self.vel) > 0.5:
            self.vel -= math.copysign(0.5, self.vel)

        dx = (self.vel * math.sin(self.a_pos)) * (1 / TICKRATE)
        dy = (self.vel * math.cos(self.a_pos)) * (1 / TICKRATE)

        self.pos[0] += dx
        self.pos[1] += dy

        self.poly = translate(self.poly, xoff=dx, yoff=dy)


def is_collide(obj1: PhysicsObject, obj2: PhysicsObject) -> bool:
    """
    Check if two PhysicsObjects are colliding

    :param obj1: a PhysicsObject
    :param obj2: a PhysicsObject
    :return: true iff the two object are colliding
    """

    return obj1.poly.intersects(obj2.poly)
