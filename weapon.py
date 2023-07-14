from sprite import *


class Weapon:
    """
    Weapons that sit on top of cars that can fire various projectiles
    """

    damage: float           # damage per hit
    rate_of_fire: float     # cooldown between projectiles being created
    ammo: float             # when ammo runs out, can't shoot
    sprite: Sprite          # sprite for the weapon

    def __init__(self, damage: float, rate_of_fire: float, ammo: float, sprite: Sprite):
        """
        Initializer

        :param
        """

        self.damage = damage
        self.rate_of_fire = rate_of_fire
        self.ammo = ammo
        self.sprite = sprite


