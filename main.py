from game import *


if __name__ == '__main__':
    game = Game(500, 500)
    game.add_car(Car(20, (16, 36), 5))
    game.run_game_loop()
