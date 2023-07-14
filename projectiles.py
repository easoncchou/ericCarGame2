from sprite import *
from physics_object import *


class Projectile(PhysicsObject):
    """
    Projectile fired from a weapon
    """

    mass: int
    poly: Polygon
    pos: list[int, int]
    vel: float
    a_pos: float
    max_speed: int
    acceleration: int

    def __init__(self, mass: int, pos: list[int], max_speed: int,
                 acceleration: int, image: pygame.image, poly=None) -> None:
        """
        Initializer

        :param mass: mass of projectile
        :param poly: polygon representing the shape of the projectile, rectangle by default
        """

        self.sprite = Sprite((pos[0], pos[1]), image)

        # if poly is None, create polygon from rect
        if poly is None:
            vertices = [self.sprite.rect.topleft,
                        self.sprite.rect.topright,
                        self.sprite.rect.bottomright,
                        self.sprite.rect.bottomleft]
            poly = Polygon(vertices)

        super().__init__(mass, max_speed, acceleration, pos, poly)


class Bullet(Projectile):
    """
    Projectile fired by a machine gun
    """


class Laser(Projectile):
    """
    Projectile fired by a laser cannon
    """


class Rocket(Projectile):
    """
    Projectile fired by a rocket launcher
    """

