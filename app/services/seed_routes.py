import json
from pathlib import Path
from sqlalchemy.orm import Session

from app.models.train import Train
from app.models.station import Station
from app.models.route import TrainRoute


def load_routes(db: Session):
    data_path = Path(__file__).resolve().parent.parent / "data" / "routes.json"
    routes = json.loads(data_path.read_text())

    for item in routes:
        train = db.query(Train).filter(Train.train_no == item["train_no"]).first()
        if not train:
            continue

        for idx, code in enumerate(item["stations"], start=1):
            station = db.query(Station).filter(Station.code == code).first()
            if not station:
                continue

            exists = db.query(TrainRoute).filter_by(
                train_id=train.id,
                station_id=station.id
            ).first()

            if not exists:
                db.add(
                    TrainRoute(
                        train_id=train.id,
                        station_id=station.id,
                        stop_order=idx
                    )
                )

    db.commit()
