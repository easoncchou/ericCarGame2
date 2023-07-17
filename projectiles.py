from sprite import *
from physics_object import *


class Projectile(PhysicsObject):
    """
    Projectile fired from a weapon
    """

    damage: float
    mass: int
    poly: Polygon
    pos: list[int, int]
    vel: float
    a_pos: float
    max_speed: int
    acceleration: int

    def __init__(self, damage: float, mass: int, pos: list[int], speed: int, a_pos: float, image: pygame.image, poly=None) -> None:
        """
        Initializer

        :param mass: mass of projectile
        :param damage: damage done by the projectile when it collides with a target
        :param mass: mass of the projectile
        :param pos: a list of two integers representing the x and y coordinates of the projectile
        :param speed: the speed at which the projectile will travel at
        :param a_pos: the angular position of the projectile, in radians
        :param image: a pygame image of the projectile's sprite currently loaded in main
        :param poly: polygon representing the shape of the projectile, rectangle by default
        """

        pos = pos.copy()

        self.sprite = Sprite(pos, image)

        # if poly is None, create polygon from rect
        if poly is None:
            vertices = [self.sprite.rect.topleft,
                        self.sprite.rect.topright,
                        self.sprite.rect.bottomright,
                        self.sprite.rect.bottomleft]
            poly = Polygon(vertices)

        super().__init__(mass, speed, 0, pos, poly)
        self.vel = speed
        self.a_pos = a_pos

        self.damage = damage

        # rotate the sprite to match the weapon
        self.sprite.image = pygame.transform.rotate(self.sprite.original_image, ((180 / math.pi) * self.a_pos))

    def update_sprite(self) -> None:
        """
        Update the sprite

        :return: None
        """

        self.sprite.rect = self.sprite.image.get_rect(center=self.sprite.image.get_rect(center=(self.pos[0], self.pos[1])).center)

    def check_bound_collision(self) -> bool:
        """
        Checks if the projectile is out of bounds

        :return: true iff the projectile is out of bounds
        """
        OUTER_BOUND = 100

        return self.pos[0] <= -OUTER_BOUND or self.pos[0] > MAP_WIDTH + OUTER_BOUND or self.pos[1] <= -OUTER_BOUND or self.pos[1] > MAP_HEIGHT + OUTER_BOUND


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

