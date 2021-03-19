import asyncio
from contextlib import suppress
from datetime import datetime
from datetime import timezone

import psutil
import zmq
import zmq.asyncio


zmq_context: zmq.asyncio.Context = zmq.asyncio.Context()


async def stats_reporter(color: str):
    process: psutil.Process = psutil.Process()
    sock: zmq.asyncio.Socket = zmq_context.socket(zmq.PUB)
    sock.setsockopt(zmq.LINGER, 1)
    sock.connect("tcp://localhost:5555")
    with suppress(asyncio.CancelledError):
        while True:
            await sock.send_json(
                dict(
                    color=color,
                    timestamp=datetime.now(tz=timezone.utc).isoformat(),
                    cpu=process.cpu_percent(),
                    mem=process.memory_full_info().rss / 1024 / 1024
                )
            )
            await asyncio.sleep(1)
    sock.close()





