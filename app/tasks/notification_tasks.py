from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app.services.notification_engine import generate_mock_notifications

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3})
def run_notification_engine(self):
    db = SessionLocal()
    try:
        generate_mock_notifications(db)
    finally:
        db.close()
