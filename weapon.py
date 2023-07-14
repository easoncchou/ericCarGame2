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

        :param
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


class MachineGun(Weapon):
    """
    A machine gun that shoots bullets
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
        bullet_image.fill(RED)

        return Bullet(self.damage, 5, self.pos, 2500, self.a_pos, bullet_image)


