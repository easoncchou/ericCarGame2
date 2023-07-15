import math
from sprite import *
from projectiles import *


class Weapon:
    """
    Weapons that sit on top of cars that can fire various projectiles
    """

    damage: float           # damage per hit
    atk_cd: int             # cooldown between projectiles being created in ticks
    curr_atk_cd: int        # the time left until the next cd
    ammo: float             # when ammo runs out, can't shoot
    sprite: Sprite          # sprite for the weapon
    a_pos: float            # direction the weapon is facing
    pos: list[int]

    def __init__(self, pos: list[int], damage: float, atk_cd: float, ammo: float, sprite: Sprite):
        """
        Initializer

        :param pos: a list of two integers representing the x y position of the gun's center
        :param damage: an integer representing the damage value of each projectile fired by the weapon
        :param atk_cd: the number of ticks a weapon requires inbetween firing projectiles
        :param ammo: the number of projectiles a weapon can fire before running out
        :param sprite: the sprite of the weapon
        """

        self.damage = damage
        self.atk_cd = atk_cd
        self.curr_atk_cd = 0
        self.ammo = ammo
        self.sprite = sprite
        self.a_pos = math.pi
        self.pos = pos

    def update_sprite(self, new_pos: list[int]) -> None:
        """
        Update sprite
        :return:
        """

        # todo move to a better place
        self.curr_atk_cd -= 1

        self.sprite.image = pygame.transform.rotate(self.sprite.original_image, ((180 / math.pi) * self.a_pos))
        self.sprite.rect = self.sprite.image.get_rect(center=self.sprite.image.get_rect(center=(self.pos[0], self.pos[1])).center)

    def shoot(self) -> Projectile:
        """
        Abstract class
        :return:
        """

        raise NotImplementedError

    def delete_offscreen_projectile(self) -> None:
        """
        Delete a projectile once it has completely gone off the edge of the screen. Deletion is done by both
        deleting the projectile's sprite and removing it from the game.
        :return:
        """

        if self.pos[0] < -50 or self.pos[0] > MAP_WIDTH:
            pass
            # TODO: remove it from the sprite group and set the variable to none
        elif self.pos[0] < -50 or self.pos[0] > MAP_WIDTH:
            pass
            # TODO: remove it from the sprite group and set the variable to none


class MachineGun(Weapon):
    """
    A machine gun that shoots bullets

    :param pos: a list of two integers representing the x y position of the gun's center
    :param damage: an integer representing the damage value of each projectile fired by the weapon
    :param atk_cd: the number of ticks a weapon requires inbetween firing projectiles
    :param ammo: the number of projectiles a weapon can fire before running out
    :param sprite: the sprite of the weapon
    """

    def shoot(self) -> Bullet:
        """
        Shoots a bullet in the guns current direction
        :return:
        """

        if self.curr_atk_cd <= 0:
            self.curr_atk_cd = self.atk_cd
        else:
            return None

        bullet_image = pygame.surface.Surface((2, 80))
        bullet_image.fill([235, 170, 49])

        return Bullet(self.damage, 5, self.pos, 2500, self.a_pos, bullet_image)


class RocketLauncher(Weapon):
    """
    A rocket launcher that shoots rockets

    :param pos: a list of two integers representing the x y position of the launcher's center
    :param damage: an integer representing the damage value of each projectile fired by the weapon
    :param atk_cd: the number of ticks a weapon requires inbetween firing projectiles
    :param ammo: the number of projectiles a weapon can fire before running out
    :param sprite: the sprite of the weapon
    """

    def shoot(self) -> Rocket:
        """
        Shoots a rocket in the guns current direction, which will seek out a target
        :return:
        """

        if self.curr_atk_cd <= 0:
            self.curr_atk_cd = self.atk_cd
        else:
            return None

        rocket_image = pygame.surface.Surface((15, 60))
        rocket_image.fill(RED)

        return Rocket(self.damage, 5, self.pos, 1000, self.a_pos, rocket_image)



