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
    projs: list[Projectile]

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
        self.projs = []

        # can set title later

    def add_car(self, car: Car) -> None:
        """
        Adds a car to self.cars

        :param car: Car to add
        :return: None
        """

        self.cars.append(car)
        self.all_sprites_group.add(car.sprite)
        self.all_sprites_group.add(car.wep.sprite)

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
            if keys[pygame.K_w]:
                self.cars[0].apply_force_tan(UP)
                # TODO change from cars[0]
            if keys[pygame.K_s]:
                self.cars[0].apply_force_tan(DOWN)
            if keys[pygame.K_d]:
                self.cars[0].steer_car(RIGHT)
            if keys[pygame.K_a]:
                self.cars[0].steer_car(LEFT)

            # handle mouse
            x, y = pygame.mouse.get_pos()

            try:
                if y - self.cars[0].pos[1] >= 0:
                    self.cars[0].wep.a_pos = math.atan((x - self.cars[0].pos[0]) / (y - self.cars[0].pos[1]))
                else:
                    self.cars[0].wep.a_pos = math.pi + math.atan((x - self.cars[0].pos[0]) / (y - self.cars[0].pos[1]))
            except ZeroDivisionError:
                # if there's a zero division error, then do nothing
                pass

            m_buttons = pygame.mouse.get_pressed()
            if m_buttons[0]:
                new_proj = self.cars[0].wep.shoot()
                if new_proj is not None:
                    self.projs.append(new_proj)
                    self.all_sprites_group.add(new_proj.sprite)

            # update cars
            for car in self.cars:
                car.check_wall_collision()
                car.update_pos()
                car.update_sprite()

            # update projectiles
            for proj in self.projs:
                proj.update_pos()
                proj.update_sprite()

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
