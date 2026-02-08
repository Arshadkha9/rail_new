from apscheduler.schedulers.background import BackgroundScheduler
from app.db.session import SessionLocal
from app.services.notification_engine import generate_mock_notifications

def start_scheduler():
    scheduler = BackgroundScheduler()

    def job():
        db = SessionLocal()
        try:
            generate_mock_notifications(db)
        finally:
            db.close()

    scheduler.add_job(
        job,
        trigger="interval",
        minutes=1,   # har 1 minute (testing)
        id="notification_job",
        replace_existing=True
    )

    scheduler.start()
