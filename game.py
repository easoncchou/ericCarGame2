import pymunk
import pymunk.pygame_util
import pygame
import math
from typing import Union

from constants import *
from entities import GenericEntity, HealthEntity
from car_2 import Car2
from projectiles import Projectile
from enemy import Target


class Game:
    """
    Game class containing the game loop
    """

    space: pymunk.Space
    done: bool
    size: tuple[int, int]
    car: Union[Car2, None]
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

        # collision handler
        def hit(arbiter, space, data):
            for proj in self.projs:
                if proj.shape == arbiter.shapes[0]:
                    for enemy in self.enemies:
                        if enemy.shape == arbiter.shapes[1]:
                            enemy.hp -= proj.damage

                    self.delete_proj(proj)

            return True

        h = self.space.add_collision_handler(COLL_PROJ, COLL_ENEM)
        h.begin = hit

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

        self.add_entity(car.hp_bar)

    def add_entity(self, ent: GenericEntity) -> None:
        """
        Add an Entity

        :param ent: Entity to add
        :return:
        """
        self.all_sprites_group.add(ent.sprite)
        self.ents.append(ent)

    def delete_entity(self, ent: GenericEntity) -> None:
        """
        Delete an Entity

        :param ent: Entity to remove
        :return: None
        """

        self.all_sprites_group.remove(ent.sprite)
        self.ents.remove(ent)

    def add_target(self, target: Target) -> None:
        """
        Add a Target

        :param target: Target to add
        :return: None
        """

        self.add_entity(target)
        self.enemies.append(target)
        self.space.add(target.body, target.shape)

        self.add_entity(target.hp_bar)

    def delete_target(self, target: Target) -> None:
        """
        Delete the Target

        :param target: Target to delete
        :return:
        """

        self.delete_entity(target)
        self.enemies.remove(target)
        self.space.remove(target.body, target.shape)

    def add_proj(self, proj: Projectile) -> None:
        """
        Add a Projectile

        :param proj: Projectile to add
        :return:
        """

        self.add_entity(proj)
        self.projs.append(proj)
        self.space.add(proj.body, proj.shape)

    def delete_proj(self, proj: Projectile) -> None:
        """
        Delete a Projectile

        :param proj: Projectile to delete
        :return:
        """

        self.delete_entity(proj)
        self.projs.remove(proj)
        self.space.remove(proj.body, proj.shape)

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
                new_proj = self.car.wep.shoot()
                if new_proj is not None:
                    self.add_proj(new_proj)

            # update all entities
            for ent in self.ents:
                ent.update()

                if isinstance(ent, Projectile):
                    if ent.collide_bounds():
                        self.delete_proj(ent)
                elif isinstance(ent, Target):
                    if ent.hp <= 0:
                        self.delete_target(ent)
                        self.delete_entity(ent.hp_bar)

            # tick physics
            for i in range(16):
                self.space.step(1 / TICKRATE / 16)

            # render
            self.screen.fill(WHITE)

            # debug speedometer todo remove later
            font = pygame.font.SysFont(None, 48)
            img = font.render(str(round(abs(self.car.car_body.velocity), 1)), True, BLUE)
            self.screen.blit(img, (MAP_WIDTH - 120, MAP_HEIGHT - 80))

            self.all_sprites_group.update()
            self.all_sprites_group.draw(self.screen)

            options = pymunk.pygame_util.DrawOptions(self.screen)
            self.space.debug_draw(options)

            # update display
            pygame.display.flip()
            self.clock.tick(60)
