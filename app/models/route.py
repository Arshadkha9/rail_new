from sqlalchemy import Column, Integer, ForeignKey
from app.db.session import Base

class TrainRoute(Base):
    __tablename__ = "train_routes"

    id = Column(Integer, primary_key=True)
    train_id = Column(Integer, ForeignKey("trains.id"), nullable=False)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    stop_order = Column(Integer, nullable=False)
