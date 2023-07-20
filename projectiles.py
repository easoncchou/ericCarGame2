from game import *
from entities import *
from sprite import *
from physics_object import *


class Projectile(PhysicsObject, GenericEntity):
    """
    Projectile fired from a weapon
    """

    game: 'Game'
    damage: float
    mass: int
    poly: Polygon
    pos: list[int, int]
    vel: float
    a_pos: float
    max_speed: int
    acceleration: int

    def __init__(self, game: 'Game', damage: float, mass: int, pos: list[int], speed: int, a_pos: float, image: pygame.image, poly=None) -> None:
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

        GenericEntity.__init__(self, game, pos, Sprite(pos, image), (0, 0))

        # if poly is None, create polygon from rect
        if poly is None:
            vertices = [self.sprite.rect.topleft,
                        self.sprite.rect.topright,
                        self.sprite.rect.bottomright,
                        self.sprite.rect.bottomleft]
            poly = Polygon(vertices)

        PhysicsObject.__init__(self, mass, speed, 0, pos, poly)

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

    def check_bound_collision(self) -> None:
        """
        Checks if the projectile is out of bounds

        :return: None
        """
        outer_bound = 100

        if self.pos[0] <= -outer_bound or self.pos[0] > MAP_WIDTH + outer_bound or self.pos[1] <= -outer_bound or\
                self.pos[1] > MAP_HEIGHT + outer_bound:
            self.delete()

    def update(self) -> None:
        """
        Updates the entity every tick
        :return: None
        """

        self.update_pos()
        self.update_sprite()
        self.check_bound_collision()

    def delete(self) -> None:
        """
        Deletes the entity from the game

        :return: None
        """

        GenericEntity.delete(self)
        self.game.projs.remove(self)


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

    target: HealthEntity
    accuracy: int       # how well a rocket can adjust its trajectory in order to hit the target

    def __int__(self, game: 'Game', damage: float, mass: int, pos: list[int], speed: int, a_pos: float,
                image: pygame.image, target: HealthEntity, accuracy: int, poly=None):
        super().__init__(game, damage, mass, pos, speed, a_pos, image)

        self.target = target
        self.accuracy = accuracy

    def track(self) -> None:
        """
        adjust the trajectory of the rocket based on the target's current position

        :return: None
        """


