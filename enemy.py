from constants import *
from physics_object import *
import math
from shapely.geometry import Polygon, LineString
from shapely.affinity import translate, rotate

class Enemy(PhysicsObject):
    """
    Any convex polygon object with physics
    """

    mass: int
    poly: Polygon
    pos: list[int, int]
    vel: float
    a_pos: float
    max_speed: int
    acceleration: int