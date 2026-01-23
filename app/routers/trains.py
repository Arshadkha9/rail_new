from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.train import Train
from app.services.seed_trains import load_trains

router = APIRouter(prefix="/api/trains", tags=["Trains"])


@router.get("/")
def search_trains(
    q: str = Query(None, description="Train number or name"),
    db: Session = Depends(get_db),
):
    load_trains(db)

    query = db.query(Train)
    if q:
        query = query.filter(
            (Train.train_no.ilike(f"%{q}%")) |
            (Train.name.ilike(f"%{q}%"))
        )

    return query.all()
