from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db,engine, Base
from app.models import station, train
from app.routers import stations
from app.routers import trains



Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)
app.include_router(stations.router)
app.include_router(trains.router)

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": settings.APP_NAME
    }


@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    return {
        "db": "connected"
    }
