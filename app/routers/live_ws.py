from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json
from app.core.redis_client import redis_client
from app.core.pubsub import CHANNEL

router = APIRouter()

@router.websocket("/ws/train/{train_no}")
async def train_live_status(ws: WebSocket, train_no: str):
    await ws.accept()

    pubsub = redis_client.pubsub()
    pubsub.subscribe(CHANNEL)

    try:
        while True:
            message = pubsub.get_message(ignore_subscribe_messages=True)

            if message:
                data = json.loads(message["data"])

                # sirf wahi train bhejo jo client ne open ki
                if data.get("train_no") == train_no:
                    await ws.send_json(data)

            await asyncio.sleep(0.1)

    except WebSocketDisconnect:
        pubsub.unsubscribe(CHANNEL)
        print(f"Client disconnected for train {train_no}")
