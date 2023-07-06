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
        self.all_sprites_group = pygame.sprite.Group()

        self.cars = []

        # can set title later

    def add_car(self, car: Car) -> None:
        """
        Adds a car to self.cars

        :param car: Car to add
        :return:
        """

        self.cars.append(car)
        self.all_sprites_group.add(car.sprite)

    def run_game_loop(self) -> None:
        """
        Runs the game loop

        :return:
        """

        while not self.done:
            # handle events
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    self.done = True

            # render
            self.screen.fill((255, 255, 255))
            self.all_sprites_group.update()
            self.all_sprites_group.draw(self.screen)

            # update display
            pygame.display.flip()
            self.clock.tick(60)
