from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.db.session import Base

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    train_id = Column(Integer, ForeignKey("trains.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "train_id", name="uq_user_train"),
    )
