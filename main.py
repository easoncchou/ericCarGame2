from game import *


if __name__ == '__main__':
    game = Game(MAP_WIDTH, MAP_HEIGHT)
    game.add_car(Car(20, (40, 75), [100, 100], 5))
    game.run_game_loop()
