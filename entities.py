from game import *
from sprite import *
from physics_object import *


class GenericEntity:
    """
    An entity with a sprite
    """
    game: 'Game'
    sprite: 'Sprite'

    def __init__(self, game: 'Game', sprite: Sprite):
        """
        Initializer
        """

        self.game = game
        self.sprite = sprite

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


class HealthEntity(GenericEntity):
    """
    An entity with HP
    """

    game: 'Game'
    max_hp: int
    hp: int

    def __init__(self, game: 'Game', sprite: Sprite, max_hp: int) -> None:
        """
        Initializer

        :param max_hp: max hp of this entity
        """
        GenericEntity.__init__(self, game, sprite)
        self.max_hp = max_hp
        self.hp = max_hp

    def update(self) -> None:
        """
        Updates the entity every tick

        :return: None
        """

        if self.hp <= 0:
            self.game.ents.remove(self)
