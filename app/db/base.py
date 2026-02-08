from app.db.session import Base

# 👇 FORCE import all models
from app.models.user import User
from app.models.station import Station
from app.models.train import Train
from app.models.route import TrainRoute
from app.models.favorite import Favorite
from app.models.notification import Notification
from app.models.refresh_token import RefreshToken
