from sqlalchemy import Column, Integer, String, Index
from app.db.session import Base

class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    city = Column(String(100), nullable=True)

    __table_args__ = (
        Index("ix_station_code", "code"),
    )
