from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.seed_stations import load_stations
from app.services.seed_trains import load_trains
from app.services.seed_routes import load_routes

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/seed-all")
def seed_all(db: Session = Depends(get_db)):
    load_stations(db)
    load_trains(db)
    load_routes(db)

    return {
        "status": "ok",
        "message": "Stations, Trains, and Routes seeded successfully"
    }
