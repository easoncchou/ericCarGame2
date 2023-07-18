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
    gun_image = pygame.surface.Surface((10, 30))
    gun_image.fill(GREY)

    # create car and wep
    car = Car(game, 20, init_pos, 250, 2000, 100, 100, 500, car_image)
    wep = MachineGun(game, car, init_pos, 20, 10, 500, gun_image)

    # add wep to car and car to game
    car.set_weapon(wep)
    game.set_car(car)

    # add target
    target_image = pygame.surface.Surface((50, 50))
    target_image.fill(RED)
    target = Target(game, [400, 400], 500, target_image)

    game.add_target(target)

    # run game
    game.run_game_loop()

