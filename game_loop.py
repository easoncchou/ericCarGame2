import pymunk

from constants import *

from game import Game
from car_2 import Car2
from enemy import Target, MovingTarget
from weapon import MachineGun, RocketLauncher, LaserCannon


def run_game_loop():
    import pygame

    pygame.init()

    done = False
    size = (MAP_WIDTH, MAP_HEIGHT)
    screen = pygame.display.set_mode(size)
    all_sprites_group = pygame.sprite.Group()
    clock = pygame.time.Clock()

    game = Game(screen, all_sprites_group, 0)

    init_pos = pymunk.Vec2d(300, 300)

    # load the image for the car
    car_image = pygame.image.load("assets/car1.png")
    # Resize
    car_image = pygame.transform.scale(
        car_image,
        (45, 80),
    )

    # define the pygame sprite for the machine gun
    gun_image = pygame.image.load("assets/machine_gun1.png")
    gun_image = pygame.transform.scale(gun_image, [40, 70])

    # define the pygame sprite for the rocket launcher
    launcher_image = pygame.image.load("assets/rocket_launcher1.png")
    launcher_image = pygame.transform.scale(launcher_image, [30, 70])

    # define the pygame sprite for the laser cannon
    cannon_image = pygame.image.load("assets/laser_cannon1.png")
    cannon_image = pygame.transform.scale(cannon_image, [60, 85])

    # create car and wep
    car = Car2(game.space, 1000, init_pos, 250, car_image)
    wep1 = MachineGun(init_pos, 20, 10, 500, pymunk.Vec2d(-4, 15), gun_image)
    wep2 = RocketLauncher(init_pos, 300, 60, 500, pymunk.Vec2d(0, 18),
                          launcher_image)
    wep3 = LaserCannon(init_pos, 5, 0, None, 500, pymunk.Vec2d(0, 25),
                       cannon_image)

    # add wep to car and car to game
    car.set_weapon(wep1)
    game.add_car(car, 0)

    # add target
    target_image = pygame.surface.Surface((50, 50))
    target_image.fill(RED)
    target1 = Target(pymunk.Vec2d(200, 200), 1500, target_image)
    target2 = Target(pymunk.Vec2d(300, 200), 1500, target_image)
    m_target = MovingTarget(pymunk.Vec2d(200, 200), pymunk.Vec2d(500, 500),
                            1500, target_image)

    game.add_target(target1)
    game.add_target(target2)

    while not done:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        game.handle_input()
        game.update()
        game.render()
        clock.tick(TICKRATE)

