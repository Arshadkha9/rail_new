from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.train import Train
from app.models.route import TrainRoute
from app.models.station import Station
from app.services.seed_routes import load_routes

router = APIRouter(prefix="/api/trains", tags=["Routes"])


@router.get("/{train_no}/route")
def get_route(train_no: str, db: Session = Depends(get_db)):
    load_routes(db)

    train = db.query(Train).filter(Train.train_no == train_no).first()
    if not train:
        return {"error": "Train not found"}

    rows = (
        db.query(TrainRoute, Station)
        .join(Station, TrainRoute.station_id == Station.id)
        .filter(TrainRoute.train_id == train.id)
        .order_by(TrainRoute.stop_order)
        .all()
    )

    return {
        "train_no": train.train_no,
        "train_name": train.name,
        "route": [
            {
                "order": r.TrainRoute.stop_order,
                "code": r.Station.code,
                "name": r.Station.name,
            }
            for r in rows
        ],
    }
