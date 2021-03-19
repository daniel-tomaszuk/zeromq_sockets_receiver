import asyncio
from contextlib import suppress
from weakref import WeakSet


import zmq
import zmq.asyncio

zmq_context: zmq.asyncio.Context = zmq.asyncio.Context()
connections = WeakSet()


async def collector():
    sock: zmq.asyncio.Socket = zmq_context.socket(zmq.SUB)
    sock.setsockopt_string(zmq.SUBSCRIBE, "")
    sock.bind("tmp://*:5555")
    with suppress(asyncio.CancelledError):
        while data := await sock.recv_json():
            print(data)
            for connection in connections:
                await connection.put(data)
    sock.close()
