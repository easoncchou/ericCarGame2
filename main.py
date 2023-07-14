from game import *


if __name__ == '__main__':
    game = Game(MAP_WIDTH, MAP_HEIGHT)
    car_image = pygame.image.load("assets/car1.png")
    # Resize
    car_image = pygame.transform.scale(
        car_image,
        (40, 75),
    )
    game.add_car(Car(20, [100, 100], 200, 2000, 100, 2, car_image))
    game.run_game_loop()
