from game import *


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
    init_pos = [100, 100]

    # define the pygame sprite for the machine gun
    gun_image = pygame.image.load("assets/machine_gun1.png")
    gun_image = pygame.transform.scale(gun_image, [70, 70])

    # define the pygame sprite for the rocket launcher
    launcher_image = pygame.image.load("assets/rocket_launcher1.png")
    launcher_image = pygame.transform.scale(launcher_image, [70, 70])

    # create car and wep
    car = Car(game, 20, init_pos, 250, 2000, 100, 100, 500, (0, 0), car_image)
    wep1 = MachineGun(game, car, init_pos, 20, 10, 500, (10, 10), gun_image)
    wep2 = RocketLauncher(game, car, init_pos, 100, 60, 500, (0, -10), launcher_image)

    # add wep to car and car to game
    car.set_weapon(wep2)
    game.set_car(car)

    # add target
    target_image = pygame.surface.Surface((50, 50))
    target_image.fill(RED)
    target = Target(game, [400, 400], 500, target_image)

    game.add_target(target)

    # run game
    game.run_game_loop()

