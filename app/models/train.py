from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Train(Base):
    __tablename__ = "trains"

    id = Column(Integer, primary_key=True, index=True)
    train_no = Column(String(10), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
