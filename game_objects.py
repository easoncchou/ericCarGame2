from physics_object import *
from sprite import *


class Terrain(PhysicsObject):
    """
    A terrain obstacle that can't move
    """

    def __init__(self, pos: list[int, int], poly: Polygon) -> None:
        """
        Initializer

        :param pos: position of the obj
        :param poly: size of the obj
        """

        super().__init__(0, 0, pos, poly)
