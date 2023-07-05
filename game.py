import pygame

from car import *


class Game:
    """
    Game class containing the game loop

    === Attributes ===
    done: whether the game loop is done
    """

    done: bool
    size: tuple[int, int]
    cars: list[Car]

    def __init__(self, width: int, height: int) -> None:
        """
        Initializer
        """

        pygame.init()

        self.done = False
        self.size = (width, height)
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        self.cars = []

        # can set title later

    def add_car(self, car: Car) -> None:
        """
        Adds a car to self.cars

        :param car: Car to add
        :return:
        """

        self.cars.append(car)

    def run_game_loop(self) -> None:
        """
        Runs the game loop

        :return:
        """

        while not self.done:
            # render
            self.screen.fill((255, 255, 255))
            for car in self.cars:
                car.sprite.update()

            # update display
            pygame.display.flip()
            self.clock.tick(60)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, w: int, h: int, color: tuple[int, int, int]):
        # Call superclass constructor
        super().__init__()

        self.image = pygame.Surface([w, h])
        self.image.fill(color)
