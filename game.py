import pymunk
import pymunk.pygame_util
import pygame
import math
from typing import Union

import shapely

from constants import *
from sprite import Sprite
from entities import GenericEntity, HealthEntity, Reticle, Explosion
from car_2 import Car2
from weapon import MachineGun, RocketLauncher, LaserCannon
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
        self.space.damping = 0.7

        # add walls
        # Create a ground shape (a segment in this case)
        bottom_wall_shape = pymunk.Segment(self.space.static_body, (0, 0), (0, height), 1)
        bottom_wall_shape.collision_type = COLLTYPE_WALL
        self.space.add(bottom_wall_shape)

        # Create other walls or boundaries as needed
        # Example: A left wall
        left_wall_shape = pymunk.Segment(self.space.static_body, (0, height), (width, height), 1)
        left_wall_shape.collision_type = COLLTYPE_WALL
        self.space.add(left_wall_shape)

        # Example: A right wall
        right_wall_shape = pymunk.Segment(self.space.static_body, (width, height), (width, 0), 1)
        right_wall_shape.collision_type = COLLTYPE_WALL
        self.space.add(right_wall_shape)

        # Example: A ceiling
        top_wall_shape = pymunk.Segment(self.space.static_body, (width, 0), (0, 0), 1)
        top_wall_shape.collision_type = COLLTYPE_WALL
        self.space.add(top_wall_shape)

        # collision handlers
        def bullet_coll(arbiter, space, data):
            # neat trick, if we add an attribute to the pymunk.Shape attribute in the enemy and proj initializer, we can get the entities associated easily
            proj = arbiter.shapes[0].ent
            enemy = arbiter.shapes[1].ent

            enemy.hp -= proj.damage
            self.delete_proj(proj)

            return True

        bullet_handler = self.space.add_collision_handler(COLLTYPE_BULLETPROJ, COLLTYPE_ENEM)
        bullet_handler.begin = bullet_coll

        def rocket_coll(arbiter, space, data):
            proj = arbiter.shapes[0].ent

            for enemy in self.enemies:
                if abs(enemy.pos - proj.pos) <= proj.explosion_radius:
                    enemy.hp -= proj.damage
                    # assume that the enemy has a body
                    enemy.body.apply_impulse_at_local_point((enemy.pos - proj.pos).normalized() * proj.explosion_force)

            self.add_entity(proj.explode())
            self.delete_proj(proj)

            return True

        rocket_handler = self.space.add_collision_handler(COLLTYPE_ROCKETPROJ, COLLTYPE_ENEM)
        rocket_handler.begin = rocket_coll

        def bullet_wall_coll(arbiter, space, data):
            proj = arbiter.shapes[0].ent
            self.delete_proj(proj)

            return True

        bullet_wall_handler = self.space.add_collision_handler(COLLTYPE_BULLETPROJ, COLLTYPE_WALL)
        bullet_wall_handler.begin = bullet_wall_coll

        rocket_wall_handler = self.space.add_collision_handler(COLLTYPE_ROCKETPROJ, COLLTYPE_WALL)
        rocket_wall_handler.begin = rocket_coll

        self.done = False
        self.size = (width, height)
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.all_sprites_group = pygame.sprite.Group()

        self.car = None
        self.ents = []
        self.enemies = []
        self.projs = []

        self.reticle = None

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

    def render(self) -> None:
        """
        Render graphics

        :return: None
        """
        # render
        self.screen.fill(WHITE)

        self.all_sprites_group.update()
        self.all_sprites_group.draw(self.screen)

        # debug pymunk
        options = pymunk.pygame_util.DrawOptions(self.screen)
        self.space.debug_draw(options)

        # debug speedometer todo remove later
        font = pygame.font.SysFont(None, 48)
        img = font.render(str(round(abs(self.car.body.velocity), 1)), True, BLUE)
        self.screen.blit(img, (MAP_WIDTH - 120, MAP_HEIGHT - 80))

        body_a = (-self.car.body.rotation_vector.angle) % (2 * math.pi)
        body_v = (math.pi / 2 - self.car.body.velocity.angle) % (2 * math.pi)

        if abs(body_a - body_v) < math.pi / 2:
            img = font.render('front', True, BLUE)
            self.screen.blit(img, (MAP_WIDTH - 120, MAP_HEIGHT - 160))
        else:
            img = font.render('back', True, BLUE)
            self.screen.blit(img, (MAP_WIDTH - 120, MAP_HEIGHT - 160))

        img = font.render(str(round(self.car.body.rotation_vector.angle, 4)), True, BLUE)
        self.screen.blit(img, (MAP_WIDTH - 120, MAP_HEIGHT - 200))

        # update display
        pygame.display.flip()

    def rl_track(self, x: int, y: int) -> None:
        """
        Tracking function for RocketLauncher
        :return: None
        """

        if self.car.wep.current_target is None:
            for enemy in self.enemies:
                # check if the mouse is within a radius of the enemy
                if abs(pymunk.Vec2d(x, y) - enemy.pos) < 100:
                    if self.car.wep.targeting_status == 0:
                        self.car.wep.current_target = enemy
        else:
            if abs(pymunk.Vec2d(x, y) - self.car.wep.current_target.pos) < 150:
                # the target has been followed by the mouse for long enough, so set it to the current target
                #   and reset the timer on targeting status
                if self.car.wep.targeting_status == OFF:
                    pass
                elif self.car.wep.targeting_status >= 100:
                    self.car.wep.targeting_status = OFF

                    if self.reticle is None:
                        reticle_image = pygame.image.load("assets/reticle1.png")
                        reticle_image = pygame.transform.scale(reticle_image, [140, 100])
                        reticle_pos = self.car.wep.current_target.pos
                        reticle_sprite = Sprite(reticle_pos, reticle_image)
                        self.reticle = Reticle(reticle_pos, reticle_sprite, self.car.wep.current_target)
                    else:
                        self.reticle.current_target = self.car.wep.current_target

                    self.add_entity(self.reticle)
                # the target hasn't been followed for long enough, so continue counting
                else:
                    self.car.wep.targeting_status += 1
            else:
                if self.car.wep.targeting_status == OFF and self.reticle in self.ents:
                    # delete reticle
                    self.delete_entity(self.reticle)
                    pass
                self.car.wep.targeting_status = 0
                self.car.wep.current_target = None

    def laser_length(self) -> float:
        """

        :return:
        """

        self.car.wep: LaserCannon

        to_endpoint = pymunk.Vec2d(0, self.car.wep.laser.length)
        to_endpoint = to_endpoint.rotated(-self.car.wep.laser.a_pos)
        line = shapely.LineString([self.car.wep.laser.pos, self.car.wep.pos + to_endpoint])

        closest = None
        closest_distance = 100000000

        for enemy in self.enemies:
            # print([point + enemy.pos for point in enemy.shape.get_vertices()])
            poly = shapely.Polygon([point + enemy.pos for point in enemy.shape.get_vertices()])

            if line.intersects(poly):
                # collides
                if closest is None:
                    closest = enemy
                    intersections = shapely.intersection(line, poly).coords
                    # get closest intersection
                    for point in intersections:
                        dist = abs(self.car.wep.laser.pos + pymunk.Vec2d(0, self.car.wep.barrel_len).rotated(-self.car.wep.a_pos) - point)
                        if dist < closest_distance:
                            closest_distance = dist
                else:
                    closest_dist = abs(self.car.wep.pos - closest.pos)
                    current_dist = abs(self.car.wep.pos - enemy.pos)
                    if current_dist < closest_dist:
                        closest = enemy
                        intersections = shapely.intersection(line, poly).coords
                        # get closest intersection
                        for point in intersections:
                            dist = abs(self.car.wep.laser.pos + pymunk.Vec2d(0, self.car.wep.barrel_len).rotated(-self.car.wep.a_pos) - point)
                            if dist < closest_distance:
                                closest_distance = dist

        if closest is not None:
            self.car.wep.laser.length = closest_distance

    def update(self) -> None:
        """
        Update the game every tick
        :return:
        """

        phys_tick = 8

        # tick physics
        for i in range(phys_tick):
            self.space.step(1 / TICKRATE / phys_tick)

        # update all entities
        for ent in self.ents:
            ent.update()

            if isinstance(ent, Target):
                if ent.hp <= 0:
                    self.delete_target(ent)
                    self.delete_entity(ent.hp_bar)
            elif isinstance(ent, Explosion):
                if ent.lifespan <= 0:
                    self.delete_entity(ent)

        if self.reticle is not None and self.reticle.current_target.hp <= 0:
            if self.reticle in self.ents:
                self.delete_entity(self.reticle)

    def handle_input(self) -> None:
        """
        Input handler

        :return: None
        """

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

        # handle keyboard
        #   better to handle this way to account for holding down key
        #   presses
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.car.accelerate(10 ** 6)
        if keys[pygame.K_s]:
            self.car.accelerate(-10 ** 6)

        th = 0
        if keys[pygame.K_d]:
            th += self.car.max_steering
        if keys[pygame.K_a]:
            th -= self.car.max_steering

        self.car.steer(th)

        # handle mouse
        x, y = pygame.mouse.get_pos()

        self.car.wep.a_pos = -(pymunk.Vec2d(x, y) - self.car.pos).angle + math.pi / 2

        # if the cars current weapon is a rocket launcher, start tracking
        if isinstance(self.car.wep, RocketLauncher):
            self.rl_track(x, y)

        m_buttons = pygame.mouse.get_pressed()
        if m_buttons[0]:
            new_proj = self.car.wep.shoot()
            if isinstance(self.car.wep, LaserCannon):

                self.car.wep.laser.length = 1000
                # calculate the length of the laser beam sprite based on collision
                self.laser_length()

                if new_proj is not None:
                    self.add_entity(new_proj)

            else:
                if new_proj is not None:
                    self.add_proj(new_proj)
        else:
            if isinstance(self.car.wep, LaserCannon) and self.car.wep.laser is not None:
                self.delete_entity(self.car.wep.laser)
                self.car.wep.laser = None

    def run_game_loop(self) -> None:
        """
        Runs the game loop

        :return: None
        """
        while not self.done:
            self.handle_input()

            self.update()

            self.render()

            self.clock.tick(60)
