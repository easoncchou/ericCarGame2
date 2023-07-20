import pygame.math

from game import *
from sprite import *
from physics_object import *


class GenericEntity:
    """
    An entity with a sprite
    """
    game: 'Game'
    sprite: 'Sprite'
    pos: list[int]
    a_pos: float
    rot_off: pygame.math.Vector2

    def __init__(self, game: 'Game', pos: list[int], sprite: Sprite, rot_off: tuple[int, int]):
        """
        Initializer
        """

        pos = pos.copy()

        self.pos = pos
        self.a_pos = 0
        self.game = game
        self.sprite = sprite
        self.rot_off = pygame.math.Vector2(rot_off)

    def update_sprite(self) -> None:
        """
        Update the sprite

        :return: None
        """

        self.sprite.image = pygame.transform.rotate(self.sprite.original_image, ((180 / math.pi) * self.a_pos))

        offset_rotated = self.rot_off.rotate(-((180 / math.pi) * self.a_pos))
        self.sprite.rect = self.sprite.image.get_rect(center=self.pos + offset_rotated)

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
    pos: list[int]
    a_pos: float
    max_hp: int
    hp: int
    hp_bar: 'HealthBar'

    def __init__(self, game: 'Game', pos: list[int], sprite: Sprite, max_hp: int, rot_off: tuple[int, int]) -> None:
        """
        Initializer

        :param max_hp: max hp of this entity
        """
        pos = pos.copy()
        GenericEntity.__init__(self, game, pos, sprite, rot_off)
        self.max_hp = max_hp
        self.hp = max_hp
        self.hp_bar = HealthBar(self)

    def update(self) -> None:
        """
        Updates the entity every tick

        :return: None
        """

        if self.hp <= 0:
            self.game.ents.remove(self)


class HealthBar(GenericEntity):
    """
    A drawn bar visualizing health remaining / max health of a HealthEntity
    """

    health_entity: HealthEntity
    total_length: int
    current_length: int
    width: int
    x_position: int
    y_position: int

    def __init__(self, health_entity: HealthEntity):
        """

        :param health_entity: an instance of a HealthEntity
        """

        self.health_entity = health_entity
        self.total_length = 80
        self.height = 10

        image = pygame.Surface([self.total_length, self.height])
        image.fill(RED)
        new_pos = [self.health_entity.pos[0], self.health_entity.pos[1] - self.health_entity.sprite.rect.h / 1.4]
        GenericEntity.__init__(self, health_entity.game, new_pos, Sprite(new_pos, image), (0, 0))

        # add the health bar to the sprite group
        self.game.ents.append(self)
        self.game.all_sprites_group.add(self.sprite)

    def update(self) -> None:
        """
        Update the information regarding the health bar

        :return: None
        """

        percentage_health = self.health_entity.hp / self.health_entity.max_hp
        length = percentage_health * self.total_length

        self.sprite.image.fill(RED)
        self.pos = [self.health_entity.pos[0], self.health_entity.pos[1] - self.health_entity.sprite.rect.h / 1.4]
        self.update_sprite()

        pygame.draw.rect(self.sprite.image, GREEN, [0, 0, length, self.height])

        if self.health_entity.hp <= 0:
            self.delete()










