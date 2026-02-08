from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db,engine, Base
from app.routers import stations, trains, routes, status, admin, auth, favorites,notifications,live_ws
from app.models import station, train, route, user, favorite,notification,refresh_token
from app.core.scheduler import start_scheduler
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.limiter import limiter


Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)
app.include_router(stations.router)
app.include_router(trains.router)
app.include_router(routes.router)
app.include_router(status.router)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(favorites.router)
app.include_router(notifications.router)
app.include_router(live_ws.router)
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)


@app.on_event("startup")
def startup_event():
    start_scheduler()



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
