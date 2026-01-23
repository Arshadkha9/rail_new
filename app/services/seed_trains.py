import json
from pathlib import Path
from sqlalchemy.orm import Session

from app.models.train import Train


def load_trains(db: Session):
    data_path = Path(__file__).resolve().parent.parent / "data" / "trains.json"
    trains = json.loads(data_path.read_text())

    for item in trains:
        exists = db.query(Train).filter(Train.train_no == item["train_no"]).first()
        if not exists:
            db.add(Train(**item))

    db.commit()