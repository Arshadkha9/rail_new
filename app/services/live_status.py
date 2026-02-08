# import random
# from datetime import datetime

# from sqlalchemy.orm import Session
# from app.models.train import Train
# from app.models.route import TrainRoute
# from app.models.station import Station


# def get_live_status(db: Session, train_no: str):
#     train = db.query(Train).filter(Train.train_no == train_no).first()
#     if not train:
#         return None

#     rows = (
#         db.query(TrainRoute, Station)
#         .join(Station, TrainRoute.station_id == Station.id)
#         .filter(TrainRoute.train_id == train.id)
#         .order_by(TrainRoute.stop_order)
#         .all()
#     )

#     if not rows:
#         return None

#     # Pick a random "current" station from route
#     current = random.choice(rows)

#     delay = random.choice([0, 5, 10, 15, 20])

#     return {
#         "train_no": train.train_no,
#         "train_name": train.name,
#         "current_station": current.Station.code,
#         "last_updated": datetime.utcnow().isoformat(),
#         "delay_minutes": delay,
#         "status_message": (
#             "On time" if delay == 0 else f"Running late by {delay} minutes"
#         ),
#     }



from datetime import datetime
from sqlalchemy.orm import Session

from app.integrations.railway_api import fetch_live_status
from app.models.train import Train


def get_live_status(db: Session, train_no: str):
    train = db.query(Train).filter(Train.train_no == train_no).first()
    if not train:
        return None

    api_data = fetch_live_status(train_no)

    # 👇 Railway API response mapping
    current_station = api_data["current_station"]["code"]
    delay = api_data.get("delay", 0)

    return {
        "train_no": train.train_no,
        "train_name": train.name,
        "current_station": current_station,
        "last_updated": datetime.utcnow().isoformat(),
        "delay_minutes": delay,
        "status_message": (
            "On time" if delay == 0 else f"Running late by {delay} minutes"
        ),
    }