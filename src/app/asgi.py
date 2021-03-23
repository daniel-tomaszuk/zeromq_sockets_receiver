import asyncio

import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.main import get_application
from app.monitoring.receivers import Collector

asgi_app: FastAPI = get_application()
socket_receiver: Collector = Collector()
templates = Jinja2Templates(directory="templates")
asgi_app.mount("/static", StaticFiles(directory="static"), name="static")

app_async_tasks = []


@asgi_app.on_event("startup")
async def add_app_db_events_listeners():
    app_async_tasks.append(asyncio.create_task(socket_receiver.collect_data()))


@asgi_app.on_event("shutdown")
async def add_app_db_events_listeners():
    await socket_receiver.terminate()
    [task.cancell() for task in app_async_tasks]


if __name__ == "__main__":
    # app_workers: int = os.cpu_count() // 6  # https://docs.gunicorn.org/en/stable/design.html#how-many-workers
    app_workers = 1
    uvicorn.run("asgi:asgi_app", host="0.0.0.0", port=8000, timeout_keep_alive=60, workers=app_workers)
