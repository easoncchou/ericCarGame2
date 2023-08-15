import math
import pygame
import pygame.mouse
import pymunk
from typing import Union

from constants import *
from projectiles import Projectile, Bullet, Rocket, Laser
from entities import GenericEntity, HealthEntity, LaserContact
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
    barrel_len: int         # barrel length
    rot_off: pymunk.Vec2d   # offset for the pivot of rotation for the sprite

    def __init__(self, pos: pymunk.Vec2d, damage: float, atk_cd: int, ammo: float,
                 rot_off: pymunk.Vec2d, image: pygame.image):
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
        self.rot_off = rot_off
        self.barrel_len = self.sprite.rect.h

    def update_sprite(self) -> None:
        """
        Update the sprite

        :return: None
        """

        self.sprite.image = pygame.transform.rotate(self.sprite.original_image, ((180 / math.pi) * self.a_pos))
        offset_rotated = self.rot_off.rotated(-self.a_pos)
        self.sprite.rect = self.sprite.image.get_rect(center=self.screen_pos + offset_rotated)

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

    # TODO: Add spread to the bullets

    def shoot(self) -> Union[Bullet, None]:
        """
        Shoots a bullet in the guns current direction
        :return:
        """
        if self.curr_atk_cd <= 0 < self.ammo:
            self.curr_atk_cd = self.atk_cd
            self.ammo -= 1

            bullet_image = pygame.surface.Surface((3, 80))
            bullet_image.fill(BULLET_ORANGE)

            return Bullet(self.damage,
                          self.pos + (pymunk.Vec2d(0, self.barrel_len / 2 + self.rot_off.y + bullet_image.get_height() / 2)).rotated(-self.a_pos),
                          2500,
                          self.a_pos,
                          bullet_image)


class RocketLauncher(Weapon):
    """
    A rocket launcher that shoots rockets
    """

    potential_target: Union[HealthEntity, None]     # the potential target being considered by the select_target function
    targeting_status: int                           # an integer from 0-100, 100 signifying that the target is locked on
    current_target: Union[HealthEntity, None]       # the current target locked onto by the launcher

    def __init__(self, pos: pymunk.Vec2d, damage: float, atk_cd: int, ammo: float,
                 rot_off: pymunk.Vec2d, image: pygame.image):
        Weapon.__init__(self, pos, damage, atk_cd, ammo, rot_off, image)

        self.current_target = None
        self.potential_target = None
        self.targeting_status = 0

    def shoot(self) -> Projectile:
        """
        Shoots a bullet in the guns current direction

        :return: Projectile
        """
        if self.curr_atk_cd <= 0 < self.ammo:
            self.curr_atk_cd = self.atk_cd
            self.ammo -= 1

            rocket_image = pygame.image.load("assets/rocket1.png")
            rocket_image = pygame.transform.scale(rocket_image, [65, 65])

            return Rocket(self.damage,
                          100,
                          25000,
                          self.pos + (pymunk.Vec2d(0, self.barrel_len / 2 + self.rot_off.y + rocket_image.get_height() / 2)).rotated(-self.a_pos),
                          750,
                          self.a_pos,
                          rocket_image,
                          None if self.targeting_status != OFF else self.current_target,
                          0.05)


class LaserCannon(Weapon):
    """
    Laser cannon that fires a laser at the mouse direction
    """

    proj: Union[Laser, None]
    laser_contact: LaserContact

    def __init__(self, pos: pymunk.Vec2d, damage: float, atk_cd: int, laser: Laser, ammo: float,
                 rot_off: pymunk.Vec2d, image: pygame.image):
        """
        Initializer

        :param pos: a list of two integers representing the x y position of the gun's center
        :param damage: an integer representing the damage value of each projectile fired by the weapon
        :param atk_cd: unused for the laser subclass
        :param ammo: the number of projectiles a weapon can fire before running out
        :param image: the image for the sprite of the weapon
        """

        Weapon.__init__(self, pos, damage, atk_cd, ammo, rot_off, image)

        self.laser = laser
        self.laser_contact = None

    def shoot(self) -> Projectile:
        """
        Creates a Laser pointed at the mouse's direction

        :return: Projectile
        """

        if self.curr_atk_cd <= 0 < self.ammo:
            self.curr_atk_cd = self.atk_cd
            self.ammo -= 0.2

        block_image = pygame.image.load("assets/laser_beam_block.png")
        block_image = pygame.transform.scale(block_image, [20, 20])

        contact_image = pygame.image.load('assets/laser_contact1.png')
        contact_image = pygame.transform.scale(contact_image, [50, 50])

        # TODO: make the laser stop shooting when out of ammo
        if self.laser is None:
            self.laser = Laser(self.damage, self.pos + (pymunk.Vec2d(0, self.barrel_len / 2 + self.rot_off.y)).rotated(-self.a_pos),
                               self.a_pos, 300, block_image)
            self.laser_contact = LaserContact(Sprite(pymunk.Vec2d(0, 0), contact_image), pymunk.Vec2d(0, 0))
            return self.laser
        else:
            self.laser.pos = self.pos + (pymunk.Vec2d(0, self.barrel_len / 2 + self.rot_off.y)).rotated(-self.a_pos)
            self.laser.a_pos = self.a_pos


