from sprite import *
from physics_object import *
from entities import *


class Target(PhysicsObject, HealthEntity):
    """
    A stationary target with hp
    """

    mass: int
    poly: Polygon
    pos: list[int, int]
    vel: float
    a_pos: float
    max_speed: int
    acceleration: int

    def __init__(self, game, pos: list[int], max_hp: int, image: pygame.image, poly=None):
        """

        :param game:
        :param pos:
        :param max_hp:
        :param image:
        :param poly:
        """

        pos = pos.copy()
        self.sprite = Sprite(pos, image)

        PhysicsObject.__init__(self, 0, 0, 0, pos, poly)
        HealthEntity.__init__(self, game, max_hp)

    def update(self) -> None:
        """
        Updates the entity every tick

        :return: None
        """

        if self.hp <= 0:
            self.game.all_sprites_group.remove(self.sprite)
            self.game.ents.remove(self)
