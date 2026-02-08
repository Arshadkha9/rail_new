from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.notification import Notification
from app.services.notification_engine import generate_mock_notifications

router = APIRouter(prefix="/me", tags=["Notifications"])


@router.post("/notifications/mock")
def trigger_notifications(
    db: Session = Depends(get_db),
):
    generate_mock_notifications(db)
    return {"message": "Mock notifications generated"}

@router.get("/notifications")
def get_notifications(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    rows = (
        db.query(Notification)
        .filter(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )

    return [
        {
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "is_read": n.is_read,
            "created_at": n.created_at
        }
        for n in rows
    ]


@router.post("/notifications/{notification_id}/read")
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    notif = (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == current_user.id
        )
        .first()
    )

    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")

    notif.is_read = True
    db.commit()

    return {"message": "Notification marked as read"}

@router.get("/notifications/unread-count")
def unread_count(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    count = (
        db.query(Notification)
        .filter(
            Notification.user_id == current_user.id,
            Notification.is_read == False
        )
        .count()
    )

    return {"unread_count": count}
