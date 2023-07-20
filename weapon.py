import math
import pygame
import pygame.mouse
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

    :param pos: a list of two integers representing the x y position of the launcher's center
    :param damage: an integer representing the damage value of each projectile fired by the weapon
    :param atk_cd: the number of ticks a weapon requires inbetween firing projectiles
    :param ammo: the number of projectiles a weapon can fire before running out
    :param image: the sprite of the weapon
    """
    potential_target: HealthEntity    # the potential target being considered by the select_target function
    targeting_status: int             # an integer from 0-100, 100 signifying that the target is locked on
    current_target: HealthEntity      # the current target locked onto by the launcher

    def __init__(self, game: 'Game', car: 'Car', pos: list[int], damage: float, atk_cd: int, ammo: float,
                 rot_off: tuple[int, int], image: pygame.image):
        super().__init__(game, car, pos, damage, atk_cd, ammo, rot_off, image)

        self.current_target = None
        self.potential_target = None
        self.targeting_status = 0
        self.reticle = None

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

    def select_target(self) -> None:
        """
        Detect when the mouse has been focused within the radius of an enemy for a period of time and select the
        enemy to be the target of the rockets

        :return:
        """

        x, y = pygame.mouse.get_pos()

        if self.potential_target is None:
            for enemy in self.game.enemies:
                # check if the mouse is within a square area of an enemy
                if enemy.pos[0] - 100 < x < enemy.pos[0] + 100:
                    if enemy.pos[1] - 100 < y < enemy.pos[1] + 100:
                        # if no current target is being tracked, set this close enemy to the potential target
                        if self.targeting_status == 0:
                            self.potential_target = enemy
        else:
            if self.potential_target.pos[0] - 100 < x < self.potential_target.pos[0] + 100:
                if self.potential_target.pos[1] - 100 < y < self.potential_target.pos[1] + 100:
                    # the target has been followed by the mouse for long enough, so set it to the current target
                    #   and reset the timer on targeting status
                    if self.targeting_status == OFF:
                        pass
                    elif self.targeting_status >= 100:
                        self.current_target = self.potential_target
                        self.targeting_status = OFF
                        print("TARGET LOCKED XDD!\n")

                        reticle_image = pygame.image.load("assets/reticle1.png")
                        reticle_image = pygame.transform.scale(reticle_image, [140, 100])
                        reticle_pos = [self.current_target.pos[0], self.current_target.pos[1]]
                        reticle_sprite = Sprite(reticle_pos, reticle_image)
                        self.reticle = Reticle(self.game, reticle_pos, reticle_sprite, self.current_target)

                    # the target hasn't been followed for long enough, so continue counting
                    else:
                        self.targeting_status += 1
            else:
                if self.targeting_status == OFF and self.reticle in self.game.ents:
                    self.reticle.delete()
                self.targeting_status = 0
                self.potential_target = None
                print("target lost noob...")








