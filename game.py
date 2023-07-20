import itertools
import pymunk
import pygame

from entities import *
from car_2 import *
from projectiles import *
from enemy import *
from physics_object import *


class Game:
    """
    Game class containing the game loop

    === Attributes ===
    done: whether the game loop is done
    """

    space: pymunk.Space
    done: bool
    size: tuple[int, int]
    car: Car2
    ents: list[GenericEntity]
    enemies: list[HealthEntity]
    projs: list[Projectile]

    def __init__(self, width: int, height: int) -> None:
        """
        Initializer

        :param width: width of the screen
        :param height: height of the screen
        """

        pygame.init()
        self.space = pymunk.Space()
        self.space.damping = 0.9

        self.done = False
        self.size = (width, height)
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.all_sprites_group = pygame.sprite.Group()

        self.car = None
        self.ents = []
        self.enemies = []
        self.projs = []

        # can set title later

    def set_car(self, car: Car2) -> None:
        """
        Adds a car to self.cars

        :param car: Car to add
        :return: None
        """

        self.car = car
        self.all_sprites_group.add(car.sprite)
        self.all_sprites_group.add(car.wep.sprite)

        self.ents.append(car)

    def add_target(self, target: Target) -> None:
        """
        Adds a target to shoot at

        :param target: target object to add
        :return:
        """
        self.all_sprites_group.add(target.sprite)
        self.ents.append(target)
        self.enemies.append(target)

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
            """
            
            if keys[pygame.K_w]:
                force = pymunk.Vec2d(0, 1000)
                point = pymunk.Vec2d(0, -30)
                self.car.body.apply_force_at_local_point(force, point)
            if keys[pygame.K_s]:
                force = pymunk.Vec2d(0, -1000)
                point = pymunk.Vec2d(0, -30)
                self.car.body.apply_force_at_local_point(force, point)
            if keys[pygame.K_d]:
                force = pymunk.Vec2d(-5000, -100)
                point = pymunk.Vec2d(-5, 30)
                pivot = pymunk.Vec2d(0, -30)
                self.car.body.apply_force_at_local_point(force, point)
                self.car.body.apply_force_at_local_point(-force, pivot)
            if keys[pygame.K_a]:
                force = pymunk.Vec2d(5000, -100)
                point = pymunk.Vec2d(5, 30)
                pivot = pymunk.Vec2d(0, -30)
                self.car.body.apply_force_at_local_point(force, point)
                self.car.body.apply_force_at_local_point(-force, pivot)
                """
            if keys[pygame.K_w]:
                self.car.accelerate(100000)
            if keys[pygame.K_s]:
                self.car.accelerate(-100000)

            th = 0
            if keys[pygame.K_d]:
                th += math.pi / 4
            if keys[pygame.K_a]:
                th -= math.pi / 4

            self.car.steer(th)

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
                self.car.wep.shoot()

            # update all entities
            for ent in self.ents:
                ent.update()

            # check collision of enemies with projectiles
            for enemy in self.enemies:
                for proj in self.projs:
                    if proj.collide(enemy):
                        enemy.hp -= proj.damage
                        proj.delete()

            # tick physics
            for i in range(16):
                self.space.step(1 / 60 / 16)

            # render
            self.screen.fill(WHITE)

            # debug speedometer todo remove later
            font = pygame.font.SysFont(None, 48)
            img = font.render(str(round(abs(self.car.body.velocity), 1)), True, BLUE)
            self.screen.blit(img, (MAP_WIDTH - 120, MAP_HEIGHT - 80))

            self.all_sprites_group.update()
            self.all_sprites_group.draw(self.screen)

            # debug draw car wheels/dir
            pygame.draw.circle(self.screen, RED, self.car.front_wheel.position, 2)
            pygame.draw.circle(self.screen, GREEN, self.car.back_wheel.position, 2)
            pygame.draw.line(self.screen, GREEN, self.car.front_wheel.position,
                             self.car.front_wheel.position + pymunk.Vec2d(0, 20).rotated(self.car.front_wheel.angle))
            pygame.draw.line(self.screen, BLUE, self.car.front_wheel_groove.groove_a, self.car.front_wheel_groove.groove_b)

            # update display
            pygame.display.flip()
            self.clock.tick(60)
