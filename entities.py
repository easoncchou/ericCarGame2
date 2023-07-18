from game import *
from physics_object import *


class GenericEntity:
    """
    An entity with a sprite
    """
    game: 'Game'

    def __init__(self, game: 'Game'):
        """
        Initializer
        """

        self.game = game

    def update(self) -> None:
        """
        Updates the entity every tick

        :return: None
        """

        raise NotImplementedError

    def delete(self) -> None:
        """
        Deletes the entity from the game

        :return: None
        """

        self.game.all_sprites_group.remove(self.sprite)
        self.game.ents.remove(self)
        if isinstance(self, PhysicsObject):
            self.game.phys_objs.remove(self)


class HealthEntity(GenericEntity):
    """
    An entity with HP
    """

    game: 'Game'
    max_hp: int
    hp: int

    def __init__(self, game: 'Game', max_hp: int) -> None:
        """
        Initializer

        :param max_hp: max hp of this entity
        """
        GenericEntity.__init__(self, game)
        self.max_hp = max_hp
        self.hp = max_hp

    def update(self) -> None:
        """
        Updates the entity every tick

        :return: None
        """

        if self.hp <= 0:
            self.game.ents.remove(self)
