from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from datetime import datetime
from app.db.session import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    title = Column(String(255), nullable=False)
    message = Column(String(500), nullable=False)

    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
