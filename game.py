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

        :param width: width of the screen
        :param height: height of the screen
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
        :return: None
        """

        self.cars.append(car)
        self.all_sprites_group.add(car.sprite)

    def run_game_loop(self) -> None:
        """
        Runs the game loop

        :return: None
        """

        while not self.done:
            # handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            # handle keyboard
            #   better to handle this way to account for holding down key
            #   presses
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.cars[0].apply_force_tan("up")
                # TODO change from cars[0]
            if keys[pygame.K_DOWN]:
                self.cars[0].apply_force_tan("down")
            if keys[pygame.K_RIGHT]:
                self.cars[0].steer_car("right")
            if keys[pygame.K_LEFT]:
                self.cars[0].steer_car("left")

            # update cars
            for car in self.cars:
                car.check_wall_collision()
                car.update_pos()
                car.update_sprite()

            # render
            self.screen.fill(WHITE)

            # debug draw polygon todo remove later
            polygon_vertices = list(self.cars[0].poly.exterior.coords)
            pygame.draw.polygon(self.screen, RED, polygon_vertices)

            # debug speedometer todo remove later
            font = pygame.font.SysFont(None, 48)
            img = font.render(str(round(self.cars[0].vel, 1)), True, BLUE)
            self.screen.blit(img, (MAP_WIDTH - 120, MAP_HEIGHT - 80))

            self.all_sprites_group.update()
            self.all_sprites_group.draw(self.screen)

            # update display
            pygame.display.flip()
            self.clock.tick(60)
