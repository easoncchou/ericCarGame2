from physics_object import *
from sprite import *
from weapon import *


class Car(PhysicsObject):
    """
    Car class
    """

    mass: int
    size: tuple[int, int]
    pos: list[int, int]
    vel: float
    a_pos: float
    a_vel: float
    sprite: Sprite
    wep: Weapon

    def __init__(self, mass: int, pos: list[int], max_speed: int,
                 acceleration: int, max_a_speed: int, handling: int, image: pygame.image, wep: Weapon, poly=None) -> None:
        """
        Initializer

        :param mass: mass of the car
        :param handling: how well a car steers/turns (the higher the value the faster it turns)
        :param poly: polygon representing the shape of the car, rectangle by default
        """

        self.sprite = Sprite(pos, image)
        self.max_a_speed = max_a_speed
        self.handling = handling
        self.wep = wep

        # if poly is None, create polygon from rect
        if poly is None:
            vertices = [self.sprite.rect.topleft,
                        self.sprite.rect.topright,
                        self.sprite.rect.bottomright,
                        self.sprite.rect.bottomleft]
            poly = Polygon(vertices)

        super().__init__(mass, max_speed, acceleration, pos, poly)

    def steer_car(self, direction: int) -> None:
        """
        Steers the car by changing the angular velocity of the car

        :param direction: direction of the force
        :return: None
        """

        # calculate the angular velocity

        a_vel = self.vel / self.handling

        if a_vel >= self.max_a_speed:
            a_vel = self.max_a_speed

        #   determine the direction of normal acceleration
        if direction == RIGHT:
            a_vel *= -1

        # update the angular position
        dth = a_vel * (1 / TICKRATE)
        self.a_pos += dth
        self.poly = rotate(self.poly, - dth * 180 / math.pi)

    def update_sprite(self) -> None:
        """
        Update the sprite

        :return: None
        """

        self.sprite.image = pygame.transform.rotate(self.sprite.original_image, ((180 / math.pi) * self.a_pos))
        self.sprite.rect = self.sprite.image.get_rect(center=self.sprite.image.get_rect(center=(self.pos[0], self.pos[1])).center)

        self.wep.update_sprite(self.pos)
