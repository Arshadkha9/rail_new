from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.station import Station
from app.services.seed_stations import load_stations

router = APIRouter(prefix="/api/stations", tags=["Stations"])


@router.get("/")
def list_stations(db: Session = Depends(get_db)):
    load_stations(db)
    stations = db.query(Station).all()
    return stations
