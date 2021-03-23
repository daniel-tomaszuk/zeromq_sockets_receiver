import asyncio
from contextlib import suppress
from typing import Optional
from weakref import WeakSet

import ujson
import zmq
import zmq.asyncio

connections = WeakSet()


class Collector:
    def __init__(self):
        self.zmq_context: zmq.asyncio.Context = zmq.asyncio.Context()
        self.sock: Optional[zmq.asyncio.Socket] = None

    async def collect_data(self):
        self.sock: zmq.asyncio.Socket = self.sock or await self.__get_sub_socket()
        with suppress(asyncio.CancelledError):
            while True:
                while data := await self.sock.recv_json():
                    print(f"\nActive connections: {connections}")
                    for connection in connections:
                        await connection.put(ujson.dumps(data))
        self.sock.close()

    async def get_collected_data(self, client_queue: asyncio.Queue):
        with suppress(asyncio.CancelledError):
            while data := await client_queue.get():
                print(f"Sending data to FE client: {data}")
                yield dict(data=data)

        await self.remove_connection_queue(client_queue)

    async def terminate(self):
        self.zmq_context.term()

    async def add_connecetion_queue(self, client_queue: asyncio.Queue):
        connections.add(client_queue)

    async def remove_connection_queue(self, client_queue: asyncio.Queue):
        connections.remove(client_queue)

    async def __get_sub_socket(self, socket_topic_name: str = "") -> zmq.asyncio.Socket:
        sock: zmq.asyncio.Socket = self.zmq_context.socket(zmq.SUB)
        sock.setsockopt_string(zmq.SUBSCRIBE, socket_topic_name)
        try:
            sock.bind("tcp://0.0.0.0:8888")
        except Exception as e:
            print(e)
        return sock
