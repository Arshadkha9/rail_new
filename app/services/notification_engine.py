import random
from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.models.favorite import Favorite
from app.models.train import Train
from app.core.redis_client import redis_client
from app.core.pubsub import publish_train_update



def get_cache_key(train_id: int):
    return f"train_status:{train_id}"


# def generate_mock_notifications(db: Session):
#     favorites = db.query(Favorite).all()

#     for fav in favorites:
#         train = db.query(Train).filter(Train.id == fav.train_id).first()
#         if not train:
#             continue

#         if random.choice([True, False]):
#             notif = Notification(
#                 user_id=fav.user_id,
#                 title="Train Delay Alert",
#                 message=f"Train {train.train_no} is running late"
#             )
#             db.add(notif)

#     db.commit()

# def generate_mock_notifications(db: Session):
#     favorites = db.query(Favorite).all()

#     for fav in favorites:
#         train = db.query(Train).filter(Train.id == fav.train_id).first()
#         if not train:
#             continue

#         # MOCK current delay
#         current_delay = random.randint(0, 60)

#         key = get_cache_key(train.id)
#         last_delay = redis_client.get(key)

#         # ONLY act if delay changed
#         if last_delay is not None and int(last_delay) == current_delay:
#             continue

#         # update cache
#         redis_client.set(key, current_delay, ex=600)  # 10 min TTL

#         notif = Notification(
#             user_id=fav.user_id,
#             title="Train Delay Alert",
#             message=f"Train {train.train_no} delay changed to {current_delay} minutes"
#         )
#         db.add(notif)

#     db.commit()



def generate_mock_notifications(db: Session):
    favorites = db.query(Favorite).all()

    for fav in favorites:
        train = db.query(Train).filter(Train.id == fav.train_id).first()
        if not train:
            continue

        current_delay = random.randint(0, 60)

        key = get_cache_key(train.id)
        last_delay = redis_client.get(key)

        if last_delay is not None and int(last_delay) == current_delay:
            continue

        redis_client.set(key, current_delay, ex=600)

        # 🔥 PUB/SUB HERE
        publish_train_update({
            "train_id": train.id,
            "train_no": train.train_no,
            "delay": current_delay
        })

        notif = Notification(
            user_id=fav.user_id,
            title="Train Delay Alert",
            message=f"Train {train.train_no} delay changed to {current_delay} minutes"
        )
        db.add(notif)

    db.commit()
