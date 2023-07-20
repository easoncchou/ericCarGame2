import math
import pygame
import pymunk
from typing import Union

from constants import *
from projectiles import Projectile, Bullet, Rocket
from entities import GenericEntity
from sprite import Sprite


class Weapon(GenericEntity):
    """
    Weapons that sit on top of cars that can fire various projectiles
    """

    damage: float           # damage per hit
    atk_cd: int             # cooldown between projectiles being created in ticks
    curr_atk_cd: int        # the time left until the next cd
    ammo: float             # when ammo runs out, can't shoot
    sprite: Sprite          # sprite for the weapon
    a_pos: float            # direction the weapon is facing
    rot_off: pygame.math.Vector2     # offset for the pivot of rotation for the sprite

    def __init__(self, pos: pymunk.Vec2d, damage: float, atk_cd: int, ammo: float,
                 rot_off: tuple[int, int], image: pygame.image):
        """
        Initializer

        :param pos: a list of two integers representing the x y position of the gun's center
        :param damage: an integer representing the damage value of each projectile fired by the weapon
        :param atk_cd: the number of ticks a weapon requires inbetween firing projectiles
        :param ammo: the number of projectiles a weapon can fire before running out
        :param image: the image for the sprite of the weapon
        """

        GenericEntity.__init__(self, Sprite(pos, image), pos, math.pi)

        self.damage = damage
        self.atk_cd = atk_cd
        self.curr_atk_cd = 0
        self.ammo = ammo
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

        self.curr_atk_cd -= 1
        self.update_sprite()

    def shoot(self) -> Projectile:
        """
        Abstract method
        :return:
        """

        raise NotImplementedError


class MachineGun(Weapon):
    """
    A machine gun that shoots bullets
    """

    def shoot(self) -> Union[Bullet, None]:
        """
        Shoots a bullet in the guns current direction
        :return:
        """
        if self.curr_atk_cd <= 0:
            self.curr_atk_cd = self.atk_cd

            bullet_image = pygame.surface.Surface((2, 80))
            bullet_image.fill(RED)

            return Bullet(self.damage, self.pos, 2500, self.a_pos, bullet_image)


class RocketLauncher(Weapon):
    """
    A rocket launcher that shoots rockets
    """

    def shoot(self) -> None:
        """
        Shoots a bullet in the guns current direction
        :return:
        """
        if self.curr_atk_cd <= 0:
            self.curr_atk_cd = self.atk_cd

            rocket_image = pygame.image.load("assets/rocket1.png")
            rocket_image = pygame.transform.scale(rocket_image, [65, 65])

            new_proj = Rocket(self.game, self.damage, list(self.car.car_body.position), 750, self.a_pos, rocket_image)

            self.game.ents.append(new_proj)
            self.game.projs.append(new_proj)
            self.game.all_sprites_group.add(new_proj.sprite)



