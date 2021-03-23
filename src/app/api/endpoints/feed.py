import asyncio

from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from sse_starlette.sse import EventSourceResponse

from app.asgi import socket_receiver
from app.asgi import templates

router = APIRouter()


def init_app(app_instance):
    app_instance.include_router(router, tags=["feed"])


@router.get("/feed")
async def feed(request: Request) -> EventSourceResponse:
    client_queue: asyncio.Queue = asyncio.Queue()
    await socket_receiver.add_connecetion_queue(client_queue)
    return EventSourceResponse(socket_receiver.get_collected_data(client_queue))


@router.get("/stats", response_class=HTMLResponse)
async def stats(request: Request) -> EventSourceResponse:
    return templates.TemplateResponse("index.html", {"request": request})
