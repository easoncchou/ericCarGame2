from game import *
from entities import *
from sprite import *
from physics_object import *


class Target(PhysicsObject, HealthEntity):
    """
    A stationary target with hp
    """

    game: 'Game'
    mass: int
    poly: Polygon
    pos: list[int, int]
    vel: float
    a_pos: float
    max_speed: int
    acceleration: int

    def __init__(self, game: 'Game', pos: list[int], max_hp: int, image: pygame.image, poly=None):
        """

        :param game:
        :param pos:
        :param max_hp:
        :param image:
        :param poly:
        """

        pos = pos.copy()

        HealthEntity.__init__(self, game, pos, Sprite(pos, image), max_hp, (0, 0))

        # if poly is None, create polygon from rect
        if poly is None:
            vertices = [self.sprite.rect.topleft,
                        self.sprite.rect.topright,
                        self.sprite.rect.bottomright,
                        self.sprite.rect.bottomleft]
            poly = Polygon(vertices)

        PhysicsObject.__init__(self, 0, 0, 0, pos, poly)

    def update(self) -> None:
        """
        Updates the entity every tick

        :return: None
        """

        if self.hp <= 0:
            self.delete()

    def delete(self) -> None:
        """
        Deletes the entity from the game

        :return: None
        """

        HealthEntity.delete(self)
        self.game.enemies.remove(self)
