from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.live_status import get_live_status

router = APIRouter(prefix="/api/trains", tags=["Live Status"])


@router.get("/{train_no}/status")
def train_status(train_no: str, db: Session = Depends(get_db)):
    data = get_live_status(db, train_no)
    if not data:
        return {"error": "Train or route not found"}
    return data
