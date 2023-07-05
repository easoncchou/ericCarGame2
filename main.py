from game import *


if __name__ == '__main__':
    game = Game(500, 500)
    game.add_car(Car(20, 800, (5, 15), (2.5, 7.5)))
    game.run_game_loop()
