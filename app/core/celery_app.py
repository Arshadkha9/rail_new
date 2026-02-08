from celery import Celery
import app.db.base 

celery_app = Celery(
    "train_tracker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
    include=["app.tasks.notification_tasks"],  # 👈 IMPORTANT
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
)

