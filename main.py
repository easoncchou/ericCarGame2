from game import *


if __name__ == '__main__':
    # set the size of the map
    game = Game(MAP_WIDTH, MAP_HEIGHT)
    # load the image for the car
    car_image = pygame.image.load("assets/car1.png")
    # Resize
    car_image = pygame.transform.scale(
        car_image,
        (40, 75),
    )
    game.add_car(Car(20, [100, 100], 300, 2000, 100, 100, car_image))
    game.run_game_loop()
