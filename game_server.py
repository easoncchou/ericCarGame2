import asyncio
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


class ClientContext:
    clients: dict

    def __init__(self, gs_conn, cp_conn):
        self.gs_conn = gs_conn
        self.cp_conn = cp_conn
        self.clients = {}

    def add_client(self, _id, client_writer):
        self.clients[_id] = client_writer

    def remove_client(self, _id):
        self.clients.pop(_id)

    async def handle_client(self, client_reader, client_writer):
        _id = len(self.clients)
        self.add_client(_id, client_writer)

        # send a start-up message
        try:
            init_pos = (100, 100)
            new_car_info = {'id': _id, 'init_pos': init_pos}
            out_msg = {'init': new_car_info,
                       'add_cars': {}}

            self.gs_conn.send({'type': 'get_cars'})

            while not self.gs_conn.poll():
                pass

            out_msg['add_cars'] = json.loads(self.gs_conn.recv().decode())

            await net.write_message(client_writer,
                                    json.dumps(out_msg).encode())

            for __id, client in self.clients.items():
                if _id != __id:
                    await net.write_message(client, json.dumps(
                        {'add_cars': {_id: init_pos}}).encode())

            print(f"Connection from {_id} opened")
        except Exception as e:
            # Remove the client if there's an error sending data
            self.remove_client(_id)
            print(f"Error with client {_id}: {e}")

        # create the car
        self.gs_conn.send({'type': 'add_car', 'data': _id})

        event = asyncio.Event()

        async def receive_data(event: asyncio.Event):
            while not event.is_set():
                try:
                    data = await net.read_message(client_reader)

                    message = json.loads(data.decode())
                    print(f"Received from client: {message}")
                    message['id'] = _id

                    self.cp_conn.send(json.dumps(message).encode())
                except ConnectionError as e:
                    print(f'{type(e).__name__} while receiving: {e}')
                    event.set()
                except Exception as e:
                    print(f'{type(e).__name__} while receiving: {e}')

        async def send_data(event: asyncio.Event):
            while not event.is_set():
                await asyncio.sleep(0)
                if self.cp_conn.poll():
                    msg = self.cp_conn.recv()
                    while self.cp_conn.poll():
                        msg = self.cp_conn.recv()

                    # Broadcast the updated game_state to all connected clients
                    for __id, client in self.clients.items():
                        await net.write_message(client, msg)

        receive_task = asyncio.create_task(receive_data(event))
        send_task = asyncio.create_task(send_data(event))

        try:
            await asyncio.gather(receive_task, send_task)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"Error with client {_id}: {e}")
        finally:
            self.remove_client(_id)

            try:
                client_writer.close()
                await client_writer.wait_closed()
            except Exception as e:
                print(f'{type(e).__name__} while closing: {e}')

            print(f"Connection from {_id} closed")


def run_server_game_loop(gs_conn, cp_conn):
    import pygame

    pygame.init()
    size = (0, 0)
    pygame.display.set_mode(size)

    clock = pygame.time.Clock()

    game = Game()

    while True:
        if gs_conn.poll():
            msg = gs_conn.recv()

            # todo make adding car more general
            if msg.get('type') == 'add_car':
                init_pos = pymunk.Vec2d(100, 100)

                # load the image for the car
                car_image = pygame.image.load("assets/car1.png")
                # Resize
                car_image = pygame.transform.scale(
                    car_image,
                    (45, 80),
                )

                # define the pygame sprite for the machine gun
                gun_image = pygame.image.load("assets/machine_gun1.png")
                gun_image = pygame.transform.scale(gun_image, [40, 70])

                # create car and wep
                car = Car2(game.space, 1000, init_pos, 250, car_image)
                wep1 = MachineGun(init_pos, 20, 10, 500, pymunk.Vec2d(-4, 15),
                                  gun_image)

                # add wep to car and car to game
                car.set_weapon(wep1)

                game.add_car(car, msg.get('data'))
            elif msg.get('type') == 'get_cars':
                out_msg = {}

                for _id, car in game.cars.items():
                    car_info = {'pos': car.body.position, 'a_pos': car.body.angle,
                                'vel': car.body.velocity,
                                'steering_angle': car.steering_angle,
                                'wep_angle': car.wep.a_pos}

                    out_msg[_id] = car_info

                gs_conn.send(json.dumps(out_msg).encode())

        while cp_conn.poll():
            data = cp_conn.recv()

            car_info = json.loads(data.decode())
            car = game.cars[car_info['id']]

            car.body.position = pymunk.Vec2d(car_info['pos'][0], car_info['pos'][1])
            car.body.angle = car_info['a_pos']
            car.update_grooves()
            car.body.velocity = car_info['vel']
            car.steering_angle = car_info['steering_angle']
            car.wep.a_pos = car_info['wep_angle']

        out_msg = {'update_cars': {}}

        for _id, car in game.cars.items():
            car_info = {'pos': car.body.position, 'a_pos': car.body.angle,
                        'vel': car.body.velocity,
                        'steering_angle': car.steering_angle,
                        'wep_angle': car.wep.a_pos}

            out_msg['update_cars'][_id] = car_info

        cp_conn.send(json.dumps(out_msg).encode())

        game.update()
        clock.tick(TICKRATE)


async def run_server(ctx):
    # Start the server
    server = await asyncio.start_server(ctx.handle_client, HOST, PORT)

    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")

    # Serve clients indefinitely
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    gs_conn1, gs_conn2 = multiprocessing.Pipe()
    cp_conn1, cp_conn2 = multiprocessing.Pipe()

    # Start the game loop and input handling processes
    game_process = multiprocessing.Process(target=run_server_game_loop,
                                           args=(gs_conn1, cp_conn1))
    game_process.start()

    ctx = ClientContext(gs_conn2, cp_conn2)
    asyncio.run(run_server(ctx))

    # Wait for the game process to finish
    game_process.terminate()
    game_process.join()
