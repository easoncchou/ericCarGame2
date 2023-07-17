from car import *
from entities import *


class Game:
    """
    Game class containing the game loop

    === Attributes ===
    done: whether the game loop is done
    """

    done: bool
    size: tuple[int, int]
    car: Car
    ents: list[GenericEntity]

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

        self.car = None
        self.ents = []

        # can set title later

    def set_car(self, car: Car) -> None:
        """
        Adds a car to self.cars

        :param car: Car to add
        :return: None
        """

        self.car = car
        self.all_sprites_group.add(car.sprite)
        self.all_sprites_group.add(car.wep.sprite)

        self.ents.append(car)

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
                self.car.apply_force_tan(UP)
                # TODO change from car
            if keys[pygame.K_s]:
                self.car.apply_force_tan(DOWN)
            if keys[pygame.K_d]:
                self.car.steer_car(RIGHT)
            if keys[pygame.K_a]:
                self.car.steer_car(LEFT)

            # handle mouse
            x, y = pygame.mouse.get_pos()

            try:
                if y - self.car.pos[1] >= 0:
                    self.car.wep.a_pos = math.atan((x - self.car.pos[0]) / (y - self.car.pos[1]))
                else:
                    self.car.wep.a_pos = math.pi + math.atan((x - self.car.pos[0]) / (y - self.car.pos[1]))
            except ZeroDivisionError:
                # if there's a zero division error, then do nothing
                pass

            m_buttons = pygame.mouse.get_pressed()
            if m_buttons[0]:
                new_proj = self.car.wep.shoot()
                if new_proj is not None:
                    self.ents.append(new_proj)
                    self.all_sprites_group.add(new_proj.sprite)

            # update all entities and check collision between entities
            for ent in self.ents:
                ent.update()



            # render
            self.screen.fill(WHITE)

            # debug draw polygon todo remove later
            polygon_vertices = list(self.car.poly.exterior.coords)
            pygame.draw.polygon(self.screen, RED, polygon_vertices)

            # debug speedometer todo remove later
            font = pygame.font.SysFont(None, 48)
            img = font.render(str(round(self.car.vel, 1)), True, BLUE)
            self.screen.blit(img, (MAP_WIDTH - 120, MAP_HEIGHT - 80))

            self.all_sprites_group.update()
            self.all_sprites_group.draw(self.screen)

            # update display
            pygame.display.flip()
            self.clock.tick(60)
