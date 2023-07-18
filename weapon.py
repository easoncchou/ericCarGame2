import math

from entities import GenericEntity
from sprite import *
from projectiles import *
from game import *
from car import *


class Weapon(GenericEntity):
    """
    Weapons that sit on top of cars that can fire various projectiles
    """

    car: 'Car'
    game: 'Game'
    damage: float           # damage per hit
    atk_cd: int             # cooldown between projectiles being created in ticks
    curr_atk_cd: int        # the time left until the next cd
    ammo: float             # when ammo runs out, can't shoot
    sprite: Sprite          # sprite for the weapon
    a_pos: float            # direction the weapon is facing
    pos: list[int]          # position of the weapon in x y coordinates
    rot_off: tuple[int, int]     # offset for the pivot of rotation for the sprite

    def __init__(self, game: 'Game', car: 'Car', pos: list[int], damage: float, atk_cd: int, ammo: float,
                 rot_off: tuple[int, int], image: pygame.image):
        """
        Initializer

        :param pos: a list of two integers representing the x y position of the gun's center
        :param damage: an integer representing the damage value of each projectile fired by the weapon
        :param atk_cd: the number of ticks a weapon requires inbetween firing projectiles
        :param ammo: the number of projectiles a weapon can fire before running out
        :param image: the image for the sprite of the weapon
        """

        pos = pos.copy()

        self.car = car
        self.damage = damage
        self.atk_cd = atk_cd
        self.curr_atk_cd = 0
        self.ammo = ammo
        self.sprite = Sprite(pos, image)
        self.a_pos = math.pi
        self.pos = pos
        self.rot_off = rot_off

        GenericEntity.__init__(self, game, self.pos, self.sprite, self.rot_off)

    def update(self) -> None:
        """
        Updates the entity every tick
        :return: None
        """

        self.curr_atk_cd -= 1
        self.pos = self.car.pos
        self.update_sprite()

    def shoot(self) -> None:
        """
        Abstract class
        :return:
        """

        raise NotImplementedError


class MachineGun(Weapon):
    """
    A machine gun that shoots bullets

    :param pos: a list of two integers representing the x y position of the gun's center
    :param damage: an integer representing the damage value of each projectile fired by the weapon
    :param atk_cd: the number of ticks a weapon requires inbetween firing projectiles
    :param ammo: the number of projectiles a weapon can fire before running out
    :param sprite: the sprite of the weapon
    """

    def shoot(self) -> None:
        """
        Shoots a bullet in the guns current direction
        :return:
        """
        if self.curr_atk_cd <= 0:
            self.curr_atk_cd = self.atk_cd

            bullet_image = pygame.surface.Surface((2, 80))
            bullet_image.fill(YELLOW)

            new_proj = Bullet(self.game, self.damage, 5, self.pos, 2500, self.a_pos, bullet_image)

            self.game.ents.append(new_proj)
            self.game.projs.append(new_proj)
            self.game.all_sprites_group.add(new_proj.sprite)


class RocketLauncher(Weapon):
    """
    A rocket launcher that shoots rockets

    :param pos: a list of two integers representing the x y position of the launcher's center
    :param damage: an integer representing the damage value of each projectile fired by the weapon
    :param atk_cd: the number of ticks a weapon requires inbetween firing projectiles
    :param ammo: the number of projectiles a weapon can fire before running out
    :param sprite: the sprite of the weapon
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

            new_proj = Rocket(self.game, self.damage, 25, self.pos, 750, self.a_pos, rocket_image)

            self.game.ents.append(new_proj)
            self.game.projs.append(new_proj)
            self.game.all_sprites_group.add(new_proj.sprite)



