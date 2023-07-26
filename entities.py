import pygame.math
import pygame
import pymunk

from constants import *
from sprite import Sprite


class GenericEntity:
    """
    An entity with a sprite
    """

    sprite: 'Sprite'
    pos: pymunk.Vec2d
    a_pos: float

    def __init__(self, sprite: Sprite, pos=pymunk.Vec2d(0, 0), a_pos=0):
        """
        Initializer
        """

        self.sprite = sprite
        self.pos = pos
        self.a_pos = a_pos

    def update_sprite(self) -> None:
        """
        Update the sprite

        :return: None
        """

        raise NotImplementedError

    def update(self) -> None:
        """
        Updates the entity every tick

        :return: None
        """

        raise NotImplementedError


class HealthEntity(GenericEntity):
    """
    An entity with HP
    """

    pos: pymunk.Vec2d
    a_pos: float
    max_hp: int
    hp: int
    hp_bar: 'HealthBar'

    def __init__(self, sprite: Sprite, max_hp: int, pos=pymunk.Vec2d(0, 0), a_pos=0) -> None:
        """
        Initializer

        :param max_hp: max hp of this entity
        """

        GenericEntity.__init__(self, sprite, pos, a_pos)
        self.max_hp = max_hp
        self.hp = max_hp
        self.hp_bar = HealthBar(self)

    def update_sprite(self) -> None:
        """
        Update the sprite

        :return: None
        """

        raise NotImplementedError

    def update(self) -> None:
        """
        Updates the entity every tick

        :return: None
        """

        self.hp_bar.update()


class HealthBar(GenericEntity):
    """
    A drawn bar visualizing health remaining / max health of a HealthEntity
    """

    sprite: 'Sprite'
    pos: pymunk.Vec2d
    a_pos: float
    health_entity: HealthEntity
    w: int
    h: int

    def __init__(self, health_entity: HealthEntity):
        """

        :param health_entity: an instance of a HealthEntity
        """

        self.health_entity = health_entity
        self.w = 80
        self.h = 10

        image = pygame.Surface([self.w, self.h])
        image.fill(RED)
        new_pos = pymunk.Vec2d(self.health_entity.pos[0], self.health_entity.pos[1] - self.health_entity.sprite.rect.h / 1.4)
        GenericEntity.__init__(self, Sprite(new_pos, image), new_pos)

    def update_sprite(self) -> None:
        """
        Update the sprite

        :return:
        """

        self.sprite.rect = self.sprite.image.get_rect(center=self.pos)

    def update(self) -> None:
        """
        Update the information regarding the health bar

        :return: None
        """

        percentage_health = self.health_entity.hp / self.health_entity.max_hp
        length = percentage_health * self.w

        self.sprite.image.fill(RED)
        self.pos = pymunk.Vec2d(self.health_entity.pos[0], self.health_entity.pos[1] - self.health_entity.sprite.rect.h / 1.4)
        self.update_sprite()

        pygame.draw.rect(self.sprite.image, GREEN, [0, 0, length, self.h])


class Reticle(GenericEntity):
    """
    A reticle spawned when a rocket launcher selects a target. The Reticle will follow the targeted Enemy.
    """

    def __init__(self, pos: pymunk.Vec2d, sprite: Sprite, current_target: HealthEntity):
        GenericEntity.__init__(self, sprite, pos)
        self.current_target = current_target

    def update_sprite(self) -> None:
        """
        Update the sprite

        :return:
        """

        self.sprite.rect = self.sprite.image.get_rect(center=self.pos)

    def update(self) -> None:
        """
        Update the position of the reticle

        :return: None
        """

        self.pos = self.current_target.pos
        self.update_sprite()


class Explosion(GenericEntity):
    def __init__(self, radius: float, pos: pymunk.Vec2d):
        image = pygame.Surface([2 * radius, 2 * radius], pygame.SRCALPHA)
        pygame.draw.circle(image, RED, (radius, radius), radius)

        GenericEntity.__init__(self, Sprite(pos, image), pos)

        self.lifespan = TICKRATE / 5    # 0.2 second

    def update_sprite(self) -> None:
        pass

    def update(self) -> None:
        self.lifespan -= 1


class LaserContact(GenericEntity):
    """
    An entity that exists at the endpoint of a laser beam
    """

    def update(self) -> None:
        """
        Does nothing

        :return:
        """
        self.update_sprite()

    def update_sprite(self) -> None:
        """
        Update the sprite

        :return:
        """

        self.sprite.rect = self.sprite.image.get_rect(center=self.pos)









