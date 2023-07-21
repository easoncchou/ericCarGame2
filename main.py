import pygame
import pymunk

from constants import *
from game import Game
from car_2 import Car2
from enemy import Target, MovingTarget
from weapon import MachineGun, RocketLauncher


if __name__ == '__main__':
    # create game
    game = Game(MAP_WIDTH, MAP_HEIGHT)

    # load the image for the car
    car_image = pygame.image.load("assets/car1.png")
    # Resize
    car_image = pygame.transform.scale(
        car_image,
        (40, 75),
    )
    init_pos = pymunk.Vec2d(100, 100)

    # define the pygame sprite for the machine gun
    gun_image = pygame.image.load("assets/machine_gun1.png")
    gun_image = pygame.transform.scale(gun_image, [70, 70])

    # define the pygame sprite for the rocket launcher
    launcher_image = pygame.image.load("assets/rocket_launcher1.png")
    launcher_image = pygame.transform.scale(launcher_image, [70, 70])

    # create car and wep
    car = Car2(game.space, 1000, init_pos, 250, car_image)
    wep1 = MachineGun(init_pos, 20, 10, 500, (10, 10), gun_image)
    wep2 = RocketLauncher(init_pos, 100, 60, 500, (0, 18), launcher_image)

    # add wep to car and car to game
    car.set_weapon(wep2)
    game.set_car(car)

    # add target
    target_image = pygame.surface.Surface((50, 50))
    target_image.fill(RED)
    target = MovingTarget(pymunk.Vec2d(200, 200), pymunk.Vec2d(500, 500), 1500, target_image)

    game.add_target(target)

    # run game
    game.run_game_loop()

