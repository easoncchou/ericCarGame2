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
    pos: list[int]

    def __init__(self, game: 'Game', car: 'Car', pos: list[int], damage: float, atk_cd: int, ammo: float, image: pygame.image):
        """
        Initializer

        :param pos: a list of two integers representing the x y position of the gun's center
        :param damage: an integer representing the damage value of each projectile fired by the weapon
        :param atk_cd: the number of ticks a weapon requires inbetween firing projectiles
        :param ammo: the number of projectiles a weapon can fire before running out
        :param sprite: the sprite of the weapon
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

        GenericEntity.__init__(self, game)

    def update_sprite(self) -> None:
        """
        Update sprite
        :return:
        """

        self.sprite.image = pygame.transform.rotate(self.sprite.original_image, ((180 / math.pi) * self.a_pos))
        self.sprite.rect = self.sprite.image.get_rect(center=self.sprite.image.get_rect(center=(self.pos[0], self.pos[1])).center)

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
            self.game.phys_objs.append(new_proj)
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



