import asyncio
# import uvloop
import multiprocessing
import pymunk
import json

from constants import *
from ip_addr import *
import net

from game import Game
from car_2 import Car2
from enemy import Target, MovingTarget
from weapon import MachineGun, RocketLauncher, LaserCannon


async def handle_server(conn):
    reader, writer = await asyncio.open_connection(HOST, PORT)

    # on start-up, server will send {'id': x, 'init_pos': [x, y]}
    try:
        data = await net.read_message(reader)
        print(f'Received response from server: {data.decode()}')
        conn.send(data)
    except Exception as e:
        print(f'{type(e).__name__} while initializing: {e}')
        writer.close()
        await writer.wait_closed()
        return

    event = asyncio.Event()

    async def receive_data(event: asyncio.Event):
        while not event.is_set():
            try:
                data = await net.read_message(reader)

                # print(f'Received response from server: {data.decode()}')
                conn.send(data)
            except ConnectionError as e:
                print(f'{type(e).__name__} while reading: {e}')
                event.set()
            except Exception as e:
                print(f'{type(e).__name__} while reading: {e}')

    async def send_data(event: asyncio.Event):
        while not event.is_set():
            await asyncio.sleep(0)
            if conn.poll():
                msg = conn.recv()

                try:
                    await net.write_message(writer, msg)
                except ConnectionError as e:
                    print(f'{type(e).__name__} while writing: {e}')
                    event.set()
                except Exception as e:
                    print(f'{type(e).__name__} while writing: {e}')

    receive_task = asyncio.create_task(receive_data(event))
    send_task = asyncio.create_task(send_data(event))

    try:
        await asyncio.gather(receive_task, send_task)
    except asyncio.CancelledError:
        pass
    except Exception as e:
        print(f'Error: {e}')
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except Exception as e:
            print(f'{type(e).__name__} while closing: {e}')

        print(f"Connection to server closed")


def run_client_loop(conn):
    import pygame

    pygame.init()

    done = False
    size = (MAP_WIDTH, MAP_HEIGHT)
    screen = pygame.display.set_mode(size)
    all_sprites_group = pygame.sprite.Group()
    clock = pygame.time.Clock()

    # wait for the server connection to establish
    while not conn.poll():
        pass

    # on start-up, server will send {'init': {'id': x, 'init_pos': [x, y]}, add_cars: { ... }}
    msg = json.loads(conn.recv().decode())
    game = Game(screen, all_sprites_group, msg['init']['id'])

    # todo make adding car more general
    init_pos = pymunk.Vec2d(msg['init']['init_pos'][0],
                            msg['init']['init_pos'][1])

    # load the image for the car
    car_image = pygame.image.load('assets/car1.png')
    # Resize
    car_image = pygame.transform.scale(
        car_image,
        (45, 80),
    )

    # define the pygame sprite for the machine gun
    gun_image = pygame.image.load('assets/machine_gun1.png')
    gun_image = pygame.transform.scale(gun_image, [40, 70])

    # create car and wep
    car = Car2(game.space, 1000, init_pos, 250, car_image)
    wep1 = MachineGun(init_pos, 20, 10, 500, pymunk.Vec2d(-4, 15), gun_image)

    # add wep to car and car to game
    car.set_weapon(wep1)

    game.add_car(car, game.id)

    if msg.get('add_cars') is not None:
        for _id, car_info in msg.get('add_cars').items():
            # create car and wep
            car = Car2(game.space, 1000, pymunk.Vec2d(car_info['pos'][0], car_info['pos'][1]), 250, car_image)
            wep1 = MachineGun(init_pos, 20, 10, 500, pymunk.Vec2d(-4, 15), gun_image)

            # add wep to car and car to game
            car.set_weapon(wep1)
            car.body.angle = car_info['a_pos']
            car.update_grooves()
            car.body.velocity = car_info['vel']
            car.steering_angle = car_info['steering_angle']
            car.wep.a_pos = car_info['wep_angle']

            game.add_car(car, int(_id))

    while not done:
        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        if conn.poll():
            msg = json.loads(conn.recv().decode())
            if msg.get('remove_cars') is not None:
                for _id in msg.get('remove_cars'):
                    game.remove_car(_id)

            if msg.get('add_cars') is not None:
                for _id, init_pos in msg.get('add_cars').items():
                    init_pos = pymunk.Vec2d(init_pos[0], init_pos[1])
                    # load the image for the car
                    car_image = pygame.image.load('assets/car1.png')
                    # Resize
                    car_image = pygame.transform.scale(
                        car_image,
                        (45, 80),
                    )

                    # define the pygame sprite for the machine gun
                    gun_image = pygame.image.load('assets/machine_gun1.png')
                    gun_image = pygame.transform.scale(gun_image, [40, 70])

                    # create car and wep
                    car = Car2(game.space, 1000, init_pos, 250, car_image)
                    wep1 = MachineGun(init_pos, 20, 10, 500, pymunk.Vec2d(-4, 15), gun_image)

                    # add wep to car and car to game
                    car.set_weapon(wep1)

                    game.add_car(car, int(_id))

            if msg.get('update_cars') is not None:
                for _id, car_info in msg.get('update_cars').items():
                    if int(_id) != game.id and game.cars.get(int(_id)) is not None:
                        car = game.cars[int(_id)]
                        car.body.position = pymunk.Vec2d(car_info['pos'][0], car_info['pos'][1])
                        car.body.angle = car_info['a_pos']
                        car.update_grooves()
                        car.body.velocity = car_info['vel']
                        car.steering_angle = car_info['steering_angle']
                        car.wep.a_pos = car_info['wep_angle']

        game.handle_input()
        game.update()

        # wrap our car information
        car_info = {'id': game.id,
                    'pos': game.car.body.position,
                    'a_pos': game.car.body.angle,
                    'vel': game.car.body.velocity,
                    'steering_angle': game.car.steering_angle,
                    'wep_angle': game.car.wep.a_pos}

        conn.send(json.dumps(car_info).encode())

        game.render()
        clock.tick(60)


if __name__ == '__main__':
    # uvloop.install()

    game_conn, h_input_conn = multiprocessing.Pipe()

    # Start the game loop and input handling processes
    game_process = multiprocessing.Process(target=run_client_loop, args=(game_conn,))
    game_process.start()

    # Create an asyncio event loop and run the handle_input coroutine
    asyncio_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(asyncio_loop)
    asyncio_loop.run_until_complete(handle_server(h_input_conn))

    # Wait for the game process to finish
    game_process.terminate()
    game_process.join()
