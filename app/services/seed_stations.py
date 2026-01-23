import json
from pathlib import Path
from sqlalchemy.orm import Session

from app.models.station import Station



def load_stations(db: Session):
    data_path = Path(__file__).resolve().parent.parent / "data" / "stations.json"
    stations = json.loads(data_path.read_text())

    for item in stations:
        exists = db.query(Station).filter(Station.code == item["code"]).first()
        if not exists:
            db.add(Station(**item))

    db.commit()

