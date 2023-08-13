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
    cars: dict[int, Car2]
    ents: list[GenericEntity]
    enemies: list[HealthEntity]
    projs: list[Projectile]

    def __init__(self, screen: pygame.display = None,
                 all_sprites_group: pygame.sprite.Group = None,
                 _id: int = -1) -> None:
        """
        Initializer

        :param width: width of the screen
        :param height: height of the screen
        """

        self.screen = screen
        self.all_sprites_group = all_sprites_group
        width, height = MAP_WIDTH, MAP_HEIGHT

        self.space = pymunk.Space()
        self.space.damping = 0.7

        # add walls
        # Create a ground shape (a segment in this case)
        bottom_wall_shape = pymunk.Segment(self.space.static_body, (0, 0),
                                           (0, height), 1)
        bottom_wall_shape.collision_type = COLLTYPE_WALL
        self.space.add(bottom_wall_shape)

        # Create other walls or boundaries as needed
        # Example: A left wall
        left_wall_shape = pymunk.Segment(self.space.static_body, (0, height),
                                         (width, height), 1)
        left_wall_shape.collision_type = COLLTYPE_WALL
        self.space.add(left_wall_shape)

        # Example: A right wall
        right_wall_shape = pymunk.Segment(self.space.static_body,
                                          (width, height), (width, 0), 1)
        right_wall_shape.collision_type = COLLTYPE_WALL
        self.space.add(right_wall_shape)

        # Example: A ceiling
        top_wall_shape = pymunk.Segment(self.space.static_body, (width, 0),
                                        (0, 0), 1)
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

        bullet_handler = self.space.add_collision_handler(COLLTYPE_BULLETPROJ,
                                                          COLLTYPE_ENEM)
        bullet_handler.begin = bullet_coll

        def rocket_coll(arbiter, space, data):
            proj = arbiter.shapes[0].ent

            for enemy in self.enemies:
                if abs(enemy.pos - proj.pos) <= proj.explosion_radius:
                    enemy.hp -= proj.damage
                    # assume that the enemy has a body
                    enemy.body.apply_impulse_at_local_point((
                                                                        enemy.pos - proj.pos).normalized() * proj.explosion_force)

            self.add_entity(proj.explode())
            self.delete_proj(proj)

            return True

        rocket_handler = self.space.add_collision_handler(COLLTYPE_ROCKETPROJ,
                                                          COLLTYPE_ENEM)
        rocket_handler.begin = rocket_coll

        def bullet_wall_coll(arbiter, space, data):
            proj = arbiter.shapes[0].ent
            self.delete_proj(proj)

            return True

        bullet_wall_handler = self.space.add_collision_handler(
            COLLTYPE_BULLETPROJ, COLLTYPE_WALL)
        bullet_wall_handler.begin = bullet_wall_coll

        rocket_wall_handler = self.space.add_collision_handler(
            COLLTYPE_ROCKETPROJ, COLLTYPE_WALL)
        rocket_wall_handler.begin = rocket_coll

        self.id = _id
        self.car = None
        self.ents = []
        self.cars = {}
        self.enemies = []
        self.projs = []

        self.reticle = None

        # can set title later

    def add_car(self, car: Car2, _id: int) -> None:
        """
        Adds a car to self.cars

        :param car: Car to add
        :param _id: id of the Car to add
        :return: None
        """

        self.cars[_id] = car

        if self.id == _id:
            self.car = car

        self.add_entity(car)
        self.add_entity(car.wep)
        self.add_entity(car.hp_bar)

    def add_entity(self, ent: GenericEntity) -> None:
        """
        Add an Entity

        :param ent: Entity to add
        :return:
        """
        if self.all_sprites_group is not None:
            self.all_sprites_group.add(ent.sprite)
        self.ents.append(ent)

    def delete_entity(self, ent: GenericEntity) -> None:
        """
        Delete an Entity

        :param ent: Entity to remove
        :return: None
        """

        if self.all_sprites_group is not None:
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

        tile_dim = pymunk.Vec2d(100, 100)
        tile = pygame.Surface(tile_dim)
        tile.fill(BLACK)
        sub_tile = pygame.Surface(tile_dim // 2)
        sub_tile.fill(MAGENTA)
        tile.blit(sub_tile, (0, 0))
        tile.blit(sub_tile, tile_dim // 2)

        x_off = (-self.car.pos.x) % tile_dim.x
        y_off = (-self.car.pos.y) % tile_dim.y

        # vert tile
        vert_tile = pygame.Surface((tile_dim.x, SCREEN_HEIGHT))
        curr_y = y_off - tile_dim.y
        while curr_y < SCREEN_HEIGHT:
            vert_tile.blit(tile, (0, curr_y))
            curr_y += tile_dim.y

        # tile screen with vert tile
        curr_x = x_off - tile_dim.x
        while curr_x < SCREEN_WIDTH:
            self.screen.blit(vert_tile, (curr_x, 0))
            curr_x += tile_dim.x

        if self.all_sprites_group is not None:
            self.all_sprites_group.update()
            self.all_sprites_group.draw(self.screen)

        # debug pymunk
        options = pymunk.pygame_util.DrawOptions(self.screen)
        # self.space.debug_draw(options)

        # debug speedometer todo remove later
        font = pygame.font.SysFont(None, 48)
        img = font.render(str(round(abs(self.car.body.velocity), 1)), True,
                          BLUE)
        self.screen.blit(img, (MAP_WIDTH - 120, MAP_HEIGHT - 80))

        body_a = (-self.car.body.rotation_vector.angle) % (2 * math.pi)
        body_v = (math.pi / 2 - self.car.body.velocity.angle) % (2 * math.pi)

        if abs(body_a - body_v) < math.pi / 2:
            img = font.render('front', True, BLUE)
            self.screen.blit(img, (MAP_WIDTH - 120, MAP_HEIGHT - 160))
        else:
            img = font.render('back', True, BLUE)
            self.screen.blit(img, (MAP_WIDTH - 120, MAP_HEIGHT - 160))

        img = font.render(str(round(self.car.body.rotation_vector.angle, 4)),
                          True, BLUE)
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
                        reticle_image = pygame.transform.scale(reticle_image,
                                                               [140, 100])
                        reticle_pos = self.car.wep.current_target.pos
                        reticle_sprite = Sprite(reticle_pos, reticle_image)
                        self.reticle = Reticle(reticle_pos, reticle_sprite,
                                               self.car.wep.current_target)
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

    def laser_collide(self) -> tuple[pymunk.Vec2d, Union[HealthEntity, None]]:
        """

        :return:
        """

        self.car.wep: LaserCannon

        contact = self.car.wep.laser.pos + pymunk.Vec2d(0,
                                                        self.car.wep.laser.max_length).rotated(
            -self.car.wep.laser.a_pos)
        line = shapely.LineString([self.car.wep.laser.pos, contact])

        # determine the length of the laser if it were to hit a wall
        barrier_definition = shapely.LineString(
            [[0, 0], [MAP_WIDTH, 0], [MAP_WIDTH, MAP_HEIGHT], [0, MAP_HEIGHT],
             [0, 0]])
        wall_contact = shapely.intersection(line, barrier_definition).coords

        if len(wall_contact) == 1:
            contact = wall_contact[0]

        # determine the length of the laser if it were to hit an enemy
        closest_distance = abs(self.car.wep.laser.pos - contact)
        closest_enemy = None

        for enemy in self.enemies:
            # print([point + enemy.pos for point in enemy.shape.get_vertices()])
            poly = shapely.Polygon(
                [point + enemy.pos for point in enemy.shape.get_vertices()])

            if line.intersects(poly):
                # collides
                intersections = shapely.intersection(line, poly).coords
                # get closest intersection
                for point in intersections:
                    dist = abs(self.car.wep.laser.pos - point)
                    if dist < closest_distance:
                        closest_distance = dist
                        contact = point
                        closest_enemy = enemy

        # calculate and perform the laser's damage if it hits an enemy
        return contact, closest_enemy

    def update(self) -> None:
        """
        Update the game every tick
        :return:
        """

        phys_tick = 8

        # tick physics
        for i in range(phys_tick):
            for _id, car in self.cars.items():
                car.update_grooves()
            self.space.step(1 / TICKRATE / phys_tick)

        # update all entities
        for ent in self.ents:
            if self.id != -1:
                ent.car_pos = self.car.pos
                ent.find_relative_pos()

            ent.update()

            if isinstance(ent, Target):
                if ent.hp <= 0:
                    self.delete_target(ent)
                    self.delete_entity(ent.hp_bar)

                    if isinstance(self.car.wep, RocketLauncher):
                        self.car.wep.current_target = None
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

        self.car.wep.a_pos = -(
                    pymunk.Vec2d(x, y) - self.car.screen_pos).angle + math.pi / 2

        # if the cars current weapon is a rocket launcher, start tracking
        if isinstance(self.car.wep, RocketLauncher):
            self.rl_track(x, y)

        m_buttons = pygame.mouse.get_pressed()
        if m_buttons[0]:  # pressed down left mouse button
            # attempt to shoot
            new_proj = self.car.wep.shoot()

            # if weapon is a laser cannon
            if isinstance(self.car.wep, LaserCannon):
                # calculate the length of the laser beam sprite based on collision
                laser_contact_pos, closest_enemy = self.laser_collide()
                self.car.wep.laser_contact.pos = laser_contact_pos
                self.car.wep.laser.length = abs(
                    self.car.wep.laser.pos - laser_contact_pos)

                if closest_enemy is not None:
                    if self.car.wep.curr_atk_cd <= 0:
                        self.car.wep.curr_atk_cd = self.car.wep.atk_cd
                        closest_enemy.hp -= self.car.wep.laser.damage

                if new_proj is not None:
                    self.add_entity(new_proj)
                    self.add_entity(self.car.wep.laser_contact)

            # if the weapon isn't a laser cannon
            else:
                if new_proj is not None:
                    self.add_proj(new_proj)
        else:  # let go of left mouse button
            if isinstance(self.car.wep,
                          LaserCannon) and self.car.wep.laser is not None:
                self.delete_entity(self.car.wep.laser)
                self.delete_entity(self.car.wep.laser_contact)
                self.car.wep.laser = None
