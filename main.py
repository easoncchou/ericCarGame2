from game import *


if __name__ == '__main__':
    game = Game(500, 500)
    game.add_car(Car(20, 800, (16, 36), 1))
    game.run_game_loop()
