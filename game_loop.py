import pymunk

from constants import *

from game import Game
from car_2 import Car2
from enemy import Target, MovingTarget
from weapon import MachineGun, RocketLauncher, LaserCannon
from terrain import Terrain, BoundaryWall, CoverWall
from entities import AmmoBox


def run_game_loop():
    import pygame

    pygame.init()

    done = False
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)
    all_sprites_group = pygame.sprite.Group()
    clock = pygame.time.Clock()

    game = Game(screen, all_sprites_group, 0)

    init_pos = pymunk.Vec2d(MAP_WIDTH / 2 - 200, MAP_HEIGHT / 2 - 200)

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
    wep1 = MachineGun(init_pos, 20, 10, 100, pymunk.Vec2d(-4, 15), gun_image)
    wep2 = RocketLauncher(init_pos, 300, 60, 25, pymunk.Vec2d(0, 18),
                          launcher_image)
    wep3 = LaserCannon(init_pos, 5, 0, None, 200, pymunk.Vec2d(0, 25),
                       cannon_image)

    # add wep to car and car to game
    car.set_weapon(wep3)
    game.add_car(car, 0)

    # add target
    target_image = pygame.surface.Surface((50, 50))
    target_image.fill(RED)
    target1 = Target(pymunk.Vec2d(200, 200), 1500, target_image)
    target2 = Target(pymunk.Vec2d(MAP_WIDTH - 200, MAP_HEIGHT - 300), 1500, target_image)
    m_target = MovingTarget(pymunk.Vec2d(200, 200), pymunk.Vec2d(500, 500),
                            1500, target_image)

    game.add_target(target1)
    game.add_target(target2)

    # add terrain
    # add boundary walls
    boundary_top = BoundaryWall(game.space, 0, pymunk.Vec2d(MAP_WIDTH / 2, 0), MAP_WIDTH, 10)
    boundary_bot = BoundaryWall(game.space, 0, pymunk.Vec2d(MAP_WIDTH / 2, MAP_HEIGHT), MAP_WIDTH, 10)
    boundary_left = BoundaryWall(game.space, 0, pymunk.Vec2d(0, MAP_HEIGHT / 2), 10, MAP_HEIGHT)
    boundary_right = BoundaryWall(game.space, 0, pymunk.Vec2d(MAP_WIDTH, MAP_HEIGHT / 2), 10, MAP_HEIGHT)
    game.add_terrain(boundary_top)
    game.add_terrain(boundary_bot)
    game.add_terrain(boundary_left)
    game.add_terrain(boundary_right)

    # add cover walls
    cover_wall_1 = CoverWall(game.space, 0, pymunk.Vec2d(MAP_WIDTH - 300, 250), 150, 10)
    game.add_terrain(cover_wall_1)
    cover_wall_2 = CoverWall(game.space, 0, pymunk.Vec2d(300, MAP_HEIGHT - 200), 10, 150)
    game.add_terrain(cover_wall_2)

    # add a ammo box once
    # ammo_box_1 = AmmoBox(100, 100)
    # game.add_ammo_box(ammo_box_1)

    while not done:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        game.handle_input()
        game.update()
        game.render()
        clock.tick(TICKRATE)

