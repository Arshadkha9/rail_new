import json
from app.core.redis_client import redis_client

CHANNEL = "train_updates"

def publish_train_update(data: dict):
    redis_client.publish(CHANNEL, json.dumps(data))
